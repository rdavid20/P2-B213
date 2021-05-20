import threading
import socket
import sys

pcAddr = ('192.168.137.1', 8890)

def relayState():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 8890))
    while True:
            data, server = s.recvfrom(1518)
            s.sendto(data, pcAddr)

relayState()

