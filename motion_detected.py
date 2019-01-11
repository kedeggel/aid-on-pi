#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  motion_detected.py
#
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#

import sys
import http.client
import time
import json
import os
import sensor
import add_sensor
from pushy import PushyAPI
import requests


current_timestamp = lambda: int(round(time.time() * 1000))

BASE_URL = 'localhost'
DB_PORT = '5984'
DB_PATH = '/aid'	# don't forget the starting '/'
REGISTER_PATH = 'register'
DEVICE_TOKEN_VIEW_PATH = '_design/device-token/_view/device-token'
MOTION_PORT = '8080'
POST = 'POST'
PUT = 'PUT'
GET = 'GET'

def get_sensors():
	return list(map(lambda s: sensor.create_sensor_from_json(s), add_sensor.read_sensors_from_file()))


def send_request(path, port, method, body=None, headers={}):
	conn = http.client.HTTPConnection(BASE_URL, port=port)
	conn.request(method, path, body, headers)
	resp = conn.getresponse()
	resp_data = resp.read()
	return resp_data.decode('utf-8')


def add_detection_entry(sensor):
	data = {
		'sensor': sensor.name,
		'sensortype': sensor.sensor_type,
		'location': sensor.location,
		'timestamp': current_timestamp()
	}
	resp = requests.post('http://{}:{}{}'.format(BASE_URL, DB_PORT, DB_PATH), json=data)
	return resp.json()


def add_attachment(id, rev, image_path):
	if not os.path.exists(image_path):
		print('{} does not exist!'.format(image_path))
		return None

	data = open(image_path, 'rb').read()
	headers = {
		'If-Match': rev,
		'Content-Type': 'image/jpeg'
	}
	path = '{}/{}/{}'.format(DB_PATH, id, os.path.basename(image_path))
	resp = send_request(path, DB_PORT, PUT, data, headers)

	return json.loads(resp)


def take_snapshot(path):
	requests.get('http://{}:{}{}'.format(BASE_URL, MOTION_PORT, path))


def get_sensor_by_name(name):
	for s in get_sensors():
		if s.name == name:
			return s
	return None


def get_sensor_names():
	return list(map(lambda s: s.name, get_sensors()))


def motion_detected(sensor_name):
	sensor = get_sensor_by_name(sensor_name)
	if sensor == None:
		print('\'{}\' is not a valid sensor.\nKnown sensors: {}'
		.format(sensor_name, get_sensor_names()))
		return

	print('+++ Sending push notification')
	send_push('Motion detected by ' + sensor_name) 

	if sensor.snapshot_path is not None:
		take_snapshot(sensor.snapshot_path)
		print('+++ Taking snapshot with ' + sensor.name)
	elif sensor.linked_camera is not None:
		linked_camera = get_sensor_by_name(sensor.linked_camera)
		if linked_camera.snapshot_path is not None:
			take_snapshot(linked_camera.snapshot_path)
			print('+++ Taking snapshot with ' + linked_camera.name)

	resp_data = add_detection_entry(sensor)

	if resp_data['ok']:
		print('+++ Detection entry uploaded successfully +++')
		if sensor.image_path is not None or linked_camera is not None:
			id = resp_data['id']
			rev = resp_data['rev']
			image_path = sensor.image_path
			if sensor.image_path is None:
				image_path = linked_camera.image_path
			if image_path is not None:
				att_resp = add_attachment(id, rev, image_path)
				if att_resp and att_resp['ok']:
					print('+++ Attachment uploaded successfully +++')

			

	else:
		print('Error while uploading detection entry!')


def send_push(message):
	data = {'message': message}

	req = requests.get('http://{}:{}/{}/{}'.format(BASE_URL, DB_PORT, REGISTER_PATH,
						DEVICE_TOKEN_VIEW_PATH))

	json = req.json()
	to = set()
	for entry in json['rows']:
		to.add(entry['value'])
	PushyAPI.sendPushNotification(data, list(to))


def main(args):
	if len(args) > 1:
		motion_detected(args[1])
	else:
		print('usage: python motion_detected.py [sensor]')
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
