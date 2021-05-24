#이 파일의 method들은 상황에 맞추어 전구와 펌프를 작동시킨다.
#다만, 실제 동작은 다른 패키지의 모듈을 이용해서 달성한다.
#이 파일의 메소드는 해당 모듈의 기능을 호출할 뿐이다. 
#조건문을 통해 상황에 맞추어 그러한 기본 동작들을 호출하는 게, 이 파일의 목적이다. 

from LightControl import *

#현재 lux가 부족하면 전구를 켜고, 빛 세기 증가
def increaseLightIntensity(lightSetting, IP, username, lightname):
    if lightSetting.dict["allowingOfAUser"] == False:
        LightControl.LightControl.lightOff(IP, username, lightname)
        return False
    else:
        LightControl.LightControl.lightOn(IP, username, lightname)
        
        if lightSetting.dict["goalLux"] > lightSetting.dict["currentLux"]:
            if lightSetting.dict["lightStateShouldBe"] == False:
                lightSetting.dict["lightStateShouldBe"] = True
                commandResponse = LightControl.LightControl.lightOn(IP, username, lightname)
                return True

            elif lightSetting.dict["bri"] < 250:
                if (lightSetting.dict["bri"]<240 and lightSetting.dict["bri"] > 10) and ((lightSetting.dict["goalLux"]) > (lightSetting.dict["currentLux"]+10)):
                    lightSetting.changeBrightness(lightSetting.dict["bri"]+4)
                    commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.dict["bri"])
                    return True
                else:
                    lightSetting.changeBrightness(lightSetting.dict["bri"]+2)
                    commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.dict["bri"])
                    return True
        return False

#현재 lux가 과하면 빛 세기 감소 후 전구 끄기
def decreaseLightIntensity(lightSetting, IP, username, lightname):
    if lightSetting.dict["allowingOfAUser"] == False:
        LightControl.LightControl.lightOff(IP, username, lightname)
        return False
    else:
        if (lightSetting.dict["goalLux"]+10) < lightSetting.dict["currentLux"]:
            if (lightSetting.dict["bri"]>25) and (lightSetting.dict["goalLux"] < lightSetting.dict["currentLux"]):
                LightControl.LightControl.lightOn(IP, username, lightname)
                
                lightSetting.changeBrightness(lightSetting.dict["bri"]-4)
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.dict["bri"])
                return True

            elif ((lightSetting.dict["bri"]<25) and (lightSetting.dict["bri"]>1)) or lightSetting.dict["bri"]==25:
                LightControl.LightControl.lightOn(IP, username, lightname)
                
                lightSetting.changeBrightness(int(lightSetting.dict["bri"]-2))
                commandResponse = LightControl.LightControl.changeBrightness(IP,username,lightname,lightSetting.dict["bri"])
                return True

            #밝기가 최소여도 여전히 lux가 과할 때, 전구 끄기.
            elif ((lightSetting.dict["bri"] == 1) or (lightSetting.dict["bri"] < 1)) and lightSetting.dict["lightStateShouldBe"] == True:
                lightSetting.dict["lightStateShouldBe"] = False
                commandResponse = LightControl.LightControl.lightOff(IP, username, lightname)
                return True
        return False

def updateLightColor(lightSetting, IP, username, lightname):
    if lightSetting.dict["chlorophyll"] == "A":
        commandResponse = LightControl.LightControl.changeColorTypeA(IP, username, lightname)
    elif lightSetting.dict["chlorophyll"] == "B":
        commandResponse = LightControl.LightControl.changeColorTypeB(IP, username, lightname)
    elif lightSetting.dict["chlorophyll"] == "C":
        commandResponse = LightControl.LightControl.changeColorTypeC(IP, username, lightname)

#습도가 부족할 때, pump on
def pumpOnWhenLowHumidity(waterSetting, pump):
    if waterSetting.dict["allowingOfAUser"] == False:
        pump.PumpOff()
        return False
    else:
        if waterSetting.dict["humThreshold"] > waterSetting.dict["humidity"]:
            waterSetting.dict["pumpStateShouldBe"] = True
            pump.PumpOn()
            return True
        return False

#습도가 충분하며, 아직 pump가 켜진 상태일 때, pump off
def pumpOffWhenHighHumidity(waterSetting, pump):
    if waterSetting.dict["allowingOfAUser"] == False:
        pump.PumpOff()
        return False
    else:
        if (waterSetting.dict["humThreshold"] < waterSetting.dict["humidity"] or waterSetting.dict["humThreshold"] == waterSetting.dict["humidity"]) and waterSetting.dict["pumpStateShouldBe"] == True:
            waterSetting.dict["pumpStateShouldBe"] = False
            pump.PumpOff()
            return True
        return False


