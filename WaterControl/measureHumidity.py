import RPi.GPIO as GPIO
import time
import spidev

class MeasureHumidity():
    def __init__(self):
        self.humidity = 0
        
        #수분 센서의 GPIO 번호
        self.DIGIT = 23

        #Humidity sensor output value when sensor is soaked in water.
        self.HUM_MAX = 1023

        #Initial setting of motor drive
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.DIGIT,GPIO.IN)

        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=50000

    #Function to get ADC value
    def read_spi_adc(self, adcChannel):
        adcValue = 0
        buff = self.spi.xfer2( [1, (8+adcChannel)<<4, 0] )
        adcValue = ( (buff[1] & 3 ) << 8 ) + buff[2]
        adcValue = 1023-adcValue # without this, when wet data's 0, dry data's 1023
        adcValue = adcValue*1.55  # without this max data is around 820.
        adcValue = int(adcValue)
        if adcValue > 1023:
            adcValue = 1023
        return adcValue

    #Map function to convert sensor's value into percentage.
    def map(self, value, min_adc, max_adc, min_hum, max_hum):
        adc_range = max_adc - min_adc
        hum_range = max_hum - min_hum
        scale_factor = float(adc_range) / float(hum_range)
        return min_hum + ( (value - min_adc) / scale_factor )

    def read_humidity(self):
        adcChannel = 0
        adcValue = self.read_spi_adc(adcChannel)
        #print("토양 수분 : %d" % (adcValue))
        digit_val = not(GPIO.input(self.DIGIT))
        #print("Digit Value : %d" % (digit_val))

        #converting received data into % measure.
        self.humidity = int(self.map(adcValue, 0, self.HUM_MAX, 0, 100))
        #print("측정된 습도 : %d%%" % (self.humidity))
        #time.sleep(0.5)
        return self.humidity

if __name__ == "__main__":
    import WaterSetting
    global waterSetting
    waterSetting = WaterSetting.WaterSetting()
    mH = MeasureHumidity()

    waterSetting.humidity = mH.read_humidity()
    print('waterSetting.lux :', waterSetting.humidity)


    

