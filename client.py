import socket
import time
import copy
from ctypes import *
from airplane import Airplane
from pid_controller import PID_controller
from ins_and_sns import INS, SNS, data_of_ins, data_of_sns
from kml import KML as kml

UDP_IP = "127.0.0.1"
UDP_PORT = 12346
addr = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.connect((addr))


def packing(string_buff):
    buff = string_at(byref(string_buff), sizeof(string_buff))
    return buff


def runge_cutta_4_poryadka(obj, h):  # Метод Рунге-Кутта 4-го порядка
    k1 = obj.right_sides(obj.params)
    k2 = obj.right_sides(obj.params + h * k1 / 2)
    k3 = obj.right_sides(obj.params + h * k2 / 2)
    k4 = obj.right_sides(obj.params + h * k3)
    obj.params += (k1 + 2 * k2 + 2 * k3 + k4) * h / 6


def sends(ins_or_sns, addr, sock, coord, h_pid, v_pid, k_pid, obj, h, flag):
    i = 1
    massiv_of_coord = []
    massiv_of_coord.append(coord[0])
    start = 0
    while i < len(coord):
        finish = time.time()
        xyz, blh = obj.set_all_coord([obj.params[2], obj.params[0], obj.params[1]])
        a12, d = obj.azimut_and_d(blh[0], coord[i][1], blh[1], coord[i][0])
        massiv_of_coord.append([blh[1], blh[0], 0])
        if d <= 50:
            print("reached the point!")
            print(coord[i][1], coord[i][0])
            massiv_of_coord.append([blh[1], blh[0], 0])
            i += 1
            continue
        du = v_pid.evaluation(h, obj.params[3], 250)
        da = h_pid.evaluation(h, obj.params[1], 10000)
        dy = k_pid.evaluation(h, obj.params[5], a12)
        obj.u = [du, da, 0, dy]
        runge_cutta_4_poryadka(obj, h)
        if finish - start > 0.1:
            if flag == "1":
                copy_data_ins["latitude"]["value"] = blh[0]
                copy_data_ins["longitude"]["value"] = blh[1]
                copy_data_ins["altitude"]["value"] = blh[2]
                ins_or_sns.navig(copy_data_ins)
            else:
                copy_data_sns["B"]["value"] = blh[0]
                copy_data_sns["L"]["value"] = blh[1]
                copy_data_ins["altitude"]["value"] = blh[2]
                ins_or_sns.navig(copy_data_sns)
            data = packing(ins_or_sns)
            sock.sendto(data, addr)
            start = time.time()
            print(d)
    return massiv_of_coord


file_1 = "mojaysk_vlasiha_vzakat.kml"
file_2 = 'marshrut.kml'
coordinates = kml.take_coordinates_from_kml_file(file_1)

plane = Airplane(0.0, 10000.0, 0.0, 250.0, 0.0, 0.0)
copy_data_ins = copy.deepcopy(data_of_ins)
copy_data_sns = copy.deepcopy(data_of_sns)
plane.set_blh(coordinates[0][1], coordinates[0][0], 0)
plane.set_all_coord([plane.params[2], plane.params[0], plane.params[1]])
plane.u = [85500.0, 0.0, 0.0, 0.0]
h = 0.01

h_pid = PID_controller(0.0019, 0.0002, 0.1)
v_pid = PID_controller(15500.0, 3000.0, .0)
k_pid = PID_controller(5.0, 0.5, 0.9)

if __name__ == '__main__':

    flag = input("1 INS \n2 SNS \n0 EXIT\n ")

    match flag:
        case "1":
            ins = INS()
            ins.contr()
            ins.prep()
            time.sleep(120)
            massiv_of_coord = sends(ins, addr, sock, coordinates, h_pid, v_pid, k_pid, plane, h, flag)

        case "2":
            sns = SNS()
            sns.contr()
            time.sleep(120)
            massiv_of_coord = sends(sns, addr, sock, coordinates, h_pid, v_pid, k_pid, plane, h, flag)

        case "0":
            sys.exit

sock.close()
kml.write_coordinates_to_kml_file(massiv_of_coord, file_2)

