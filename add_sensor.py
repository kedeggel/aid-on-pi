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

CONF_FILE = 'sensors.conf'

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
			
			
def print_help():
	print('help')

def print_sensors_list():
	print('print_sensors_list')
	
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
		keys.append(s['name'])
		
	sensor = dict()
	
	sensor['name'] = input('Sensor name: ')
		
	while sensor['name'] in keys or sensor['name'] == '':
		if sensor['name'] == '':
			print('+ Sensor name must not empty')
		else:
			print('+ Sensor name already exists.')
			print('+ Enter a different name to add new sensor.')
		sensor['name'] = input('Sensor name: ')
		
	sensor['sensor_type'] = input('Sensor type: ')
	while sensor['sensor_type'] == '':
		print('+ Sensor type must not empty')
		sensor['sensor_type'] = input('Sensor type: ')
		
	sensor['location'] = input('Location: ')
	while sensor['location'] == '':
		print('+ Sensor location must not empty')
		sensor['location'] = input('Location: ')


	sensor['image_path'] = input('Image path (optional): ')
	if sensor['image_path'] == '':
		sensor['image_path'] = None
		linked_camera = input('Linked camera module (optional): ')
		if not linked_camera == '':
			sensor['linked_camera'] = linked_camera


	sensors.append(sensor)
	with open(CONF_FILE, 'w') as f:
		json.dump(sensors, f, indent=4)

	
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


if __name__ == '__main__':
    sys.exit(main(sys.argv))
