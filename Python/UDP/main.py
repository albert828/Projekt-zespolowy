import socket
import time

UDP_IP = "192.168.137.186"
UDP_PORT = 4210
IP_R = "127.0.0.1"
PORT_R = 5005
MESSAGE = "abc"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.bind(('', PORT_R))

#sock = UDP.MulticastListener(UDP_IP,UDP_PORT)
while True:
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    data, adrr = sock1.recvfrom(128)
    print(data)
    time.sleep(1)