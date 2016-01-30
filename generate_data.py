#!/usr/bin/python

import json
import controller
from temperature_interface import RandomTemperature
import view

if __name__ == "__main__":
    with RandomTemperature(18, 32) as random_temp:
        view.run()
        controller.run_controller(random_temp, 1)
