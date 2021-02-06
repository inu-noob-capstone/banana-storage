import LightOnAndOff
import GetIP
import GetUsername

IP = GetIP.GetIP.findIP()
username = GetUsername.GetUsername.GetUsername2(IP)

print('IP:',IP)
print('username:',username)

LightOnAndOff.LightOnAndOff.getLightList(IP, username)
