#!/usr/bin/python

import json
import os.path
import shutil
import time_utils
from time import sleep
from temperature_interface import ArduinoTemperature


def temperature_sample_to_json(today, now, temperature):
    entry = {
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry


if __name__ == '__main__':
    with open('configuration.json') as main_configuration_file:
        config = json.load(main_configuration_file)

    with ArduinoTemperature(config['arduino_serial_port']) as arduino:
        data = []

        while True:
            today_str = time_utils.get_today_string()
            filename = 'temperature_' + today_str + '.json'

            # create file if it does not exists
            if not os.path.isfile(filename):
                with open(filename, "w") as newfile:
                    newfile.write('[]')

            # get current data
            with open(filename, "r") as datafile:
                data = json.load(datafile)
                print data

            # request a new sample
            arduino.request_new_sample()

            # prepare date
            today = time_utils.get_today_string()
            now = time_utils.get_now_string()
            # retrieve the sample
            sample = arduino.retrieve_new_sample()

            # put the sample in json format to the current data
            data.append(temperature_sample_to_json(today, now, sample))

            # write it back to the file
            with open(filename, "w") as datafile:
                parseable_data = json.dumps(data)
                datafile.write(parseable_data)

            shutil.copyfile(filename, 'visualisation/' + filename)

            # wait before requesting a new sample
            sleep(config['sample_interval'])
