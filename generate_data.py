#!/usr/bin/python

import pprint
import random
import re
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

data=[]

for i in range(1,601):
    entry = generate_sample_data()
    data.append(entry)
    print entry
    time.sleep(1)

with open("thermal_data.json","w") as datafile:
    # d3js reads with double quotes, whereas
    # pprint renders the data strings in simple quotes
    # therefore, we need to substitute ' by "
    parseable_data=re.sub("\'","\"", pprint.saferepr(data))
    datafile.write(parseable_data)
