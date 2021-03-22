import sys
import time
import threading
import keyboard
from LightControl import *

from WaterControl import *
import RPi.GPIO as GPIO
import spidev

IP = GetIP.GetIP.findIP()
#username = GetUsername.GetUsername.GetUsername2(IP)

username = 'Z6GeaIS8gsa7TTmFurLJB3-fNrsdFMXl79oYmowb'

print('IP:',IP)
print('username:',username)
print()

#브릿지에서 전구 정보 얻어오기
lightInfo = LightControl.LightControl.getLightList(IP, username)

#전구 이름 초기화
lightname = '1'

print()
print('전구 이름 :',lightname)
print()

#빛 관련 데이터 저장을 위한 객체 생성
global lightSetting
lightSetting = LightSetting.LightSetting()

#빛 관련 정보 초기화
lightSetting.changeX(lightInfo[lightname]['state']['xy'][0])
lightSetting.changeY(lightInfo[lightname]['state']['xy'][1])
lightSetting.changeOn(lightInfo[lightname]['state']['on'])
lightSetting.changeCt(lightInfo[lightname]['state']['ct'])
lightSetting.changeBrightness(lightInfo[lightname]['state']['bri'])


#빛의 세기 측정을 위한 객체 생성
mL = measureLux.MeasureLux()

#무한 루프를 쓰는 스레드들의 종료를 위한 flag
global stop_thread
stop_thread = False

#토양 습도 측정을 위한 객체 생성
mH = measureHumidity.MeasureHumidity()

#물 관련 데이터 저장을 위한 객체 생성
global waterSetting
waterSetting = WaterSetting.WaterSetting()

#펌프 작동에 사용할 객체 생성
pump = WaterPump.WaterPump()

#빛과 습도 지속적으로 자동 측정
def autoCheck(lightSetting, mL, waterSetting, mH):
    while not stop_thread:
        print()
        lightSetting.changeCurrentLux(mL.measureLux())
        print()
        waterSetting.changeHumidity(mH.read_humidity())

t1 = threading.Thread(target=autoCheck, args=(lightSetting, mL, waterSetting, mH), daemon = True)
t1.start()

'''
#빛 세기 지속적으로 측정
def luxCheck(lightSetting, mL):
    while not stop_thread:
        print()
        lightSetting.changeCurrentLux(mL.measureLux())

t1 = threading.Thread(target=luxCheck, args=(lightSetting, mL), daemon = True)
t1.start()

#토양 습도 지속적으로 측정
def humCheck(waterSetting, mH):
    while not stop_thread:
        print()
        waterSetting.changeHumidity(mH.read_humidity())

t2 = threading.Thread(target=humCheck, args=(waterSetting, mH), daemon = True)
t2.start()
'''

#전구 기본색으로 설정. 엽록소 B 함량 중간.
commandResponse = LightControl.LightControl.changeColorTypeB(IP,username,lightname)

#전구 끈 채로 시작
commandResponse = LightControl.LightControl.lightOff(IP, username, lightname) 


#목표 lux값 설정. l 누르면 lux 값 입력 받음.
def run3(lightSetting):
    while not stop_thread:
        if keyboard.is_pressed('l'):
            goalLux = int(input('목표 lux 값 설정 :'))
            lightSetting.changeGoalLux(goalLux)
        elif keyboard.is_pressed('h'):
            humThreshold = int(input('문턱 습도 값 설정 :'))
            waterSetting.changeHumThreshold(humThreshold)
        
t3 = threading.Thread(target=run3, args=(lightSetting,), daemon=True)
t3.start()

#전구나 모터 켜고 끄는 반복적 관리 동작
while True: #f1 = open('/home/ubuntu/바탕화면/Capstone Git/LightControl','r')
    #esc 누르면 기능 종료
    if keyboard.is_pressed('esc'):
        stop_thread = True
        break
        
    #현재 lux가 부족하면 전구를 켜고, 빛 세기 증가
    if lightSetting.goalLux > lightSetting.currentLux:
        if lightSetting.on == False:
            lightSetting.on = True
            commandResponse = LightControl.LightControl.lightOn(IP, username, lightname)

        if lightSetting.bri < 254:
            if lightSetting.bri<220 and lightSetting.bri > 10:
                lightSetting.changeBrightness(int(lightSetting.bri*1.15))
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)
            else:
                lightSetting.changeBrightness(lightSetting.bri+1)
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

    #현재 lux가 과하면 빛 세기 감소 후 전구 끄기
    if lightSetting.goalLux < lightSetting.currentLux:
        if lightSetting.bri>0:
            lightSetting.changeBrightness(int(lightSetting.bri/1.08))
            commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

        if lightSetting.bri == 0 and lightSetting.on == True:
            lightSetting.on = False
            commandResponse = LightControl.LightControl.lightOff(IP, username, lightname)

    if waterSetting.humThreshold > waterSetting.humidity:
        pump.PumpOn()

    if waterSetting.humThreshold < waterSetting.humidity or waterSetting.humThreshold == waterSetting.humidity:
        pump.PumpOff()
            
GPIO.cleanup()
spi.close()
