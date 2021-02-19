import requests
import json

class LightControl:
    @staticmethod
    def getLightList(ip, username):
        URL = 'http://'+ip+'/api/'+username+'/lights'
        r = requests.get(URL)
        print('light 목록 :',r.json())
        return r.text 

    @staticmethod
    def lightOff(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"on":false}'
        r = requests.put(URL, data=payload)
        print('lightOff 결과 :',r.text)
        return r.text

    def lightOn(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"on":true}'
        r = requests.put(URL, data=payload)
        print('lightOn 결과 :',r.text)
        return r.text
        
    def changeXY(ip,username,lightname,x, y):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = "{}".format(x)
        y = "{}".format(y)
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeXY 결과 :',r.text)
        return r.text

    def setColorToDefault(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        ct = '263'
        payload = '{"ct":263}'
        r = requests.put(URL, data=payload)
        print('setColorToDefault 결과 :',r.text)
        return r.text

    def changeColorTypeA(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.35'
        y = '0.1'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeColorTypeA 결과 :',r.text)
        return r.text

    def changeColorTypeB(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.325'
        y = '0.175'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeColorTypeB 결과 :',r.text)
        return r.text

    def changeColorTypeC(ip,username,lightname):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        x = '0.3125'
        y = '0.2125'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeColorTypeC 결과 :',r.text)
        return r.text

        
    
