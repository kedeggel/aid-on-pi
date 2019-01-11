#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pushy.py
#  
#  Copyright 2019  Kevin Deggelmann<kedeggel@users.noreply.github.com>
#  


import json
import requests
import os

API_KEY_FILE = 'pushy_api.key'

class PushyAPI:

	@staticmethod
	def sendPushNotification(data, to, options = {}):
		# Insert your Pushy Secret API Key here
		if not os.path.exists(API_KEY_FILE):
			print('Error: Pushy API key file does not exist.')
			return
		with open(API_KEY_FILE) as f:
			apiKey = f.readline().strip()
7
			# Default post data to provided options or empty object
			postData = options
			
			# Set notification payload and recipients
			postData['to'] = to
			postData['data'] = data
			
			# Set URL to Send Notifications API endpoint
			req = requests.post('https://api.pushy.me/push?api_key=' + apiKey, json=postData)

