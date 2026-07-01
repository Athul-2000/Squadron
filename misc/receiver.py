import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5000))

while True:
    data, addr = s.recvfrom(2048)
    print(data.decode())
