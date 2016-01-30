import abc
import serial
import time

class TemperatureInterface:
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def request_new_sample(self):
        pass

    @abc.abstractmethod
    def retrieve_new_sample(self):
        pass

class ArduinoTemperature(TemperatureInterface):

    def __init__(self, arduino_serial_device):
        self.__serial_device = arduino_serial_device
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
        # line can be cluttered with previous serial entry as well
        # safest way to get the temperature is to take the last word
        words = sample_with_prefix.split()
        return words[len(words) - 1]

    def __read_sample(self):
        temperature = self.__connection.readline()
        return temperature.strip()
