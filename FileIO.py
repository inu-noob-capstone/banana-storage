import json

#현재 setting들을 파일로 저장하기.
def saveSettingAsFile(lightSetting, waterSetting):
    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'w', encoding='utf-8') as lightFile:
        json.dump(lightSetting.dict, lightFile, indent="\t")

    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'w', encoding='utf-8') as waterFile:
        json.dump(waterSetting.dict, waterFile, indent="\t") 

#파일에서 정보 읽어와서 setting에 적용하기.   
def readSettingFile(lightSetting, waterSetting):
    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/lightSetting.json', 'r', encoding='UTF-8') as lightFile:
        lightSetting.dict = json.load(lightFile)

    with open('/root/Desktop/Capstone Design/banana-storage/ServerFiles/waterSetting.json', 'r', encoding='UTF-8') as waterFile:
        waterSetting.dict = json.load(waterFile)
