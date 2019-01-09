# AID on Raspberry Pi
Python module that interacts with **AID** - the **Automated Intrusion Detection System** - which can be found right [here](https://github.com/kedeggel/aid) on Github.

The module contains the **Sensor class** and the **create_sensor script** (_On TODO yet_)

## Installation
- Clone this repository on your Raspberry Pi.
- Create new sensor by running `python add_sensor` which leads you through the whole creation steps. After these process the file `sensors.conf` is updated (or generated if it doesn't exist).
- To test the script run `python motion_detection.py [sensor] verbose=1` where `sensor` is the name of one existing sensor.  
- If no error occurs, add the call (without the verbose flag) as callback method to a motion detection sensor script, e.g. in `motion.conf` at `on_event_start`.  

## Hints
It is highly recommended not to change entries in config file manually to avoid incompatible sensor entries.
