import socket

IP_R = "0.0.0.0"
PORT_R = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_R, PORT_R))

while True:
    data, adrr = sock.recvfrom(128)
    data = data[:-2]
    print(data)