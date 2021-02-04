from FindBridgeInfo.__init__ import ip
import requests

print("Username 얻어오기")
print()

URL = "http://"+ip
URL = URL+"/api/"
print('메시지 목적지 : ', URL)

payload = {'devicetype':'my_hue_app#iphone peter'}
response = requests.post(URL, json=payload)

print('브릿지에 보낸 메시지 : ', payload)
#print('돌아온 응답 코드 : 'responce.status_code)
print('돌아온 Command Response : ', response.text)

if response.text.find('error\":{\"type\":101') != -1:
    print('브릿지로 가서 원형의 PHILLIPS 버튼을 눌러주세요. 보안을 위해서 필요한 조치입니다.')
    
if response.text.find('username') != -1:
    locationOfUsername = response.text.find('username')
    print(locationOfUsername)
    locationOfUsername += 11
    print(locationOfUsername)
    locationOfUsername=response.text.find("\"",locationOfUsername,)
    print(locationOfUsername)
    
    #print(response.text[locationOfUsername:
    
