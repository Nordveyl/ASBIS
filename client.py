import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 12346
addr = (UDP_IP, UDP_PORT)

data = {
    "latitude": 55.811250,
    "longitude": 37.501633,
    "altitude": 4000,
    "ground speed": 620,
    "pitch": 30,
    "roll": 15
}

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.connect((addr))

massiv = list(data.values())
number_of_elements = len(massiv)

for i in range(0, 50):
    for j in range(0, number_of_elements-1):
        data = str(massiv[j]).encode('utf-8') # encode each value from dictionary
        sock.sendto(data, addr) # UDP message transmission
        time.sleep(0.1) # sending interval 0,1s = 100ms

sock.close()
