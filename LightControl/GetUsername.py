import FindBridgeInfo
import requests

URL = "http://"+FindBridgeInfo.ip
print(URL)
URL = URL+"/api/newdeveloper"
print(URL)

data = {'devicetype':'my_hue_app#iphone peter'}
responce = requests.get(URL)
print(responce.status_code)
print(responce.text)
