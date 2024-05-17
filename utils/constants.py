import netifaces

HOST = netifaces.ifaddresses('en0')[2][0]["addr"]
PORT = 9123