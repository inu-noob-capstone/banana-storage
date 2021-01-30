class CannotFindBridge(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.message = "SSDP를 실행하였으나, Hue Bridge를 찾지 못하였음."

    def __str__(self):
        return self.message
    
        
