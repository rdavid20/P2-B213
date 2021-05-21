import threading
import socket
import sys

pcAddr = ('192.168.137.1', 11111)
        
def relayVideo():
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.bind(('',11111))
     while True:
            data, server = s.recvfrom(1518)
            
            if(server[0] == '192.168.10.1'):
               s.sendto(data, pcAddr)

relayVideo()
