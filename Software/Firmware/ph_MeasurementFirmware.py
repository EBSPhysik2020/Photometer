#!/usr/bin/env python3

import LED_Driver
import time
import board
import busio
import adafruit_tsl2561

import socket

led_driver = LED_Driver.LED_Driver()

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TSL2561 instance, passing in the I2C bus
tsl = adafruit_tsl2561.TSL2561(i2c)

# Print chip info
print("Chip ID = {}".format(tsl.chip_id))
print("Enabled = {}".format(tsl.enabled))
print("Gain = {}".format(tsl.gain))
print("Integration time = {}".format(tsl.integration_time))

print("Configuring TSL2561...")

# Enable the light sensor
tsl.enabled = True
time.sleep(1)

# Set gain 0=1x, 1=16x
tsl.gain = 0

# Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
tsl.integration_time = 1

def getMeasureIntensity(s, measurement_type, i):
    led_driver.setColor("red")
    time.sleep(0.5)
    visibilityRed = tsl.lux
    time.sleep(0.5)
    s.sendall(('measurement-progress/'+str(measurement_type)+'/'+str(i*20+7)+'\n').encode())
    led_driver.setColor("green")
    time.sleep(0.5)
    visibilityGreen = tsl.lux
    time.sleep(0.5)
    s.sendall(('measurement-progress/'+str(measurement_type)+'/'+str(i*20+14)+'\n').encode())
    led_driver.setColor("blue")
    time.sleep(0.5)
    visibilityBlue = tsl.lux
    time.sleep(0.5)
    s.sendall(('measurement-progress/'+str(measurement_type)+'/'+str(i*20+20)+'\n').encode())
    led_driver.setColor("shutoff")

    #print("Visibility red: " + str(visibilityRed))
    #print("Visibility green: " + str(visibilityGreen))
    #print("Visibility blue: " + str(visibilityBlue))
    #print("------------")
    return [visibilityRed, visibilityGreen, visibilityBlue]

def measureIntensity(s, measurement_type):
    redIntensity = 0.0
    greenIntensity = 0.0
    blueIntensity = 0.0
    s.sendall(('measurement-progress/'+str(measurement_type)+'/0\n').encode())
    for i in range(5):
        intensities = getMeasureIntensity(s, measurement_type, i)
        redIntensity += intensities[0]
        greenIntensity += intensities[1]
        blueIntensity += intensities[2]
    redIntensity = redIntensity/5
    greenIntensity = greenIntensity/5
    blueIntensity = blueIntensity/5
    redIntensity = round(redIntensity, 3)
    greenIntensity = round(greenIntensity, 3)
    blueIntensity = round(blueIntensity, 3)
    print(redIntensity)
    print(greenIntensity)
    print(blueIntensity)
    return [redIntensity, greenIntensity, blueIntensity]
