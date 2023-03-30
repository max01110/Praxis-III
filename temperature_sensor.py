'''
ESC204S 2023 Lab 5, Task D
Task: Take readings using a digital temperature/humidity sensor.
'''

import board
import bitbangio
import adafruit_am2320
import time

# set up I2C protocol
i2c = bitbangio.I2C(board.GP14, board.GP15)
dhtDevice = adafruit_am2320.AM2320(i2c)

# read values from AM2320 sensor every 2 seconds
# (with gap in between temp and humidity readings)
while True:
    try:
        # Print the values to the serial port
        temp_c = dhtDevice.temperature
        time.sleep(0.5)
        hum = dhtDevice.relative_humidity
        print("AM2320 Temp: {:.1f}C Humidity: {}% ".format(temp_c,hum))

    except RuntimeError as error:
        # Errors happen fairly often, DHTs are hard to read,
        # just keep trying to run/power cycle Pico
        # If errors are persistent, increase sleep times
        # Replacing bitbangio with busio can also sometimes help
        print(error.args[0])

    time.sleep(1.5)
