#!/usr/bin/python

import json
import os.path
import shutil
import time_utils
from time import sleep
from temperature_interface import RandomTemperature

def temperature_sample_to_json(today, now, temperature):
    entry = {
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry

if __name__ == "__main__":
    with RandomTemperature(18, 32) as random_temp:
        data = []

        while True:
            today_str = time_utils.get_today_string()
            filename = '_fake_temperature_' + today_str + '.json'

            # create file if it does not exists
            if not os.path.isfile(filename):
                with open(filename, "w") as newfile:
                    newfile.write('[]')

            # get current data
            with open(filename, "r") as datafile:
                data = json.load(datafile)
                print data

            # prepare date
            today = time_utils.get_today_string()
            now = time_utils.get_now_string()
            # retrieve the sample
            sample = random_temp.retrieve_new_sample()

            # put the sample in json format to the current data
            data.append(temperature_sample_to_json(today, now, sample))

            # write it back to the file
            with open(filename, "w") as datafile:
                parseable_data = json.dumps(data)
                datafile.write(parseable_data)

            shutil.copyfile(filename, 'visualisation/' + filename)

            # wait before requesting a new sample
            sleep(1)
