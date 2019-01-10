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

current_timestamp = lambda: int(round(time.time() * 1000))

SENSORS_JSON = [
	{
		'name': 'camera01',
		'sensor_type': 'camera',
		'location': 'bedroom',
		'image_path': '/home/pi/Monitor/lastsnap.jpg',
	},
	{
		'name': 'magnet01',
		'sensor_type': 'magnet_sensor',
		'location': 'living room',
		'image_path': None,
	}
]
BASE_URL = 'localhost'
DB_PORT = 5984
DB_PATH = '/aid'	# don't forget the starting '/'
MOTION_PORT = 8080
MOTION_PATH = '/0/action/'
POST = 'POST'
PUT = 'PUT'
GET = 'GET'

sensors = list(map(lambda s: sensor.create_sensor_from_json(s), SENSORS_JSON))


def send_request(path, port, method, body=None, headers={}):
	conn = http.client.HTTPConnection(BASE_URL, port=port)
	conn.request(method, path, body, headers)
	resp = conn.getresponse()
	resp_data = resp.read()
	return resp_data.decode('utf-8')
	

def add_detection_entry(sensor):
	data = {
		'sensor': sensor.name,
		'location': sensor.location,
		'timestamp': current_timestamp()
	}
	headers = {'Content-type': 'application/json'}
	json_data = json.dumps(data)
	
	resp = send_request(DB_PATH, DB_PORT, POST, json_data, headers)

	return json.loads(resp)
	
	
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


def take_snapshot():
	send_request('{}snapshot'.format(MOTION_PATH), MOTION_PORT, GET)


def get_sensor_by_name(name):
	for s in sensors:
		if s.name == name:
			return s
	return None


def get_sensor_names():
	return list(map(lambda s: s.name, sensors)) 
	
	
def motion_detected(sensor_name):
	sensor = get_sensor_by_name(sensor_name)
	if sensor.sensor_type == 'camera':
		take_snapshot()
			
	if sensor == None:
		print('\'{}\' is not a valid sensor.\nKnown sensors: {}'
		.format(sensor_name, get_sensor_names()))
		return
	resp_data = add_detection_entry(sensor)
	
	if sensor.image_path is not None:
		if resp_data['ok']:
			print('+++ Detection entry uploaded successfully +++')
			id = resp_data['id']
			rev = resp_data['rev']
			att_resp = add_attachment(id, rev, sensor.image_path)
			if att_resp and att_resp['ok']:
				print('+++ Attachment uploaded successfully +++')

		else:
			print('Error while uploading detection entry!')

def main(args):
	if len(args) > 1:
		motion_detected(args[1])
	else:
		print('usage: python motion_detected.py [sensor]')
	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
