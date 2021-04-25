#import CustomException __main 할 때 
import LightControl.CustomException as CustomException
import json

class LightSetting:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ct = 0
        self.bri = 0
        self.goalLux = 0
        self.currentLux = 0
        self.chlorophyll= "B"
        self.on = False

    def trace(func):
        def wrapper(self,x):
            print('LightSetting Changed')
            func(self,x)
        return wrapper

    @trace
    def changeX(self,x):
        print('x : {} -> {}'.format(self.x, x))
        self.x = x

    @trace
    def changeY(self,y):
        print('y : {} -> {}'.format(self.y, y))
        self.y = y

    @trace
    def changeCt(self,ct):
        print('ct : {} -> {}'.format(self.ct,ct))
        self.ct = ct

    @trace
    def changeBrightness(self, bri):
        if bri<0:
            raise CustomException.WrongBrightnessRange
            return
        elif bri>254:
            raise CustomException.WrongBrightnessRange
            return
        print('bri : {} -> {}'.format(self.bri, bri))
        self.bri = bri

    def changeCurrentLux(self, lux):
        #print('저장된 조도 : %.2f lux -> %.2f lux' % (self.currentLux, lux))
        self.currentLux = lux

    @trace
    def changeOn(self, on):
        print('on : {} -> {}'.format(self.on, on))
        self.on = on

    def changeGoalLux(self, lux):
        print()
        print('goal lux : {} -> {}'.format(self.goalLux, lux))
        self.goalLux = lux

    def changeChlorophyll(self, chlorophyll):
        if chlorophyll == "A" or chlorophyll == "B" or chlorophyll == "C":
            print('chlorophyll : {} -> {}'.format(self.chlorophyll, chlorophyll))
            self.chlorophyll = chlorophyll
        else:
            raise CustomException.WrongChlorophyll

    def lightSettingToDict(self):
        lightSettingByDictionary = dict()

        lightSettingByDictionary["x"] = self.x
        lightSettingByDictionary["y"] = self.y
        lightSettingByDictionary["ct"] = self.ct

        lightSettingByDictionary["bri"] = self.bri
        lightSettingByDictionary["goalLux"] = self.goalLux
        lightSettingByDictionary["currentLux"] = self.currentLux

        lightSettingByDictionary["chlorophyll"] = self.chlorophyll
        lightSettingByDictionary["on"] = self.on

        return lightSettingByDictionary

    def dictToLightSetting(self, dictionary):
        self.x = dictionary["x"]
        self.y = dictionary["y"]
        self.ct = dictionary["ct"]

        self.bri = dictionary["bri"]
        
        self.changeGoalLux(dictionary["goalLux"])
        
        self.currentLux = dictionary["currentLux"]
        
        self.changeChlorophyll(dictionary["chlorophyll"])
        
        self.on = dictionary["on"]
        

if __name__=="__main__":
    lightSetting = LightSetting()
    dict = lightSetting.lightSettingToDict()

    print(dict)
