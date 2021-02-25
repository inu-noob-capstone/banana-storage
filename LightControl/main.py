import sys
import LightControl
import measureLux
import GetIP
import GetUsername
import LightSetting
import time
import threading
import continuous_threading
import CustomException

IP = GetIP.GetIP.findIP()
#username = GetUsername.GetUsername.GetUsername2(IP)

username = 'Z6GeaIS8gsa7TTmFurLJB3-fNrsdFMXl79oYmowb'

print('IP:',IP)
print('username:',username)
print()

#전구 목록 얻어오기
listOfLight = LightControl.LightControl.getLightList(IP, username)

lightname = listOfLight[2]
print()
print('전구 이름 :',lightname)
print()

#빛 관련 데이터 저장을 위한 객체 생성
global lightSetting
lightSetting = LightSetting.LightSetting()

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

#목표 lux값 설정
lightSetting.changeGoalLux(150)

while True: #f1 = open('/home/ubuntu/바탕화면/Capstone Git/LightControl','r')
    #현재 lux가 부족하면 빛 세기 증가
    if lightSetting.goalLux < lightSetting.currentLux and lightSetting.bri<254:
        lightSetting.changeBrightness(lightSetting.bri+1)
        commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.bri)
        time.sleep(0.5)

    #현재 lux가 과하면 빛 세기 감소
    if lightSetting.goalLux > lightSetting.currentLux and lightSetting.bir>0:
        lightSetting.changeBrightness(lightSetting.bri-1)
        commandResponse = LightControl.lightControl.changeBrightness(IP,username,lightname,lightSetting.bri)

#빛 세기 측정 스레드 종료
stop_thread = True
raise CustomException.MeasureLuxTerminate
'''
while True:
    print('lightSetting의 currentLux 값 :',lightSetting.currentLux)
    print()
    time.sleep(0.5)
'''
