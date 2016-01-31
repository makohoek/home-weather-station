#!/usr/bin/python

import json
import controller
from temperature_interface import ArduinoTemperature
import view

if __name__ == "__main__":
    with open('configuration.json') as main_configuration_file:
        config = json.load(main_configuration_file)

    with ArduinoTemperature(config['arduino_serial_port']) as arduino:
        view.run()
        controller.run_controller(arduino, config['sample_interval'])
