import sys
import time
import keyboard

from LightControl import *
from WaterControl import *
from FileIO import *

from methodForTest import *
from controlOfMain import *
import RPi.GPIO as GPIO

import spidev
import os

import socket, pickle

import threading

#before launch, At session(in your opening terminal), 'ulimit -n 999999'!!!!
#this program needs many file I/O


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
lightSetting.changeLightStateShouldBe(lightInfo[lightname]['state']['on'])
lightSetting.changeCt(lightInfo[lightname]['state']['ct'])
lightSetting.changeBrightness(lightInfo[lightname]['state']['bri'])

#빛의 세기 측정을 위한 객체 생성
mL = measureLux.MeasureLux()

#무한 루프를 쓰는 method들의 종료를 위한 flag
global stop_loop
stop_loop = False

#토양 습도 측정을 위한 객체 생성
mH = measureHumidity.MeasureHumidity()

#물 관련 데이터 저장을 위한 객체 생성
global waterSetting
waterSetting = WaterSetting.WaterSetting()

#펌프 작동에 사용할 객체 생성
pump = WaterPump.WaterPump()

#빛과 습도 측정하여 값을 setting에 저장하는 함수.
def autoCheck(lightSetting, mL, waterSetting, mH):  
    lightSetting.changeCurrentLux(mL.measureLux())
    waterSetting.changeHumidity(mH.read_humidity())

#초기 전구색을 중간색으로 설정. 엽록소 B 함량 중간.
commandResponse = LightControl.LightControl.changeColorTypeB(IP,username,lightname)
lightSetting.changeChlorophyll("B")

#전구 켠 채로 시작
commandResponse = LightControl.LightControl.lightOn(IP, username, lightname) 
lightSetting.changeLightStateShouldBe(True)

#최초 실행 시 setting '파일'이 존재하도록, setting '객체'의 값으로 파일 생성.
#saveSettingAsFile(lightSetting, waterSetting)    
#위 문장은 파일 없을 때만 쓰자.

#기존 파일을 설정으로 사용.
readSettingFile(lightSetting, waterSetting)

#전구나 모터 켜고 끄는 반복적 관리 동작
while True: #f1 = open('/home/ubuntu/바탕화면/Capstone Git/LightControl','r')
    #esc 누르면 기능 종료
    if keyboard.is_pressed('esc'):
        stop_loop = True
        break

    time.sleep(0.25)

    #새 목표치를 키보드로 입력 받아, 파일에'만' 쓰는 method.
    keyboardInput(lightSetting, waterSetting, keyboard)

    #파일의 목표치가 갱신됐는지 확인하기 위해, 파일을 읽어오는 method.
    #파일을 읽어와서 setting 객체를 update.
    readSettingFile(lightSetting, waterSetting)    

    #빛과 습도를 측정하여 'setting 객체에만' 저장하는 method. setting 객체 update.
    autoCheck(lightSetting, mL, waterSetting, mH)

    #새로 측정된 setting의 값으로 파일 update.
    saveSettingAsFile(lightSetting, waterSetting)

    #setting 객체의 데이터를 출력하는 method
    printSetting(lightSetting, waterSetting)
        
    #현재 lux가 부족하면 전구를 켜고, 빛 세기 증가. 그 과정에서 setting 객체 갱신.
    #increaseLightIntensity(lightSetting, IP, username, lightname)
    if increaseLightIntensity(lightSetting, IP, username, lightname):
        #setting 객체가 갱신됐을 때만, 객체를 토대로 파일도 갱신. 갱신 여부는 위의
        #조건문이 판단. increaseLightIntensity 함수는 전구 설정을 바꿨을 대 True 반환
        #이러한 조건적 파일 갱신은 파일 I/O를 최소화 하기 위해서.
        saveSettingAsFile(lightSetting, waterSetting)
    
    #현재 lux가 과하면, 빛 세기 감소 후 전구 끄기
    #decreaseLightIntensity(lightSetting, IP, username, lightname)
    #밝기가 최소여도 여전히 lux가 과할 때, 전구 끄기. 그 과정에서 setting 객체 갱신.
    if decreaseLightIntensity(lightSetting, IP, username, lightname):
        #setting 객체가 갱신됐을 때, 객체를 토대로 파일도 갱신.
        saveSettingAsFile(lightSetting, waterSetting)

    #lightSetting의 값에 따라 빛 색깔을 bridge에 요청. Setting 값은 파일에 맞추어 loop 마다 update 되는 중.
    updateLightColor(lightSetting, IP, username, lightname)
    
    #습도가 부족할 때, pump on. 그 과정에서 setting 객체 갱신.
    #pumpOnWhenLowHumidity(waterSetting, pump)
    if pumpOnWhenLowHumidity(waterSetting, pump):
        #setting 객체가 갱신됐을 때, 객체를 토대로 파일도 갱신.
        saveSettingAsFile(lightSetting, waterSetting)

    #습도가 충분하며, 아직 pump가 켜진 상태일 때, pump off. 그 과정에서 setting 객체 갱신. 
    #pumpOffWhenHighHumidity(waterSetting, pump)
    if pumpOffWhenHighHumidity(waterSetting, pump):
        #setting 객체가 갱신됐을 때, 객체를 토대로 파일도 갱신.
        saveSettingAsFile(lightSetting, waterSetting)
            
GPIO.cleanup()
spi.close()
