import serial
import time


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

    def retrieve_new_sample(self):
        sample_with_prefix = self.__read_sample()
        return sample_with_prefix.lstrip('C: ')

    def __read_sample(self):
        temperature = self.__connection.readline()
        return temperature.strip()
