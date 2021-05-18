#import CustomException __main 할 때 
import LightControl.CustomException as CustomException
import json

class LightSetting:
    def __init__(self):
        self.dict = {
            "x" : 0,
            "y" : 0,
            "ct" : 0,
            "bri" : 0,
            "goalLux" : 0,
            "currentLux" : 0,
            "chlorophyll" : 0,
            "lightStateShouldBe" : False,
            "allowingOfAUser" : True
            }

    def trace(func):
        def wrapper(self,x):
            print('LightSetting Changed')
            func(self,x)
        return wrapper

    @trace
    def changeX(self,x):
        print('x : {} -> {}'.format(self.dict["x"], x))
        self.dict["x"] = x

    @trace
    def changeY(self,y):
        print('y : {} -> {}'.format(self.dict["y"], y))
        self.dict["y"] = y

    @trace
    def changeCt(self,ct):
        print('ct : {} -> {}'.format(self.dict["ct"],ct))
        self.dict["ct"] = ct

    @trace
    def changeBrightness(self, bri):
        if bri<0:
            raise CustomException.WrongBrightnessRange
            return
        elif bri>254:
            raise CustomException.WrongBrightnessRange
            return
        print('bri : {} -> {}'.format(self.dict["bri"], bri))
        self.dict["bri"] = bri

    def changeCurrentLux(self, lux):
        print("currentLux : {} -> {}" .format(self.dict["currentLux"], lux))
        self.dict["currentLux"] = lux

    @trace
    def changeLightStateShouldBe(self, lightStateShouldBe):
        print('lightStateShouldBe : {} -> {}'.format(self.dict["lightStateShouldBe"], lightStateShouldBe))
        self.dict["lightStateShouldBe"] = lightStateShouldBe

    def changeGoalLux(self, lux):
        print()
        print('goalLux : {} -> {}'.format(self.dict["goalLux"], lux))
        self.dict["goalLux"] = lux

    def changeGoalLux2(self, lux):
        print(u'goalLux : {} -> {}'.format(self.dict["goalLux"], lux))
        self.dict["goalLux"] = lux

    def changeGoalLux3(self, lux):
        print(u'retry goalLux : {} -> {}'.format(self.dict["goalLux"], lux))
        self.dict["goalLux"] = lux

    def changeChlorophyll(self, chlorophyll):
        if chlorophyll == "A" or chlorophyll == "B" or chlorophyll == "C":
            print('chlorophyll : {} -> {}'.format(self.dict["chlorophyll"], chlorophyll))
            self.dict["chlorophyll"] = chlorophyll
        else:
            raise CustomException.WrongChlorophyll

    def changeChlorophyll2(self, chlorophyll):
        print(u'chlorophyll : {} -> {}'.format(self.dict["chlorophyll"], chlorophyll))
        self.dict["chlorophyll"] = chlorophyll

    def changeChlorophyll3(self, chlorophyll):
        print(u'retry chlorophyll : {} -> {}'.format(self.dict["chlorophyll"], chlorophyll))
        self.dict["chlorophyll"] = chlorophyll

    def changeAllowingOfAUser(self, allowingOfAUser):
        print()
        print('allowingOfAUser : {} -> {}'.format(self.dict["allowingOfAUser"], allowingOfAUser))
        self.dict["allowingOfAUser"] = allowingOfAUser

    def changeAllowingOfAUser2(self, allowingOfAUser):
        print(u'allowingOfAUser : {} -> {}'.format(self.dict["allowingOfAUser"], allowingOfAUser))
        self.dict["allowingOfAUser"] = allowingOfAUser

    def changeAllowingOfAUser3(self, allowingOfAUser):
        print(u'retry allowingOfAUser : {} -> {}'.format(self.dict["allowingOfAUser"], allowingOfAUser))
        self.dict["allowingOfAUser"] = allowingOfAUser

if __name__=="__main__":
    lightSetting = LightSetting()
    dict = lightSetting.lightSettingToDict()

    print(dict)
