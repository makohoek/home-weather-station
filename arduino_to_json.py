#!/usr/bin/python

import pprint
import re
import serial
import time
import json


#TODO: reimplement this as a client service design pattern
#TODO: reimplment this as a with statement stuff
class TemperatureInterface(object):

    def __init__(self):
        self.connection = serial.Serial("/dev/cu.usbmodem621", 9600)
        self.requestTemperatureCommandCode = '1'
        # FIXME: for now, we are just sleeping after a new connection
        # we should implement at arduino side a command to check if
        # serial connection is established
        time.sleep(2)

    def request_new_sample(self):
        self.connection.write(self.requestTemperatureCommandCode)

    def wait_for_response(self):
        # FIXME: for now, we are just sleeping after a request
        # we should implement at arduino side a command to check if new sample
        # is available
        time.sleep(0.5)

    def __read_sample(self):
        temperature = self.connection.readline()
        return temperature.strip()

    def retrieve_new_sample(self):
        sample_with_prefix = self.__read_sample()
        return sample_with_prefix.lstrip('C: ')


def temperature_sample_to_json(today, now, temperature):
    entry = {
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry


def get_today_string():
    localtime = time.localtime()
    today = time.strftime("%Y-%m-%d", localtime)
    return today


if __name__ == '__main__':
    arduino = TemperatureInterface()
    data = []

    #TODO: add daystring in filename
    today_str = get_today_string()
    current_data_file = 'temperature_' + today_str + '.json'

    while True:
        # get current data
        with open("thermal_data.json", "r") as datafile:
            data = json.load(datafile)
            print data

        # request a new sample
        arduino.request_new_sample()

        # wait for the thermometer to process
        arduino.wait_for_response()

        # prepare date
        localtime = time.localtime()
        today = time.strftime("%Y-%m-%d", localtime)
        now = time.strftime("%H:%M:%S", localtime)
        # retrieve the sample
        sample = arduino.retrieve_new_sample()

        # put the sample in json format to the current data
        data.append(temperature_sample_to_json(today, now, sample))

        # write it back to the file
        with open("thermal_data.json", "w") as datafile:
            parseable_data = json.dumps(data)
            datafile.write(parseable_data)
