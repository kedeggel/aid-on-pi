#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  magnetic_detector.py
#  
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#  

import RPi.GPIO as GPIO
from motion_detected import motion_detected

ReedPin = 11

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(ReedPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
	GPIO.add_event_detect(ReedPin, GPIO.RISING, callback=detect, bouncetime=200)


def detect(chn):
	reed = GPIO.input(ReedPin)
	if reed == 1:
		motion_detected('magnet01')
		


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		while True:
			pass
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		print('Exiting magnet.py...')
	finally:
		GPIO.cleanup()                    
