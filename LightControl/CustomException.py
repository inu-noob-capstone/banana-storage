class CannotFindBridge(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = "SSDP와 N-UPnP를 이용해 찾아봤지만, Hue Bridge IP를 찾지 못하였음."

    def __str__(self):
        return self.message

class CannotGetUsername(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = "username을 얻어오지 못했습니다. Bridge의 PHILLIPS 버튼을 눌러주세요."

    def __str__(self):
        return self.message

class MeasureLuxTerminate(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = "MeasureLux 기능이 종료되었습니다."

    def __str__(self):
        return self.message

class WrongBrightnessRange(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = "0~254 범위로 brightness를 설정해 주세요."

    def __str__(self):
        return self.message

class WrongChlorophyllAmount(Exception):
    def __init(self):
        Exception.__init__(self)
        self.message = "엽록소B 함량을 잘못 입력했습니다."

    def __str__(self):
        return self.message

    
        
