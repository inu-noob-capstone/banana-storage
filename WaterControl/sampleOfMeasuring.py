import RPi.GPIO as GPIO
import time
import spidev

GPIO.setmode(GPIO.BCM)
DIGIT=23
GPIO.setup(DIGIT,GPIO.IN)
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=50000

def read_spi_adc(adcChannel):
    adcValue=0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue = ((buff[1]&3)<<8)+buff[2]
    adcValue = 1023-adcValue # without this, when wet data's 0, dry data's 1023
    adcValue = adcValue*1.45  # without this max data is around 820.
    adcValue = int(adcValue)
    if adcValue > 1023:
        adcValue = 1023
    return adcValue

try:
    while True:
        adcValue = read_spi_adc(0)
        print("토양수분:%d " % (adcValue))
        digit_val=not(GPIO.input(DIGIT))
        print("Digit Value:%d" % (digit_val))
        time.sleep(1)
finally:
        GPIO.cleanup()
        spi.close()
