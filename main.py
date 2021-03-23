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
def autoCheck(lightSetting, mL, waterSetting, mH, mutex, thread_safe):  
    if thread_safe:
        mutex.acquire()
    try:
        #print()
        lightSetting.changeCurrentLux(mL.measureLux())
        #print()
        waterSetting.changeHumidity(mH.read_humidity())
    finally:
        if thread_safe:
            mutex.release()

'''
t1 = threading.Thread(target=autoCheck, args=(lightSetting, mL, waterSetting, mH), daemon = True)
t1.start()
'''

def printSetting(lightSetting, waterSetting, mutex, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:   
        print()
        print('현재 조도 : %dlux' % int(lightSetting.currentLux * 1.15))
        print('현재 습도 : %d%%' % waterSetting.humidity)
        print()
        time.sleep(0.7)
    finally:
        if thread_safe:
            mutex.release()

'''
t2 = threading.Thread(target=printSetting, args=(lightSetting, waterSetting), daemon = True)
t2.start()
'''


#전구 기본색으로 설정. 엽록소 B 함량 중간.
commandResponse = LightControl.LightControl.changeColorTypeB(IP,username,lightname)

#전구 켠 채로 시작
commandResponse = LightControl.LightControl.lightOn(IP, username, lightname) 


#목표 lux값 설정. l 누르면 lux 값 입력 받음.
def keyboardInput(lightSetting, mutex, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        if keyboard.is_pressed('l'):
            goalLux = int(input('목표 lux 값 설정 :'))
            lightSetting.changeGoalLux(goalLux)
        elif keyboard.is_pressed('h'):
            humThreshold = int(input('문턱 습도 값 설정 :'))
            waterSetting.changeHumThreshold(humThreshold)
    finally:
        if thread_safe:
            mutex.release()


'''        
t3 = threading.Thread(target=run3, args=(lightSetting,), daemon=True)
t3.start()
'''


#전구나 모터 켜고 끄는 반복적 관리 동작
while True: #f1 = open('/home/ubuntu/바탕화면/Capstone Git/LightControl','r')
    #esc 누르면 기능 종료
    if keyboard.is_pressed('esc'):
        stop_thread = True
        break

    threads = []
    thread_safe = True
    mutex = threading.Lock() #상호배제에 사용할 lock

    #esc를 제외한 키보드 입력 받는 스레드
    t1 = threading.Thread(target=keyboardInput, args=(lightSetting, mutex, thread_safe), daemon=True)
    t1.start()
    threads.append(t1)

    #빛과 습도를 측정하는 스레드
    t2 = threading.Thread(target=autoCheck, args=(lightSetting, mL, waterSetting, mH, mutex, thread_safe), daemon = True)
    t2.start()
    threads.append(t2)
    #autoCheck(lightSetting, mL, waterSetting, mH)

    #측정된 데이터를 출력하는 스레드
    t3 = threading.Thread(target=printSetting, args=(lightSetting, waterSetting, mutex, thread_safe), daemon = True)
    t3.start()
    threads.append(t3)
    #printSetting(lightSetting, waterSetting)

    #앞에 생성된 스레드 종료 대기.
    for tn in threads:
        tn.join()
        
    #현재 lux가 부족하면 전구를 켜고, 빛 세기 증가
    if lightSetting.goalLux > lightSetting.currentLux:
        if lightSetting.on == False:
            lightSetting.on = True
            commandResponse = LightControl.LightControl.lightOn(IP, username, lightname)

        elif lightSetting.bri < 254:
            if (lightSetting.bri<220 and lightSetting.bri > 10) and ((lightSetting.goalLux) > (lightSetting.currentLux+10)):
                lightSetting.changeBrightness(int(lightSetting.bri*1.1))
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)
            else:
                lightSetting.changeBrightness(lightSetting.bri+1)
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

    #현재 lux가 과하면 빛 세기 감소 후 전구 끄기
    if (lightSetting.goalLux+15) < lightSetting.currentLux:
        if (lightSetting.bri>25) and (lightSetting.goalLux < lightSetting.currentLux):
            lightSetting.changeBrightness(int(lightSetting.bri*0.9))
            commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

        elif ((lightSetting.bri<25) and (lightSetting.bri>1)) or lightSetting.bri==25:
            lightSetting.changeBrightness(int(lightSetting.bri-1))
            commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

        #밝기가 최소여도 여전히 lux가 과할 때, 전구 끄기.
        elif ((lightSetting.bri == 1) or (lightSetting.bri < 1)) and lightSetting.on == True:
        #elif lightSetting.on == True:
            lightSetting.on = False
            commandResponse = LightControl.LightControl.lightOff(IP, username, lightname)

    #습도가 부족할 때, pump on
    if waterSetting.humThreshold > waterSetting.humidity:
        waterSetting.on = True
        pump.PumpOn()

    #습도가 충분하며, 아직 pump가 켜진 상태일 때, pump off
    if (waterSetting.humThreshold < waterSetting.humidity or waterSetting.humThreshold == waterSetting.humidity) and waterSetting.on == True:
        waterSetting.on = False
        pump.PumpOff()
            
GPIO.cleanup()
spi.close()
