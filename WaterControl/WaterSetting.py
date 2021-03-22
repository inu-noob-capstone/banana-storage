class WaterSetting:
    def __init__(self):
        self.adcValue = 0
        self.humidity = 0
        self.humThreshold = 0 #이거 보다 습도가 낮을 때, 모터 작동할 예정

    def trace(func):
        def wrapper(self,x):
            print("WaterSetting Changed")
            func(self,x)
        return wrapper

    @trace
    def changeAdcValue(self,adcValue):
        print("adcValue : {} -> {}" .format(self.adcValue, adcValue))
        self.adcValue = adcValue

    def changeHumidity(self, humidity):
        print("저장된 습도 : {}% -> {}%" .format(self.humidity, humidity))
        self.humidity = humidity

    def changeHumThreshold(self, humThreshold):
        print("문턱 습도 : {}% -> {}%" .format(self.humThreshold, humThreshold))
        self.humThreshold = humThreshold

        
