#!/usr/bin/python

import json
import os.path
import re
import serial
import time


# TODO: reimplement this as a client service design pattern
class TemperatureInterface:

    def __init__(self):
        self.__serial_device = "/dev/cu.usbmodem621"
        self.__baudrate = 9600
        self.requestTemperatureCommandCode = '1'

    def __enter__(self):
        self.__connection = serial.Serial(
            self.__serial_device,
            self.__baudrate)
        # FIXME: for now, we are just sleeping after a new connection
        # we should implement at arduino side a command to check if
        # serial connection is established
        time.sleep(2)
        return self

    def __exit__(self, type, value, traceback):
        self.__connection.close()

    def request_new_sample(self):
        self.__connection.write(self.requestTemperatureCommandCode)

    def wait_for_response(self):
        # FIXME: for now, we are just sleeping after a request
        # we should implement at arduino side a command to check if new sample
        # is available
        time.sleep(0.5)

    def retrieve_new_sample(self):
        sample_with_prefix = self.__read_sample()
        return sample_with_prefix.lstrip('C: ')

    def __read_sample(self):
        temperature = self.__connection.readline()
        return temperature.strip()


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
    with TemperatureInterface() as arduino:
        data = []

        today_str = get_today_string()
        filename = 'temperature_' + today_str + '.json'

        # create file if it does not exists
        if not os.path.isfile(filename):
            with open(filename, "w") as newfile:
                newfile.write('[]')

        while True:
            # get current data
            with open(filename, "r") as datafile:
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
            with open(filename, "w") as datafile:
                parseable_data = json.dumps(data)
                datafile.write(parseable_data)

            # wait a minute before requesting a new sample
            time.sleep(60)
