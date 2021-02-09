import LightControl
import GetIP
import GetUsername
import time

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

#전구 꺼보기
commandResponse = LightControl.LightControl.lightOff(IP,username,lightname)

time.sleep(5)

#전구 켜보기
commandResponse = LightControl.LightControl.lightOn(IP,username,lightname)
