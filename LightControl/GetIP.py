import socket
import LightControl.CustomException as CustomException
import requests

class GetIP:
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

    #@staticmethod
    def findIP():
        #Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(5)
        s.sendto(GetIP.msg.encode('ascii'), ('239.255.255.250', 1900))
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
                    GetIP.ip = BridgeInfo[4]
                    GetIP.ip = GetIP.ip[17:]
                    GetIP.ip = GetIP.ip[:GetIP.ip.find(':')]
                    print("Bridge IP Address :",GetIP.ip)
                    print()
                    return GetIP.ip
                    #break
                else:
                    raise CustomException.CannotFindBridge        
        except socket.timeout:
            print('SSDP 검색 time out')
            print('N-UPnP 검색 시도')

            r = requests.get('https://discovery.meethue.com/')
            print('HTTP 상태 코드 :',r.status_code)

            if r.status_code == 200:
                locationOfInternalipaddress = r.text.find('internalipaddress')
                GetIP.ip = r.text[locationOfInternalipaddress+20:-4]

                print(r.text)
                print('N-UPnP로 찾은 ip 주소 :',GetIP.ip)
                pass
                return GetIP.ip
            else:
                raise CustomException.CannotFindBridge
                pass

if __name__=="__main__":
    GetIP.findIP()
