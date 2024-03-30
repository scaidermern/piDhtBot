#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import adafruit_dht
import board
import json
import signal
import sys
import time

from config import gpio

# always cleanup GPIO on strg-c or kill
def signalHandler(signal, frame):
    dhtDevice.exit()
    sys.exit(0)

config = json.load(open('config.json', 'r'))
sensor = config['dht']['type']
interval = 4.0
if sensor == 'DHT11':
    dhtDevice = adafruit_dht.DHT11(gpio)
elif sensor == 'DHT22':
    dhtDevice = adafruit_dht.DHT22(gpio)
else:
    print('Error: Invalid DHT sensor type: %s' % sensor)
    sys.exit(1)

signal.signal(signal.SIGINT, signalHandler)

print('Note: Errors are expected when reading from DHT sensor, don\'t worry about them.')
lastSuccessRead = 0
while True:
    try:
        temp = dhtDevice.temperature
        hum = dhtDevice.humidity
    except RuntimeError as e:
        # errors are expected when reading from DHT
        print(e)
        time.sleep(0.2)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    if temp is None or hum is None:
        print('Read incomplete data, trying again')
        time.sleep(0.2)
        continue

    lastSuccessRead = time.time()
    print('Temperature: %.1f C, Humidity: %s%%' % (temp, hum))

    sleepSecs = interval - (time.time() - lastSuccessRead)
    if sleepSecs > 0:
        time.sleep(sleepSecs)
