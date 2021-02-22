class LightSetting:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ct = 0
        self.bri = 0
        self.lux = 0
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
        print('bri : {} -> {}'.format(self.bri, bri))
        self.bri = bri

    @trace
    def changeLux(self, lux):
        print('lux : {} -> {}'.format(self.lux, lux))
        self.lux = lux

    @trace
    def changeOn(self, on):
        print('on : {} -> {}'.format(self.on, on))
        self.on = on

if __name__=="__main__":
    lightSetting = LightSetting()
    lightSetting.changeX(2)
    print(lightSetting.x)
