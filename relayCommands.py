ALtimport threading
import socket
import sys

host = ''
port = 8889
localaddr = (host, port)

def relayCommands():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tello_address = ('192.168.10.1', 8889)
    sock.bind(localaddr)
    while True:
        try:
            data, server = sock.recvfrom(1518)

            if (server == tello_address):
                sock.sendto(data, pc)
            else:
                pc = server
                sock.sendto(data, tello_address)
        except Exception:
            print(' . . . ')


relayCommands()