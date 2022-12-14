import time
from words_structures import BNR, Time, Date, SRNS, DSC
from ctypes import Structure


ADRES_DSC = 270
ADRES_DATA = 260
ADRES_SRNS = 273

data_of_ins = {
    "latitude": {'address': 310, 'value': 22.5, "senior_bit": 90}, #Широта
    "longitude": {'address': 311, 'value': 22.5, "senior_bit": 90}, #Долгота
    "altitude": {'address': 361, 'value': 3048, "senior_bit": 19975.3728}, #Высота
    "true_course": {'address': 314, 'value': 10, "senior_bit": 90}, #Курс истинный
    "pitch_angle": {'address': 324, 'value': 5, "senior_bit": 90}, #Угол тангажа
    "roll_angle": {'address': 325, 'value': 45, "senior_bit": 90}, #Угол крена
    "speed_north_south": {'address': 366, 'value': 102.888, "senior_bit": 1053.5822}, #Скорость Север/Юг
    "speed_east_west": {'address': 367, 'value': 102.888, "senior_bit": 1053.5822}, #Скорость Восток/Запад
    "vertically_speed": {'address': 365, 'value': 3.048, "senior_bit": 83.2307}, #Ускорение продольное
    "ax": {'address': 331, 'value': 0.196133, "senior_bit": 19.62}, #Ускорение поперечное
    "az": {'address': 332, 'value': 0.98066, "senior_bit": 19.62}, #Ускорение нормальное
    "ay": {'address': 333, 'value': 0.98066, "senior_bit": 19.62}, #Слово Состояния ИНС
    "status_word": {'address': 270},
}
data_of_sns = {
    "H": {'address': 76, 'value': 9834, "senior_bit": 65536}, #Высота
    "HDOP": {'address': 101, 'value': 312, "senior_bit": 512}, #горизонтальный геометрический фактор
    "VDOP": {'address': 102, 'value': 100, "senior_bit": 512}, #вертикальный геометрический фактор
    "PU": {'address': 103, 'value': 45, "senior_bit": 90}, #Путевой угол
    "B": {'address': 110, 'value': 45, "senior_bit": 90}, #Текущая широта
    "Bt": {'address': 120, 'value': 0.000057, "senior_bit": 0.00008583}, #Текущая широта (точно)
    "L": {'address': 111, 'value': 45, "senior_bit": 90}, #Текущая долгота
    "Lt": {'address': 121, 'value': 0.000057, "senior_bit": 0.00008583}, #Текущая долгота(точно)
    "delay": {'address': 113, 'value': 57, "senior_bit": 512}, #Задержка выдачи обновленных НП относительно MB «1 с»
    "cur_time_senior_ranks": {'address': 150, 'value': "7,35,8", "senior_bit": "16,32,32"}, #Текущее время UTC (старшие разряды)
    "cur_time_junior_ranks": {'address': 140, 'value': 10, "senior_bit": 512}, #Текущее время UTC (младшие разряды) непрерывное между метками MB «1 с»
    "Vh": {'address': 165, 'value': 231, "senior_bit": 16384}, #Вертикальная скорость                               Vh
    "date": {'address': 260, 'value': "1,12,22", "senior_bit": ""}, #Дата
    "SRNS": {'address': 273, 'value': 1, "senior_bit": ""}} #Признаки СРНС


class INS(Structure):

    _fields_ = [("latitude", BNR),
                ("longitude", BNR),
                ("altitude", BNR),
                ("true_course", BNR),
                ("pitch_angle", BNR),
                ("roll_angle", BNR),
                ("speed_north_south", BNR),
                ("speed_east_west", BNR),
                ("vertically_speed", BNR),
                ("ax", BNR),
                ("az", BNR),
                ("ay", BNR),
                ("status_word", DSC)]

#The INS has the following operating modes:

    def contr(self): #«КОНТРОЛЬ»
        time.sleep(20)
        self.status_word = DSC(code_addr(ADRES_DSC))
        self.status_word.no_init_data = 1
        self.status_word.operability_ins = 1
        print(self.status_word.no_init_data, self.status_word.ready_acceleration)

    def prep(self): #«Подготовка» (начальная выставка)
        self.status_word.prep_zk = 1
        self.status_word.no_init_data = 0
        print(self.status_word.no_init_data, self.status_word.ready_acceleration, self.status_word.prep_zk, self.status_word.no_init_data)

    def navig(self, navData): #«Навигация» (рабочий режим)
        attributes = [attrib[0] for attrib in self._fields_]
        for attributes in attributes:
            if attributes != "status_word":
                setattr(self, attributes, BNR(code_addr(addr=navData[attributes]["address"]),
                                              code_data(data=navData[attributes]["value"], bits=20,
                                                        senior_bit=navData[attributes]["senior_bit"]), 0,
                                              1))


class SNS(Structure):

    _fields_ = [("H", BNR),
                ("HDOP", BNR),
                ("VDOP", BNR),
                ("PU", BNR),
                ("B", BNR),
                ("Bt", BNR),
                ("L", BNR),
                ("Lt", BNR),
                ("delay", BNR),
                ("cur_time_senior_ranks", Time),
                ("cur_time_junior_ranks", BNR),
                ("Vh", BNR),
                ("date", Date),
                ("SRNS", SRNS)]

#The SNS has the following operating modes:

    def contr(self):  #«КОНТРОЛЬ»
        time.sleep(20)
        self.feature = SRNS(code_addr(ADRES_SRNS))
        self.feature.workMode = 2
        self.feature.sub_modes = 1
        self.feature.failing = 0
        print(self.feature.workMode, self.feature.sub_modes, self.feature.failing)

    def navig(self, navData): #«НАВИГАЦИЯ»
        attributes = [attrib[0] for attrib in self._fields_]
        for attributes in attributes:
            if (attributes != "cur_time_senior_ranks") and (attributes != "date") and (attributes != "SRNS"):
                setattr(self, attributes, BNR(code_addr(addr=navData[attributes]["address"]),
                                              code_data(data=navData[attributes]["value"], bits=20,
                                                        senior_bit=navData[attributes]["senior_bit"])))
        hours, minutes, seconds = navData["cur_time_senior_ranks"]["value"].split(",")
        self.cur_time_senior_ranks = Time(code_addr(addr=navData["cur_time_senior_ranks"]["address"]), int(hours), int(minutes), int(seconds))
        years, months, days = navData["date"]["value"].split(",")
        self.date = Date(code_addr(addr=navData["date"]["address"]), int(years), int(months), int(days))
        self.feature = SRNS(code_addr(addr=navData["SRNS"]["address"]))




def code_data(data, bits: int, senior_bit):
    return int(2 ** (bits - 1) * data / senior_bit)

def code_addr(addr):
    strAddress = str(addr)
    cAdr = 0
    for i in range(len(strAddress)):
        cAdr += int(int(strAddress[i]) * 8 ** (len(strAddress) - i - 1))
    return cAdr
