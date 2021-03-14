import RPi.GPIO as GPIO
import time
import spidev

#PIN connected with Motor Drive
A1A = 5
A1B = 6
DIGIT = 23

#Humidity threshold, in other words, Minimum Humidity %(percent).
HUM_THRESHOLD = 20

#Variable indicating How long the pump has been ON continuously.
PumpRunningSeconds = 0

#Humidity sensor output value when sensor is soaked in water.
HUM_MAX = 1023

#Initial setting of motor drive
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(DIGIT,GPIO.IN)
GPIO.setup(A1A, GPIO.OUT)
GPIO.output(A1A, GPIO.LOW)

GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1B, GPIO.LOW)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=50000

#Function to get ADC value
def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2( [1, (8+adcChannel)<<4, 0] )
    adcValue = ( (buff[1] & 3 ) << 8 ) + buff[2]
    adcValue = 1023-adcValue # without this, when wet data's 0, dry data's 1023
    adcValue = adcValue*1.45  # without this max data is around 820.
    adcValue = int(adcValue)
    if adcValue > 1023:
        adcValue = 1023
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
        print("토양 수분 : %d" % (adcValue))
        digit_val = not(GPIO.input(DIGIT))
        print("Digit Value : %d" % (digit_val))
        
        #converting received data into % measure.
        hum = int( map(adcValue, 0, HUM_MAX, 0, 100) )
        print("현재 습도(%%) : %d" % (hum))

        if hum < HUM_THRESHOLD and PumpRunningSeconds < 10: # when humidity less than threshold
            GPIO.output(A1A, GPIO.HIGH) # water pump is activated
            GPIO.output(A1B, GPIO.LOW)
            #PumpRunningSeconds += 1
        else:
            GPIO.output(A1A, GPIO.LOW)
            GPIO.output(A1B, GPIO.LOW)
            #PumpRunningSeconds = 0
            
        time.sleep(1)
finally:
    GPIO.cleanup()
    spi.close()






