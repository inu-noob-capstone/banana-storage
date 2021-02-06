import GetIP
import GetUsername

class UsernameAndIP:
    IP = GetIP.GetIP.findIP()
    username = GetUsername.GetUsername.GetUsername2(IP)

print('UsernameAndIP.IP :',UsernameAndIP.IP)
print('UsernameAndIP.username :',UsernameAndIP.username)


