// This Arduino sketch reads DS18B20 "1-Wire" digital temperature sensor.
// http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf

// Inspiration from:
// * code -> http://www.hacktronics.com/Tutorials/arduino-1-wire-tutorial.html
// * wiring -> http://www.hobbytronics.co.uk/ds18b20-arduino

// How it works:
// The arduino reads on it's serial line for commands:
// * If COMMAND_REQUEST_TEMP is send on the serial line, the arduino
//   will request the temparature from the devices connected on the onewire bus

#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 3 on the Arduino
static const int ONE_WIRE_BUS = 3;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);

// List of available commands
static const int COMMAND_TIMEOUT = 0;
static const int COMMAND_REQUEST_TEMP = 1;

// Assign the addresses of your 1-Wire temp sensors.
// See the tutorial on how to obtain these addresses:
// http://www.hacktronics.com/Tutorials/arduino-1-wire-address-finder.html
DeviceAddress thermometer = { 0x28, 0x08, 0xF0, 0x5A, 0x06, 0x00, 0x00, 0x0B };

void setup(void) {
  // start serial port
  Serial.begin(9600);
  // Start up the library
  sensors.begin();
  // set the resolution to 10 bit (good enough?)
  sensors.setResolution(thermometer, 10);
}

void __printTemperature(DeviceAddress deviceAddress) {
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == -127.00) {
    Serial.print("Error getting temperature");
  } else {
    Serial.print("C: ");
    Serial.print(tempC);
  }
}

void requestTemperature() {
  sensors.requestTemperatures();
  __printTemperature(thermometer);
  Serial.print("\n\r");
}

void loop(void) {
  delay(2000);
  int requestedCommand = Serial.parseInt();
  if (requestedCommand == COMMAND_REQUEST_TEMP)
    requestTemperature();
  // else, command might be COMMAND_TIMEOUT or an invalid value
}
