import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
from FileIO import readSettingFile
from FileIO import saveSettingAsFile

from LightControl import LightSetting
from WaterControl import WaterSetting
from threading import Lock

import socket, pickle
from multiprocessing import Process, Lock

#8081포트 이용
#범용

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        
        parsed_path = urlparse(self.path)
        message_parts=['query:{0:s}'.format(parsed_path.query)]

        message='<br>'.join(message_parts)
        self.send_response(200) #응답코드
        self.end_headers() #헤더가 본문을 구분
        self.wfile.write(message.encode('utf-8'))

        print(u"[START: Received GET for %s with query %s" % (self.path, parsed_path.query))
        
        global lightSetting
        lightSetting = LightSetting.LightSetting()

        global waterSetting
        waterSetting = WaterSetting.WaterSetting() 
        
        if(self.path[2:9] == "goalLux"):
            #Query문이 ?goalLux='숫자'일 때
            s = self.path
            print(parse_qs(s[2:]))
            dict_a = parse_qs(s[2:])
            
            goalLux = int(dict_a["goalLux"][0])
            print(goalLux)
            
            readSettingFile(lightSetting, waterSetting)
            lightSetting.changeGoalLux2(goalLux)

            saveSettingAsFile(lightSetting, waterSetting)

        if(self.path[2:13] == "chlorophyll"):
            #Query문이 ?chlorophyll='A'일 때
            s = self.path
            print(parse_qs(s[2:]))
            dict_a = parse_qs(s[2:])
            
            chlorophyll = dict_a["chlorophyll"][0]
            print(chlorophyll)

            readSettingFile(lightSetting, waterSetting)
            lightSetting.changeChlorophyll2(chlorophyll)

            saveSettingAsFile(lightSetting, waterSetting)

        if(self.path[2:17] == "allowingOfLight"):
            #Query문이 ?allowingOfLight=true일 때
            s = self.path
            print(parse_qs(s[2:]))
            dict_a = parse_qs(s[2:])

            allowingOfLight = (dict_a["allowingOfLight"][0]) == 'true'
            print(allowingOfLight)

            readSettingFile(lightSetting, waterSetting)
            lightSetting.changeAllowingOfAUser2(allowingOfLight)

            saveSettingAsFile(lightSetting, waterSetting)

        if(self.path[2:14] == "humThreshold"):
            #Query문이 ?humThreshold=0일 때
            s = self.path
            print(parse_qs(s[2:]))
            dict_a = parse_qs(s[2:])

            humThreshold = int(dict_a["humThreshold"][0])
            print(humThreshold)

            readSettingFile(lightSetting, waterSetting)
            waterSetting.changeHumThreshold2(humThreshold)

            saveSettingAsFile(lightSetting, waterSetting)

        if(self.path[2:16] == "allowingOfPump"):
            #Query문이 ?allowingOfPump=true일 때
            s = self.path
            print(parse_qs(s[2:]))
            dict_a = parse_qs(s[2:])

            allowingOfPump = dict_a["allowingOfPump"][0] == 'true'
            print(allowingOfPump)

            readSettingFile(lightSetting, waterSetting)
            waterSetting.changeAllowingOfAUser2(allowingOfPump)
            
            saveSettingAsFile(lightSetting, waterSetting)                    
            
        return None


s = http.server.HTTPServer(('',8081),MyHandler)
s.serve_forever()
