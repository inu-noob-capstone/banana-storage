import socket
import CustomException

class BridgeIP:
    msg = \
        'M-SEARCH * HTTP/1.1\n' \
        'HOST:239.255.255.250.:1900\n' \
        'ST:upnp:rootdevice\n' \
        'MX:2\n' \
        'MAN:"ssdp:discover"\n' \
        '\n'
    ip = ""
    count = 0
    
    def __init__(self):
        pass

    def findIP(self):
        #Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(5)
        s.sendto(BridgeIP.msg.encode('ascii'), ('239.255.255.250', 1900))
        try:
            while True:
                data, addr = s.recvfrom(65507)
                data = data.decode('ascii')
                data = data.replace('\r','')
                data = data.rstrip('\n')
                #print(data)
                #if find Brdige, then save it's info
                if data.find('IpBridge') != -1:
                    print('\nIpBridge 찾음\n')
                    BridgeInfo = data
                    BridgeInfo = BridgeInfo.split('\n')
                    BridgeIP.ip = BridgeInfo[4]
                    BridgeIP.ip = BridgeIP.ip[17:]
                    BridgeIP.ip = BridgeIP.ip[:BridgeIP.ip.find(':')]
                    print("Bridge IP Address :",BridgeIP.ip)
                    print()
                    return BridgeIP.ip
                    #break
                else:
                    raise CustomException.CannotFindBridge        
        except socket.timeout:
            raise CustomException.CannotFindBridge
            pass

if __name__=="__main__":
    BridgeIP.findIP(BridgeIP)
