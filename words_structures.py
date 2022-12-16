from ctypes import Structure, c_ulong


class BNR(Structure):
    _fields_ = [
        ("address", c_ulong, 8),
        ("value", c_ulong, 20),
        ("empty", c_ulong, 1),
        ("stateMatrix", c_ulong, 2),
        ("p", c_ulong, 1)
    ]


class DSC(Structure):
    _fields_ = [
        ("address", c_ulong, 8),
        ("SDI", c_ulong, 2),
        ("prep_zk", c_ulong, 1),
        ("control", c_ulong, 1),
        ("navigation", c_ulong, 1),
        ("gyrocompass", c_ulong, 1),
        ("emty1", c_ulong, 1),
        ("reboot", c_ulong, 1),
        ("prep", c_ulong, 3),
        ("heat", c_ulong, 1),
        ("termostatir", c_ulong, 1),
        ("no_init_data", c_ulong, 1),
        ("no_reception", c_ulong, 1),
        ("operability_ins", c_ulong, 1),
        ("ready_acceleration", c_ulong, 1),
        ("ready", c_ulong, 1),
        ("empty2", c_ulong, 3),
        ("sm", c_ulong, 2),
        ("p", c_ulong, 1)
    ]


class Time(Structure):
    _fields_ = [
        ("address", c_ulong, 8),
        ("hours", c_ulong, 5),
        ("minutes", c_ulong, 6),
        ("seconds", c_ulong, 6),
        ("empty", c_ulong, 4),
        ("sm", c_ulong, 2),
        ("p", c_ulong, 1)
    ]


class Date(Structure):
    _fields_ = [("address", c_ulong, 8),
                ("empty1", c_ulong, 2),
                ("years", c_ulong, 8),
                ("months", c_ulong, 5),
                ("days", c_ulong, 6),
                ("matrix", c_ulong, 2),
                ("empty2", c_ulong, 1)
                ]


class SRNS(Structure):
    _fields_ = [
        ("address", c_ulong, 8),
        ("dataRequest", c_ulong, 1),
        ("SNSType", c_ulong, 3),
        ("gpsAlmanac", c_ulong, 1),
        ("glonassAlmanac", c_ulong, 1),
        ("workMode", c_ulong, 2),
        ("sub_modes", c_ulong, 1),
        ("sign_time", c_ulong, 1),
        ("empty1", c_ulong, 2),
        ("diffMeasurments", c_ulong, 1),
        ("empty2", c_ulong, 1),
        ("failing", c_ulong, 1),
        ("signalThreshold", c_ulong, 1),
        ("coordSystem", c_ulong, 2),
        ("empty3", c_ulong, 3),
        ("sm", c_ulong, 2),
        ("p", c_ulong, 1)
    ]
