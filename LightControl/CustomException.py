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
    
        
