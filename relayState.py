import threading
import socket
import sys

def relayState():
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.bind(('', 8890))
    while True:
            data, server = s2.recvfrom(1518)
            s2.sendto(data, ('192.168.0.144', 8890))

stateThread = threading.Thread(target=relayState())
stateThread.start()