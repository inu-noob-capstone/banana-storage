import CustomException

class LightSetting:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ct = 0
        self.bri = 0
        self.goalLux = 0
        self.currentLux = 0
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

    @trace
    def changeCurrentLux(self, lux):
        print('current lux : {} -> {}'.format(self.currentLux, lux))
        self.currentLux = lux

    @trace
    def changeOn(self, on):
        print('on : {} -> {}'.format(self.on, on))
        self.on = on

    @trace
    def changeGoalLux(self, lux):
        print('goal lux : {} -> {}'.format(self.goalLux, lux))
        self.goalLux = lux

if __name__=="__main__":
    lightSetting = LightSetting()
    lightSetting.changeX(2)
    print(lightSetting.x)
