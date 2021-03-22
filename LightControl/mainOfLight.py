import sys
import LightControl
import measureLux
import GetIP
import GetUsername
import LightSetting
import time
import threading
import keyboard
import CustomException

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
m = measureLux.MeasureLux()

#빛 세기를 지속 측정 시, 무한 루프 탈출을 위한 flag
global stop_thread
stop_thread = False

#빛 세기 지속적으로 측정
def run(lightSetting, m):
    while not stop_thread:
        print()
        lightSetting.changeCurrentLux(m.measureLux())

t1 = threading.Thread(target=run, args=(lightSetting, m), daemon = True)
t1.start()

#전구 기본색으로 설정
commandResponse = LightControl.LightControl.setColorToDefault(IP,username,lightname)
time.sleep(5)

#전구 꺼보기
commandResponse = LightControl.LightControl.lightOff(IP,username,lightname)

time.sleep(5)

#전구 켜보기
commandResponse = LightControl.LightControl.lightOn(IP,username,lightname)

time.sleep(5)

#전구 색 변화
commandResponse = LightControl.LightControl.changeColorTypeA(IP,username,lightname)

time.sleep(5)

commandResponse = LightControl.LightControl.changeColorTypeB(IP,username,lightname)

time.sleep(5)

commandResponse = LightControl.LightControl.changeColorTypeC(IP,username,lightname)

#목표 lux값 설정. i 누르면 lux 값 입력 받음.
def run2(lightSetting):
    while not stop_thread:
        if keyboard.is_pressed('i'):
            goalLux = int(input('목표 lux 값 설정 :'))
            lightSetting.changeGoalLux(goalLux)
        
t2 = threading.Thread(target=run2, args=(lightSetting,), daemon=True)
t2.start()

while True: #f1 = open('/home/ubuntu/바탕화면/Capstone Git/LightControl','r')
    #esc 누르면 기능 종료
    if keyboard.is_pressed('esc'):
        stop_thread = True
        break
        
    #현재 lux가 부족하면 빛 세기 증가
    if lightSetting.goalLux > lightSetting.currentLux and lightSetting.bri<254:
        if lightSetting.bri<220 and lightSetting.bri > 10:
            lightSetting.changeBrightness(int(lightSetting.bri*1.15))
            commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)
        else:
            lightSetting.changeBrightness(lightSetting.bri+1)
            commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

    #현재 lux가 과하면 빛 세기 감소
    if lightSetting.goalLux < lightSetting.currentLux and lightSetting.bri>0:
        lightSetting.changeBrightness(int(lightSetting.bri/1.08))
        commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)        

'''
while True:
    print('lightSetting의 currentLux 값 :',lightSetting.currentLux)
    print()
    time.sleep(0.5)
    
#빛 세기 측정 스레드 종료
stop_thread = True
raise CustomException.MeasureLuxTerminate

'''
