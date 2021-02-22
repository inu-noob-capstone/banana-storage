import sys
import LightControl
import measureLux
import GetIP
import GetUsername
import LightSetting
import time
import threading

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
lightSetting = LightSetting.LightSetting()

#빛의 세기 지속적으로 측정
m = measureLux.MeasureLux()
t1 = threading.Thread(target = m.measureLux, daemon = True)
t1.deamon = True
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

#최소 lux 값
main.lux = 1000

#빛 세기 값 main에서 접근해보기.
print('현재 lux :',t1.lux)

#빛 세기 측정 중단.
t1.stop_threads = True

