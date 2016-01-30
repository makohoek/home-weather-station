#!/usr/bin/python

import json
import controller
from temperature_interface import ArduinoTemperature

if __name__ == "__main__":
    with open('configuration.json') as main_configuration_file:
        config = json.load(main_configuration_file)

    with ArduinoTemperature(config['arduino_serial_port']) as arduino:
        #TODO: add run_view here as well, which runs the webserver
        controller.run_controller(arduino, config['sample_interval'])
