import RPi.GPIO as GPIO
import time
import spidev

#PIN connected with Motor Drive
A1A = 5
A1B = 6

#Humidity threshold, in other words, Minimum Humidity %(percent).
HUM_THRESHOLD = 20

#Humidity sensor output value when sensor is soaked in water.
HUM_MAX = 100

#Initial setting of motor drive
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1A, GPIO.OUT)
