#!/usr/bin/python

import json
import os.path
import random
import time_utils
from time import sleep

def generate_sample_data():
    today=time_utils.get_today_string()
    now=time_utils.get_now_string()
    temperature=random.randint(18,32)
    entry={
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry


data=[]

while True:

    today_str = time_utils.get_today_string()
    filename = '_fake_temperature_' + today_str + '.json'

    if not os.path.isfile(filename):
        with open(filename, "w") as newfile:
            newfile.write('[]')

    # get current data
    with open(filename, "r") as datafile:
        data = json.load(datafile)
        print data

    entry = generate_sample_data()
    data.append(entry)

    # write it back to the file
    with open(filename, "w") as datafile:
        parseable_data = json.dumps(data)
        datafile.write(parseable_data)

    # wait before requesting a new sample
    sleep(1)
