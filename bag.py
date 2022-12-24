import numpy as np


G = 9.780327
BOLSHAYA_POLUOS = 6378136.5

class SantaClaussBag:

    def __init__(self, * init_params):
        self.params = np.array(init_params)
        self.mass = 500
        self.phi_angle = 0
        self.lamda = 0
        self.Xr = 0
        self.Yr = 0
        self.Zr = 0
        self.get_cx_table()
        self.cx_table = self.create_cx_table()

    def right_sides(self, arg):
        self.g = G * (1 + 0.0053024 * (np.sin(self.phi_angle) ** 2) - 0.0000058 * (np.sin(2 * self.phi_angle) ** 2)) - (3.686 * 10 ** (-6)) * arg[1]
        right_parts = [0] * len(arg)
        right_parts[0] = arg[2] * np.cos(arg[3])
        right_parts[1] = arg[2] * np.sin(arg[3])
        right_parts[2] = -(self.get_x(arg[1], arg[2]) + self.mass * self.g * np.sin(arg[3])) / self.mass
        right_parts[3] = -self.g * np.cos(arg[3]) / arg[2]
        return np.array(right_parts)    

    def set_blh(self, b, l, h):
        self.phi_angle = b * (np.pi / 180)
        self.lamda = l * (np.pi / 180)
        xyz = self.blh_to_xyz([b, l, h])
        self.Xr, self.Yr, self.Zr = xyz

    @staticmethod
    def blh_to_xyz(crds: list, blh: bool = False):
        b = 6356752.31424518
        if not blh:
            crds[0] *= (np.pi / 180)
            crds[1] *= (np.pi / 180)
            xyz = [0] * 3
            N = (BOLSHAYA_POLUOS ** 2) / np.sqrt((BOLSHAYA_POLUOS ** 2) * (np.cos(crds[0]) ** 2) + (b ** 2) * (np.sin(crds[0]) ** 2))
            xyz[0] = (N + crds[2]) * np.cos(crds[0]) * np.cos(crds[1])
            xyz[1] = (N + crds[2]) * np.cos(crds[0]) * np.sin(crds[1])
            xyz[2] = ((b ** 2 / BOLSHAYA_POLUOS ** 2) * N + crds[2]) * np.sin(crds[0])
            return xyz
        else:
            a2 = BOLSHAYA_POLUOS ** 2
            b2 = b ** 2
            Z2 = crds[2] ** 2
            r = np.sqrt((crds[0] ** 2) + (crds[1] ** 2))
            e12 = (a2 - b2) / a2
            e22 = (a2 - b2) / b2
            F = 54 * b2 * Z2
            G = (r ** 2) + (1 - e12) * Z2 - e12 * (a2 - b2)
            c = (e12 ** 2) * F * np.power(r, 2) / np.power(G, 3)
            s = np.power(1 + c + np.sqrt(np.power(c, 2) + 2 * c), (1 / 3))

            P = F / (3 * np.power((s + (1 / s) + 1), 2) * np.power(G, 2))
            Q = np.sqrt(1 + 2 * np.power(e12, 2) * P)
            r0 = ((-P * e12 * r) / (1 + Q)) + np.sqrt(
                0.5 * a2 * (1 + 1 / Q) - (P * (1 - e12) * Z2) / (Q * (1 + Q)) - 0.5 * P * np.power(r, 2))
            U = np.sqrt(np.power(r - e12 * r0, 2) + Z2)
            V = np.sqrt(np.power(r - e12 * r0, 2) + (1 - e12) * Z2)
            z0 = (b2 * crds[2]) / (BOLSHAYA_POLUOS * V)
            H = U * (1 - (b2 / (BOLSHAYA_POLUOS * V)))
            B = np.arctan((crds[2] + e22 * z0) / r)
            L = np.arctan2(crds[1], crds[0])
            B /= (np.pi / 180)
            L /= (np.pi / 180)
            return B, L, H

    def enu_to_xyz(self, crds: list, enu: bool = False):
        if not enu:
            dx = [0] * 3
            dx[0] = crds[0] - self.Xr
            dx[1] = crds[1] - self.Yr
            dx[2] = crds[2] - self.Zr
            enu = [0] * 3
            enu[0] = dx[0] * (-np.sin(self.lamda)) + dx[1] * np.cos(self.lamda)
            enu[1] = dx[0] * (-np.sin(self.phi_angle) * np.cos(self.lamda)) + dx[1] * (
                    -np.sin(self.phi_angle) * np.sin(self.lamda)) + dx[2] * np.cos(
                self.phi_angle)
            enu[2] = dx[0] * (np.cos(self.phi_angle) * np.cos(self.lamda)) + dx[1] * (np.cos(self.phi_angle) * np.sin(self.phi_angle)) + dx[2] * np.sin(
                self.phi_angle)
            return enu
        else:
            xyz = [0] * 3
            xyz[0] = -np.sin(self.lamda) * crds[0] - np.sin(self.phi_angle) * np.cos(self.lamda) * crds[1] + np.cos(self.phi_angle) * np.cos(self.lamda) * crds[2] + self.Xr
            xyz[1] = np.cos(self.lamda) * crds[0] - np.sin(self.phi_angle) * np.sin(self.lamda) * crds[1] + np.cos(self.phi_angle) * np.sin(self.lamda) * crds[2] + self.Yr
            xyz[2] = np.cos(self.phi_angle) * crds[1] + np.sin(self.phi_angle) * crds[2] + self.Zr
            return xyz

    def set_blh(self, b, l, h):
        self.phi_angle = b * (np.pi / 180)
        self.lamda = l * (np.pi / 180)
        xyz = self.blh_to_xyz([b, l, h])
        self.Xr, self.Yr, self.Zr = xyz

    def set_all_coord(self, enu):
        xyz = self.enu_to_xyz(enu, enu=True)
        blh = self.blh_to_xyz(xyz, blh=True)
        return xyz, blh

    @staticmethod
    def get_cx_table(m1=0.399, m2=1.25, step=0.001, out="cx_table.txt"):
        cx_table = [[0.0, 0.58], [0.4, 0.58], [0.55, 0.593], [0.65, 0.648], [0.75, 0.752], [0.8, 0.831], [0.9, 1.004],
                    [1.0, 1.178], [1.05, 1.262], [1.1, 1.325], [1.15, 1.367], [1.25, 1.403]]
        with open(out, "w+") as f:
            x = m1
            while x <= m2:
                result = 0
                for s in range(len(cx_table)):
                    p = 1
                    for i in range(len(cx_table)):
                        if i == s:
                            continue
                        p *= ((x - cx_table[i][0]) / (cx_table[s][0] - cx_table[i][0]))
                    result += p * cx_table[s][1]
                f.write(f'{x}\t{result}\n')
                x += step

    @staticmethod
    def create_cx_table(input_path="cx_table.txt"):
        cx_table = {"table": [], "delta": 0, "first_m": 0}
        with open(input_path, "r+") as r:
            while True:
                data = r.readline()
                if not data:
                    break
                cx_table["table"].append(list(map(lambda x: float(x), data.split()))[:])
            cx_table["delta"] = abs(cx_table["table"][1][0] - cx_table["table"][2][0])
            cx_table["first_m"] = cx_table["table"][1][0]
        return cx_table

    def get_cx(self, m):
        if m < 0.4:
            return 0.56
        start = np.floor((m - self.cx_table["first_m"]) / self.cx_table["delta"])
        for _, data in enumerate(self.cx_table["table"], start=int(start)):
            if abs(data[0] - m) < self.cx_table["delta"]:
                return data[0]
        return

    def get_x(self, height, velocity):
        temperature = 288.15 - 0.0065 * height
        q = (1.225 * np.power((1 - 0.00002256 * height), 4.256)) * np.power(velocity, 2) / 2
        m = velocity / (20.05 * temperature ** (1 / 2))
        return self.get_cx(m) * q * 0.5
