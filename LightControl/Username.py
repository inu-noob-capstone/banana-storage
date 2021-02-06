import GetIP
import requests
import sys

class Username:
    username=''

    def GetUsername(self):
        print()
        print("Username 얻어오기")

        IP = GetIP.BridgeIP()
        ip = IP.findIP()

        if ip==None:
            sys.exit()

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
            #print('\'username\'의 시작 위치 :',locationOfUsername)
            #print('\'username\' 출력 시도 :', response.text[locationOfUsername:locationOfUsername+8])
            locationOfUsername += 11
            #print('username 내용의 시작 위치 :',locationOfUsername)
            #print('username 내용 출력 시도 :', response.text[locationOfUsername:-4])
            username = response.text[locationOfUsername:-4]
            print()
            print('username :',username)    

if __name__ == "__main__":
    Username.GetUsername(Username)

if __name__== "Username": 
    Username.GetUsername(Username)
