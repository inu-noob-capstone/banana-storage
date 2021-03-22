import RPi.GPIO as GPIO
import time
import spidev

class WaterPump():
    def __init__(self):

        #모터드라이브와 연결된 PIN 번호
        self.A1A = 5
        self.A1B = 6

        #습도 문턱값(%), 이것보다 측정 습도가 낮을 때, 펌프 ON 
        self.HUM_THRESHOLD = 0

        #모터드라이브 초기 설정
        GPIO.setup(self.A1A, GPIO.OUT)
        GPIO.output(self.A1A, GPIO.LOW)

        GPIO.setup(self.A1B, GPIO.OUT)
        GPIO.output(self.A1B, GPIO.LOW)

        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz=50000

    def PumpOn(self):
        GPIO.output(self.A1A, GPIO.HIGH)
        GPIO.output(self.A1B, GPIO.LOW)
        print("Pump On")

    def PumpOff(self):
        GPIO.output(self.A1A, GPIO.LOW)
        GPIO.output(self.A1B, GPIO.LOW)
        print("Pump Off")

        
