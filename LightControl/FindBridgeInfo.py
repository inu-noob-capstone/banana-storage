import socket
import CustomException

msg = \
    'M-SEARCH * HTTP/1.1\n' \
    'HOST:239.255.255.250.:1900\n' \
    'ST:upnp:rootdevice\n' \
    'MX:2\n' \
    'MAN:"ssdp:discover"\n' \
    '\n'

#Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.settimeout(2)
s.sendto(msg.encode('ascii'), ('239.255.255.250', 1900))

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
            ip = BridgeInfo[4]
            ip = ip[17:]
            ip = ip[:ip.find(':')]
            print("Bridge IP Address :",ip)
            print()
            break
        else:
            raise CustomException.CannotFindBridge
        
except socket.timeout:
    pass
