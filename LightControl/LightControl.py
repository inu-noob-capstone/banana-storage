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
        
    def changeXY(x, y):
        URL = 'http://'+ip+'/api/'+username+'/lights/'+lightname+'/state'
        payload = '{"xy":['+x+','+y+']}'
        r = requests.put(URL, data=payload)
        print('changeXYf 결과 :',r.text)
        return r.text        

    

        
    
