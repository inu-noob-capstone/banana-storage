import requests

class LightOnAndOff:
    @staticmethod
    def getLightList(ip, username):
        URL = 'http://'+ip+'/api/'+username+'/lights'
        r = requests.get(URL)
        print('light 목록 :',r.text)

        
    
