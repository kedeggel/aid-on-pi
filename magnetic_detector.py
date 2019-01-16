#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  magnetic_detector.py
#  
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#  

import RPi.GPIO as GPIO
import time
from motion_detected import motion_detected
import os
import sys

ReedPin = 11
threshold = 5 # in seconds
last_detection_time = -threshold

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ReedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(ReedPin, GPIO.RISING, callback=detect, bouncetime=200)


def detect(chn):
	global last_detection_time
	reed = GPIO.input(ReedPin)
	print('Door opened')
	if reed == 1:
		detection_time = time.clock()
		duration = detection_time - last_detection_time
		if duration > threshold:
			last_detection_time = detection_time
			motion_detected('magnet01')
		else:
			print('Last detection was only ' + str(duration) + ' ago')
			print('But threshold is ' + str(threshold) + ' seconds')



if __name__ == '__main__':     # Program start from here
	os.chdir(os.path.dirname(sys.argv[0]))		# Change cwd to script's path to find config files
	setup()
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print('Exiting magnet.py...')
	finally:
		GPIO.cleanup()
