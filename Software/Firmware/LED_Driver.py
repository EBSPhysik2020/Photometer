#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

class LED_Driver(object):
        def __init__(self):
                
                #Alle GPIO Pins befreien
                #GPIO.cleanup()
		
		#Pin Nummern sind nach Board Nummerierung, nicht nach CPU
                GPIO.setmode(GPIO.BCM)
                
                #Steuerpins für LED deklarieren
                self.PORT_1 = 5 # Green
                self.PORT_2 = 6 # Red
                self.PORT_3 = 13 # Blue
                
                #Setup für die Pins am Raspi
                GPIO.setup(self.PORT_1, GPIO.OUT)
                GPIO.setup(self.PORT_2, GPIO.OUT)
                GPIO.setup(self.PORT_3, GPIO.OUT)
                
                #Default alle Pins auf LOW setzen
                GPIO.output(self.PORT_1, GPIO.LOW)
                GPIO.output(self.PORT_2, GPIO.LOW)
                GPIO.output(self.PORT_3, GPIO.LOW)
        
        def setGPIOStatusValues(self, r, g, b):
                if r:
                        GPIO.output(self.PORT_2, GPIO.HIGH)
                else:
                        GPIO.output(self.PORT_2, GPIO.LOW)
                if g:
                        GPIO.output(self.PORT_1, GPIO.HIGH)
                else:
                        GPIO.output(self.PORT_1, GPIO.LOW)
                if b:
                        GPIO.output(self.PORT_3, GPIO.HIGH)
                else:
                        GPIO.output(self.PORT_3, GPIO.LOW)
        
        def setColor(self, color):
                if color == "red":
                        self.setGPIOStatusValues(1, 0, 0)
                elif color == "green":
                        self.setGPIOStatusValues(0, 1, 0)
                elif color == "blue":
                        self.setGPIOStatusValues(0, 0, 1)
                elif color == "shutoff":
                        self.setGPIOStatusValues(0, 0, 0)
                else:
                        self.setGPIOStatusValues(0, 0, 0)
