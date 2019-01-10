#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sensor.py
#  
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#  

class Sensor:
	def __init__(self, name, sensor_type, location, image_path):
		self.name = name
		self.sensor_type = sensor_type
		self.location = location
		self.image_path = image_path
		
def create_sensor_from_json(json):
	name = json['name']
	sensor_type = json['sensor_type']
	location = json['location']
	image_path = json['image_path']
	return Sensor(name, sensor_type, location, image_path)
		
