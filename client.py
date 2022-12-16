import socket
import time
from words_structures import BNR, Time, Date, SRNS, DSC
from ins_and_sns import INS, SNS, data_of_ins, data_of_sns
from ctypes import *
from ctypes import Structure


UDP_IP = "127.0.0.1"
UDP_PORT = 12346
addr = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.connect((addr))


def packing(string_buff):
    buff = string_at(byref(string_buff), sizeof(string_buff))
    return buff


def sends(ins_or_sns, addr, list, sock):
    for i in range(0, 99):
        ins_or_sns.navig(list)
        data = packing(ins_or_sns)
        sock.sendto(data, addr)
        time.sleep(0.1)


if __name__ == '__main__':

    flag = input("1 INS \n2 SNS \n0 EXIT\n ")

    match flag:
        case "1":
            ins = INS()
            ins.contr()
            ins.prep()
            time.sleep(120)
            sends(ins, addr, data_of_ins, sock)

        case "2":
            sns = SNS()
            sns.contr()
            time.sleep(120)
            sends(sns, addr, data_of_sns, sock)

        case "0":
            sys.exit

sock.close()
