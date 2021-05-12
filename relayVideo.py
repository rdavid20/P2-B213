import threading
import socket
import sys
        
def relayVideo():
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.bind(('',11111))
     while True:
            data, server = s.recvfrom(1518)
            s.sendto(data, ('192.168.0.144', 11111))


videoThread = threading.Thread(target=relayVideo())
videoThread.start()
