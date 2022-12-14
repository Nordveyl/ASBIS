import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 12346
addr = (UDP_IP, UDP_PORT)

server = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
server.bind((addr)) # binds the address and port to the socket

while True:
    data = float(server.recv(1024).decode('utf-8')) # buffer size is 1024 bytes and decode from utf-8
    print(data)

server.close()
