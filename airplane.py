import numpy as np

BOLSHAYA_POLUOS = 6378136.5
SJATIE = 1 / 298.25784
EKSCENTRISITET = 0.0066934216
G = 9.780327

class Airplane:

    def __init__(self, * init_params):
        self.params = np.array(init_params)
        self.mass = 17770
        self.phi_angle = 0
        self.lamda = 0
        self.Xr = 0
        self.Yr = 0
        self.Zr = 0
        self.u = [0, 0, 0, 0]

    def right_sides(self, init_params):
        sq = 110.3
        right_sides = [0] * len(init_params)
        g = G * (1 + 0.0053024 * (np.sin(self.phi_angle) ** 2) - 0.0000058 * (np.sin(2 * self.phi_angle) ** 2)) - (3.686 * 10 ** (-6)) * init_params[1] #Вычисление ускорения свободного падения
        ro = 1.225 * (1 - 0.00002256 * init_params[1]) ** 4.256
        cy = self.get_cy(init_params[1], init_params[3], self.u[1])
        cx = self.get_cx(init_params[1], init_params[3], self.u[1], cy)
        x = cx * ro * (init_params[3] ** 2) * sq / 2
        y = cy * ro * (init_params[3] ** 2) * sq / 2
        z = (0.28 * (0.8 * 18.3 * 4 / sq) * self.u[2]) * 0.5 * (init_params[3] ** 2) *  ro * sq + 1.64 * self.u[2] * 3 * 0.5 * (init_params[3] ** 2) * ro
        right_sides[0] = init_params[3] * np.cos(init_params[4]) * np.cos(init_params[5])
        right_sides[1] = init_params[3] * np.sin(init_params[4])
        right_sides[2] = init_params[3] * np.cos(init_params[4]) * np.sin(init_params[5])
        right_sides[3] = (self.u[0] * np.cos(self.u[1]) * np.cos(self.u[2]) - x - self.mass * g * np.sin(init_params[4])) / self.mass
        right_sides[4] = ((self.u[0] * np.sin(self.u[1]) + y) * np.cos(self.u[3]) - (z - self.u[0] * np.cos(self.u[1]) * np.sin(self.u[2])) * np.sin(self.u[3]) - self.mass *g * np.cos(init_params[4])) / (self.mass * init_params[3])
        right_sides[5] = ((self.u[0] * np.sin(self.u[1]) + y) * np.sin(self.u[3]) + (z - self.u[0] * np.cos(self.u[1]) * np.sin(self.u[2])) * np.cos(self.u[3])) / (self.mass * init_params[3] * np.cos(init_params[4]))
        return np.array(right_sides)

    @staticmethod
    def azimut_and_d(phi_angle_1, phi_angle_2, lamd1, lamd2):
        phi_angle_1 = np.pi * phi_angle_1 / 180
        phi_angle_2 = np.pi * phi_angle_2 / 180
        sin_1 = np.sin(phi_angle_1) * np.sqrt(1 - EKSCENTRISITET ) / np.sqrt(1 - EKSCENTRISITET  * np.sin(phi_angle_1) ** 2)
        cos_1 = np.cos(phi_angle_1) / np.sqrt(1 - EKSCENTRISITET  * np.sin(phi_angle_1) ** 2)
        sin_2 = np.sin(phi_angle_2) * np.sqrt(1 - EKSCENTRISITET ) / np.sqrt(1 - EKSCENTRISITET  * np.sin(phi_angle_2) ** 2)
        cos_2 = np.cos(phi_angle_2) / np.sqrt(1 - EKSCENTRISITET  * np.sin(phi_angle_2) ** 2)
        lamd1 = np.pi * lamd1 / 180
        lamd2 = np.pi * lamd2 / 180
        dl = lamd2 - lamd1
        cos_sigma = sin_1 * sin_2 + cos_1 * cos_2 * np.cos(dl)
        sin_sigma = np.sqrt((cos_2 * np.sin(dl)) ** 2 + (cos_1 * sin_2 - sin_1 * cos_2 * np.cos(dl)) ** 2)
        sigma = np.arctan(sin_sigma / cos_sigma)
        m = (sigma - sin_sigma) / (1 + cos_sigma)
        n = (sigma + sin_sigma) / (1 - cos_sigma)
        u = (sin_1 + sin_2) ** 2
        v = (sin_1 - sin_2) ** 2
        alpha = (BOLSHAYA_POLUOS - SJATIE) / BOLSHAYA_POLUOS
        dsigma = -0.25 * alpha * (m * u + n * v)
        a12 = np.arctan(cos_2 * np.sin(dl) / (cos_1 * sin_2 - sin_1 * cos_2 * np.cos(dl)))
        d = BOLSHAYA_POLUOS * (sigma + dsigma)
        return a12, d

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

    def set_blh(self, b, l, h):
        self.phi_angle = b * (np.pi / 180)
        self.lamda = l * (np.pi / 180)
        xyz = self.blh_to_xyz([b, l, h])
        self.Xr, self.Yr, self.Zr = xyz

    def set_all_coord(self, enu):
        xyz = self.enu_to_xyz(enu, enu=True)
        blh = self.blh_to_xyz(xyz, blh=True)
        return xyz, blh

    def get_p(self, height, v, table):
        temperature = 288.15 - 0.0065 * height  # абсолютная температура на высоте до 11км
        m = v / (20.05 * temperature ** (1 / 2))
        result = 0
        for s in range(len(table)):
            p = 1
            for i in range(len(table)):
                if i == s:
                    continue
                p *= ((m - table[i][0]) / (table[s][0] - table[i][0]))
            result += (p * table[s][1])
        return result

    def get_cy(self, height, v, at):
        cy_table = [[0.4, 0.1471243], [0.6, 0.1489569], [0.8, 0.1618757],
                    [1.2, 0.1553215], [1.4, 0.1377]]
        return 0.1 * at + self.get_p(height, v, cy_table)

    def get_cx(self, height, v, at, cy):
        cx_table = [[0.4, 0.021], [0.6, 0.022], [0.8, 0.045],
                    [1.2, 0.126], [1.4, 0.122]]

        return self.get_p(height, v, cx_table) + (cy / (1.4 * 3.12)) - 0.005

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
            enu[2] = dx[0] * (np.cos(self.phi_angle) * np.cos(self.lamda)) + dx[1] * (np.cos(self.phi_angle) * np.sin(self.lamda)) + \
                     dx[2] * np.sin(
                self.phi_angle)
            return enu
        else:
            xyz = [0] * 3
            xyz[0] = -np.sin(self.lamda) * crds[0] - np.sin(self.phi_angle) * np.cos(self.lamda) * crds[1] + np.cos(
                self.phi_angle) * np.cos(self.lamda) * \
                     crds[2] + self.Xr
            xyz[1] = np.cos(self.lamda) * crds[0] - np.sin(self.phi_angle) * np.sin(self.lamda) * crds[1] + np.cos(
                self.phi_angle) * np.sin(
                self.lamda) * \
                     crds[2] + self.Yr
            xyz[2] = np.cos(self.phi_angle) * crds[1] + np.sin(self.phi_angle) * crds[2] + self.Zr
            return xyz