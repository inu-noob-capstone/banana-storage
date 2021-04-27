import requests
import json
from LightControl import CustomException as CustomException
#import LightControl.CustomException as CustomException
#import LightSetting
import LightControl.GetIP as GetIP

class LightControl:
    def trace(func):
        def wrapper(ip, username, *args):
            print()
            r = func(ip, username, *args)
            print()
            return r
        return wrapper

    @trace
    def getLightList(ip, username):
        URL = 'http://'+ip+'/api/'+username+'/lights'
        r = requests.get(URL)
        print('light 목록 :',r.json())
        return r.json() 

    @trace
    def lightOff(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"on":false}'
        r = requests.put(URL, data=payload)
        print('lightOff 결과 :',r.text)
        return r.text

    @trace
    def lightOn(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"on":true}'
        r = requests.put(URL, data=payload)
        print('lightOn 결과 :',r.text)
        return r.text

    @trace
    def changeXY(ip,username,lightname,x, y):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = "{}".format(x)
        y = "{}".format(y)
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeXY 결과 :',r.text)
        return r.text

    @trace
    def setColorToDefault(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        ct = '263'
        payload = '{"ct":263}'
        r = requests.put(URL, data=payload)
        print('setColorToDefault 결과 :',r.text)
        return r.text

    #@trace
    def changeColorTypeA(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.35'
        y = '0.1'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        #print('changeColorTypeA 결과 :',r.text)
        return r.text

    #@trace
    def changeColorTypeB(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.325'
        y = '0.175'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        #print('changeColorTypeB 결과 :',r.text)
        return r.text

    #@trace
    def changeColorTypeC(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.3125'
        y = '0.2125'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        #print('changeColorTypeC 결과 :',r.text)
        return r.text

    @trace
    def changeBrightness(ip,username,lightname,brightness):
        if brightness < 0 or brightness > 254:
            raise CustomException.WrongBrightness
        
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"bri":'+str(brightness)+'}'
        r = requests.put(URL, data=payload)
        print('changeBrightness 결과 :',r.text)
        return r.text

if __name__ == "__main__":
    IP = GetIP.GetIP.findIP()
    username = 'Z6GeaIS8gsa7TTmFurLJB3-fNrsdFMXl79oYmowb'
    listOfLight = LightControl.getLightList(IP,username)
    lightName = listOfLight[2]
    print('lightname:',lightName)
