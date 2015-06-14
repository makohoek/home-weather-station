#!/usr/bin/python

import json
import os.path
import random
import time

def generate_sample_data():
    localtime=time.localtime()
    today=time.strftime("%Y-%m-%d", localtime)
    now=time.strftime("%H:%M:%S", localtime)
    temperature=random.randint(18,32)
    entry={
        "date": today,
        "time": now,
        "temperature": temperature,
    }
    return entry


def get_today_string():
    localtime = time.localtime()
    today = time.strftime("%Y-%m-%d", localtime)
    return today

data=[]

while True:

    today_str = get_today_string()
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
    time.sleep(1)
