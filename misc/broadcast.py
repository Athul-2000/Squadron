import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

i = 0
while True:
    msg = f"pkt_{i}".encode()
    s.sendto(msg, ("192.168.1.255", 5000))
    print(f"sent {i}")
    i += 1
