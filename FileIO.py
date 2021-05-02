import json

#현재 setting들을 파일로 저장하기.
def saveSettingAsFile(lightSetting, waterSetting):
    lightFile = open('/var/www/html/lightSetting.json', 'w', encoding='utf-8')
    json.dump(lightSetting.dict, lightFile, indent="\t")
    lightFile.close()

    waterFile = open('/var/www/html/waterSetting.json', 'w', encoding='utf-8')
    json.dump(waterSetting.dict, waterFile, indent="\t")
    waterFile.close()
    

#파일에서 정보 읽어와서 setting에 적용하기.   
def readSettingFile(lightSetting, waterSetting):
    lightFile = open('/var/www/html/lightSetting.json', 'r', encoding='UTF-8')
    lightSetting.dict = json.load(lightFile)
    lightFile.close()

    waterFile = open('/var/www/html/waterSetting.json', 'r', encoding='UTF-8')
    waterSetting.dict = json.load(waterFile)
    waterFile.close()
    
