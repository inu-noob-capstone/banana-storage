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
GPIO.output(A1A, GPIO.LOW)
GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1B, GPIO.LOW)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=500000

#Function to get ADC value
def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue

#Map function to convert sensor's value into percentage.
def map(value, min_adc, max_adc, min_hum, max_hum):
    adc_range = max_adc - min_adc
    hum_range = max_hum - min_hum
    scale_factor = float(adc_range) / float(hum_range)
    return min_hum + ( (value - min_adc) / scale_factor )

try:
    adcChannel = 0
    while True:
        adcValue = read_spi_adc(adcChannel)
        #converting received data into % measure.
        #The higher the humidity, The lower the value.
        #So subtract it from 100 that percentage getting more bigger when humidity up
        hum = 100 - int( map(adcValue, HUM_MAX, 1023, 0, 100) )

        if hum < HUM_THRESHOLD: # when humidity less than threshold
            GPIO.output(A1A, GPIO.HIGH) # water pump is activated
            GPIO.output(A1B, GPIO.LOW)
        else:
            GPIO.output(A1A, GPIO.LOW)
            GPIO.output(A1B, GPIO.LOW)

        time.sleep(1)

finally:
    GPIO.cleanup()
    spi.close()






