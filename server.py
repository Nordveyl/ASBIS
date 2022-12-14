import socket
from ins_and_sns import INS, SNS
from ctypes import *


UDP_IP = "127.0.0.1"
UDP_PORT = 12346
addr = (UDP_IP, UDP_PORT)

server = socket.socket(socket.AF_INET, # Internet
                       socket.SOCK_DGRAM) # UDP
server.bind((addr)) # binds the address and port to the socket

def decode(value, n_bit, senior_bit):
    return senior_bit * value / 2 ** (n_bit - 1)

def unpacking(type, buffer):
    buff = create_string_buffer(buffer)
    buff_real = cast(pointer(buff), POINTER(type)).contents
    return buff_real

while True:
    data = server.recv(1024)

    if len(data) == 52:
        data_length = unpacking(INS, data)
        print(len(data))
        print(decode(data_length.latitude.value, 20, 90))

    elif len(data) == 56:
        data_length = unpacking(SNS, data)
        print(len(data))
        print(decode(data_length.L.value, 20, 90))

server.close()
