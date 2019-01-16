#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  add_sensor.py
#  
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#  

import sys
import json
import os.path

CONF_FILE = os.path.dirname(sys.argv[0]) + '/sensors.conf'

NAME = 'name'
SENSOR_TYPE = 'sensor_type'
LOCATION = 'location'
IMAGE_PATH = 'image_path'
SNAPSHOT_PATH = 'snapshot_path'
LINKED_CAMERA = 'linked_camera'
KEY_ORDER = [NAME, SENSOR_TYPE, LOCATION, IMAGE_PATH, SNAPSHOT_PATH, 
			 LINKED_CAMERA]
		
			
def print_help():
	print_usage()


def print_sensors_list():
	sensors = read_sensors_from_file()
	first = True
	for s in sensors:
		if not first:
			print('++++++++++++++++++++++++++++++++++++++++++++++++++++')
		else:
			first = False
		print_sensor_info(s)
		
					
def print_sensor_info(sensor):
	for key in KEY_ORDER:
			if key == NAME:
				print(sensor[key])
			elif key in sensor.keys():
					print('\t{}\t{}'.format(key, sensor[key]))


def print_usage():
	print('usage: ./add_sensor [-h] [-l] [-d <sensor-name>]')


def delete_sensor(name):
	sensors = read_sensors_from_file()
	sensor = next((s for s in sensors if s['name']==name), None)
	if sensor == None:
		print('Sensor with name \'{}\' does not exist'.format(name))
	else:
		sensors.remove(sensor)
		with open(CONF_FILE, 'w') as f:
			json.dump(sensors, f, indent=4)
		print('Deleted sensor with name \'{}\''.format(name))


def add_new_sensor():
	sensors = read_sensors_from_file()

	print('Add new sensor:')
	
	keys = []
	for s in sensors:
		keys.append(s[NAME])
		
	sensor = dict()
	
	sensor[NAME] = input('Sensor name: ')
		
	while sensor[NAME] in keys or sensor[NAME] == '':
		if sensor[NAME] == '':
			print('+ Sensor name must not empty.')
		else:
			print('+ Sensor name already exists.')
			print('+ Enter a different name to add new sensor.')
		sensor[NAME] = input('Sensor name: ')
		
	add_entry(sensor, SENSOR_TYPE, 'Sensor type')
	add_entry(sensor, LOCATION, 'Location')

	sensor[SNAPSHOT_PATH] = None
	image_path = input('Image path (optional): ')
	if image_path == '':
		image_path = None
		linked_camera = input('Linked camera module (optional): ')
		if not linked_camera == '':
			sensor[LINKED_CAMERA] = linked_camera
		else:
			sensor[LINKED_CAMERA] = None
		
	else:
		add_entry(sensor, SNAPSHOT_PATH, 'Snapshot path')
	sensor[IMAGE_PATH] = image_path


	sensors.append(sensor)
	
	print_sensor_info(sensor)
	with open(CONF_FILE, 'w') as f:
		json.dump(sensors, f, indent=4)

def add_entry(sensor, key, name):
	first_run = True
	sensor[key] = input(name + ': ')
	while sensor[key] == '':
		print('+ ' + name + ' must not empty.')
		sensor[key] = input(name + ': ')
	
	
	
def read_sensors_from_file():
	sensors = []
	if os.path.isfile(CONF_FILE):

		with open(CONF_FILE) as f:
			try:
				sensors = json.load(f)
			except json.decoder.JSONDecodeError:
				print('***************************************************')
				print('* Config file is not in valid json format.        *')
				print('* You can abort and check file format manually.   *')
				print('* Otherwise the existing file will be overwritten.*')
				print('***************************************************')
				print()
			finally:
				return sensors
	return sensors


def main(args):
	try:			
		if len(args) > 1:
			if args[1] == '-h':
				print_help()
			elif args[1] == '-l':
				print_sensors_list()
			elif args[1] == '-d':
				if len(args) > 2:
					delete_sensor(args[2])
				else:
					print('-d expects the name of a sensor that is to be deleted')
			else:
				print('Unknown option: ' + args[1])
				print_usage()
		else:
			add_new_sensor()
	except KeyboardInterrupt:
		print()
		print('Sensor creation aborted...')
	finally:
		return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
