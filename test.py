from ipwhois import IPWhois
import socket
dd = socket.gethostbyname('www.ecoledirecte.com')
obj = IPWhois(dd)
res = obj.lookup()
print(res["nets"][0]['country'])
