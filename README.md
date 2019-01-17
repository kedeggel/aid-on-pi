# AID on Raspberry Pi
Python module that interacts with **AID** - the **Automated Intrusion Detection System** - which can be found right [here](https://github.com/kedeggel/aid) on Github.

## Prerequisites
### CouchDB
- Install CouchDB
- Create databases `register` for device tokens (needed for push notifications) and `aid` (for detection events)

### Motion
- Install package [motion](https://github.com/Motion-Project/motion)

## Installation
### General 
- Clone this repository on your Raspberry Pi
- Add file `pushy_api.key` with your API Key generated on [Pushy](https://pushy.me/)  
- Create new sensor by running `python3 add_sensor.py` which leads you through the whole creation steps
- After this process the file `sensors.conf` is updated (or generated if it doesn't exist)
- To test the script run `python motion_detection.py <sensor>` where `sensor` is the name of one existing sensor
- If no error occurs, add the call (without the verbose flag) as callback method to a motion detection sensor script, e.g. in `motion.conf` at `on_event_start`

### Camera
- Open `motion.conf` (default path: `/etc/motion/motion.conf`)
- Add `python3 <path_to_repo>/motion_detected.py <camera_name>` to `on_event_start`

### Reed switch
- Connect your reed switch to the Raspberry Pi
- Adjust variable `ReedPin` in `magnetic_detector.py` to the pin you connected the signal cable (default: 11)
- Add `magnetic_detector.py` to autostart

## Hints
It is highly recommended not to change entries in config file manually to avoid incompatible sensor entries.
