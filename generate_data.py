#!/usr/bin/python

import json
import controller
from temperature_interface import RandomTemperature

if __name__ == "__main__":
    with RandomTemperature(18, 32) as random_temp:
        # TODO: add run_view here as well, which runs the webserver
        controller.run_controller(random_temp, 1)
