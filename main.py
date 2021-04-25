import sys
import time
import threading
import keyboard
from LightControl import *

from WaterControl import *
import RPi.GPIO as GPIO
import spidev
import json

#브릿지의 IP 주소 알아오기.
IP = GetIP.GetIP.findIP()

#username = GetUsername.GetUsername.GetUsername2(IP)

#브릿지에게 메세지를 보낼 때 쓸 username. 일종의 계정 ID.
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
'''
#빛 관련 정보를 Dictionary로 만든 후 JSON 파일로 저장
lightDict = lightSetting.lightSettingToDict()
with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'w', encoding='utf-8') as lightFile:
    json.dump(lightDict, lightFile, indent="\t")
'''    

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

'''
#물 관련 데이터를 Dictionary로 만든 후, JSON 파일로 저장
waterDict = waterSetting.waterSettingToDict()
with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'w', encoding='utf-8') as waterFile:
    json.dump(waterDict, waterFile, indent="\t")
'''    

#펌프 작동에 사용할 객체 생성
pump = WaterPump.WaterPump()

#빛과 습도 측정하여 값을 setting에 저장하는 함수.
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


#데이터가 들어있는 setting 객체 내용을 출력하는 함수.
def printSetting(lightSetting, waterSetting, mutex, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:   
        print()
        print('현재 조도 : %dlux' % int(lightSetting.currentLux * 1.15))
        print('현재 습도 : %d%%' % waterSetting.humidity)
        print()
        #time.sleep(0.7)
    finally:
        if thread_safe:
            mutex.release()


#전구 기본색으로 설정. 엽록소 B 함량 중간.
commandResponse = LightControl.LightControl.changeColorTypeB(IP,username,lightname)

#전구 켠 채로 시작
commandResponse = LightControl.LightControl.lightOn(IP, username, lightname) 

#현재 setting들을 파일로 저장하기.
def saveSettingAsFile(lightSetting, waterSetting):
    lightDict = lightSetting.lightSettingToDict()
    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'w', encoding='utf-8') as lightFile:
        json.dump(lightDict, lightFile, indent="\t")

    waterDict = waterSetting.waterSettingToDict()
    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'w', encoding='utf-8') as waterFile:
        json.dump(waterDict, waterFile, indent="\t") 

#파일에서 정보 읽어와서 setting에 적용하기.   
def readSettingFile(lightSetting, waterSetting):
    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'r', encoding='utf-8') as lightFile:
        lightDict = json.load(lightFile)
        lightSetting.dictToLightSetting(lightDict)

    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'r', encoding='utf-8') as waterFile:
        waterDict = json.load(waterFile)
        waterSetting.dictTo(waterDict)
    

#설정 파일 변경. App에서 파일을 변경한 걸 시뮬레이션
def keyboardInput(lightSetting, mutex, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        if keyboard.is_pressed('l'):
            goalLux = int(input('목표 lux 값 설정 :'))

            lightDict = lightSetting.lightSettingToDict()
            lightDict["goalLux"] = goalLux

            with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'w', encoding='utf-8') as lightFile:
                json.dump(lightDict, lightFile, indent="\t")
            
        elif keyboard.is_pressed('h'):
            humThreshold = int(input('문턱 습도 값 설정 :'))

            waterDict = waterSetting.waterSettingToDict()
            waterDict["humThreshold"] = humThreshold

            with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'w', encoding='utf-8') as waterFile:
                json.dump(waterDict, waterFile, indent="\t")
            
        elif keyboard.is_pressed('c'):
            chlorophyll = input('엽록소B 함량을 알파벳으로 선택. A:적음, B:중간, C:많음 ::')

            lightDict = lightSetting.lightSettingToDict()
            lightDict["chlorophyll"] = chlorophyll

            with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'w', encoding='utf-8') as lightFile:
                json.dump(lightDict, lightFile, indent="\t")
    finally:
        if thread_safe:
            mutex.release()



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

    #측정된 데이터와 이전 loop에서 변경한 설정을 파일로 저장
    saveSettingAsFile(lightSetting, waterSetting)

    #측정된 데이터를 출력하는 스레드
    t4 = threading.Thread(target=printSetting, args=(lightSetting, waterSetting, mutex, thread_safe), daemon = True)
    t4.start()
    threads.append(t4)
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
