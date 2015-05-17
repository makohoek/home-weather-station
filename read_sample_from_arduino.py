#!/usr/bin/python

# from http://playground.arduino.cc/Interfacing/Python
# need to pip install pyserial before :)

import serial
import time

requestTemperatureCommandCode = '1'

ser = serial.Serial("/dev/cu.usbmodem621", 9600)
# two seconds should be enough to establish the serial connection
time.sleep(2)

while True:
    ser.write(requestTemperatureCommandCode)
    time.sleep(1)
    temperature = ser.readline()
    print temperature.strip()

ser.close()
