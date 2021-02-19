import LightControl
import measureLux
import GetIP
import GetUsername
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

#빛의 세기 지속적으로 측정
t1 = threading.Thread(target=measureLux.measureLux, daemon = True)
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
