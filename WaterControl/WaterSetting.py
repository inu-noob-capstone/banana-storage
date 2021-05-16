class WaterSetting:
    def __init__(self):
        self.dict = {
            "adcValue" : 0,
            "humidity" : 0,
            "humThreshold" : 0, #이거 보다 습도가 낮을 때, 모터 작동할 예정
            "pumpStateShouldBe" : False, #allowing 상태일 때, 이게 True면 pump가 작동한다.
            "allowingOfAUser" : True
            }

    def trace(func):
        def wrapper(self,x):
            print("WaterSetting Changed")
            func(self,x)
        return wrapper

    @trace
    def changeAdcValue(self,adcValue):
        print("adcValue : {} -> {}" .format(self.dict["adcValue"], adcValue))
        self.dict["adcValue"] = adcValue

    def changeHumidity(self, humidity):
        print("humidity : {} -> {}" .format(self.dict["humidity"], humidity))
        self.dict["humidity"] = humidity

    def changeHumThreshold(self, humThreshold):
        print("문턱 습도 : {}% -> {}%" .format(self.dict["humThreshold"], humThreshold))
        self.dict["humThreshold"] = humThreshold

    def changeHumThreshold2(self, humThreshold):
        print(u"문턱 습도 : {}% -> {}%" .format(self.dict["humThreshold"], humThreshold))
        self.dict["humThreshold"] = humThreshold

    def changeAllowingOfAUser(self, allowingOfAUser):
        print("allowingOfAUser : {} -> {}" .format(self.dict["allowingOfAUser"],
                                                   allowingOfAUser))
        self.dict["allowingOfAUser"] = allowingOfAUser

    def changeAllowingOfAUser2(self, allowingOfAUser):
        print(u"allowingOfAUser : {} -> {}" .format(self.dict["allowingOfAUser"],
                                                   allowingOfAUser))
        self.dict["allowingOfAUser"] = allowingOfAUser
              

        
