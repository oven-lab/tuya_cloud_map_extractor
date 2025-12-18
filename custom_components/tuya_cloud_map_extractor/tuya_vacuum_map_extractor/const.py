BYTE_HEADER_LENGHT_PATH_V1 = 26
is_Lz4 = True

bitmapTypeHexMap = {
  '00': '00', # Cleaning point
  '01': 'f1', # Obstacle point
  '10': 'f2', # Charging pile
  '11': 'ff', # Unknown area 
}

class types:
    """Number to type"""

    custom0 = {
        0: "wall_color",  # wall
        1: "room_color",
        2: "room_color",
        3: "room_color",
        4: "room_color",
        5: "room_color",
        6: "room_color",
        7: "room_color",
        8: "room_color",
        9: "room_color",
        10: "room_color",
        11: "room_color",
        12: "room_color",
        13: "room_color",
        14: "room_color",
        15: "room_color",
        16: "room_color",
        17: "room_color",
        18: "room_color",
        19: "room_color",
        20: "room_color",
        21: "room_color",
        22: "room_color",
        23: "room_color",
        24: "room_color",
        25: "room_color",
        127: "bg_color",  # bg
        255: "inside_color",  # inside
    }

    v0 = {
        0: "inside_color",
        241: "wall_color",
        242: "charger",
        255: "bg_color"
    }
    # obstacle2 unreachable?
    v1 = {
        0: "room_color_0",
        1: "wall_color",
        3: "wall_color",
        4: "room_color_1",
        5: "wall_color",
        7: "wall_color",
        8: "room_color_2",
        9: "wall_color",
        11: "wall_color",
        12: "room_color_3",
        13: "wall_color",
        15: "wall_color",
        16: "room_color_4",
        17: "wall_color",
        19: "wall_color",
        20: "room_color_5",
        21: "wall_color",
        23: "wall_color",
        24: "room_color_6",
        25: "wall_color",
        27: "wall_color",
        28: "room_color_7",
        29: "wall_color",
        31: "wall_color",
        32: "room_color_8",
        33: "wall_color",
        35: "wall_color",
        36: "room_color_9",
        37: "wall_color",
        39: "wall_color",
        40: "room_color_10",
        41: "wall_color",
        43: "wall_color",
        44: "room_color_11",
        45: "wall_color",
        47: "wall_color",
        48: "room_color_12",
        49: "wall_color",
        51: "wall_color",
        52: "room_color_13",
        53: "wall_color",
        55: "wall_color",
        56: "room_color_14",
        57: "wall_color",
        59: "wall_color",
        60: "room_color_15",
        61: "wall_color",
        63: "wall_color",
        64: "room_color_16",
        65: "wall_color",
        67: "wall_color",
        68: "room_color_17",
        69: "wall_color",
        71: "wall_color",
        72: "room_color_18",
        73: "wall_color",
        75: "wall_color",
        76: "room_color_19",
        77: "wall_color",
        79: "wall_color",
        80: "room_color_20",
        81: "wall_color",
        83: "wall_color",
        84: "room_color_21",
        85: "wall_color",
        87: "wall_color",
        88: "room_color_22",
        89: "wall_color",
        91: "wall_color",
        92: "room_color_23",
        93: "wall_color",
        95: "wall_color",
        96: "room_color_24",
        97: "wall_color",
        99: "wall_color",
        100: "room_color_25",
        101: "wall_color",
        103: "wall_color",
        104: "room_color_26",
        105: "wall_color",
        107: "wall_color",
        108: "room_color_27",
        109: "wall_color",
        111: "wall_color",
        112: "room_color_28",
        113: "wall_color",
        115: "wall_color",
        116: "room_color_29",
        117: "wall_color",
        119: "wall_color",
        120: "room_color_30",
        121: "wall_color",
        123: "wall_color",
        124: "room_color_31",
        125: "wall_color",
        127: "wall_color",
        128: "room_color_32",
        129: "wall_color",
        131: "wall_color",
        132: "room_color_33",
        133: "wall_color",
        135: "wall_color",
        136: "room_color_34",
        137: "wall_color",
        139: "wall_color",
        140: "room_color_35",
        141: "wall_color",
        143: "wall_color",
        144: "room_color_36",
        145: "wall_color",
        147: "wall_color",
        148: "room_color_37",
        149: "wall_color",
        151: "wall_color",
        152: "room_color_38",
        153: "wall_color",
        155: "wall_color",
        156: "room_color_39",
        157: "wall_color",
        159: "wall_color",
        160: "room_color_40",
        161: "wall_color",
        163: "wall_color",
        164: "room_color_41",
        165: "wall_color",
        167: "wall_color",
        168: "room_color_42",
        169: "wall_color",
        171: "wall_color",
        172: "room_color_43",
        173: "wall_color",
        175: "wall_color",
        176: "room_color_44",
        177: "wall_color",
        179: "wall_color",
        180: "room_color_45",
        181: "wall_color",
        183: "wall_color",
        184: "room_color_46",
        185: "wall_color",
        187: "wall_color",
        188: "room_color_47",
        189: "wall_color",
        191: "wall_color",
        192: "room_color_48",
        193: "wall_color",
        195: "wall_color",
        196: "room_color_49",
        197: "wall_color",
        199: "wall_color",
        200: "room_color_50",
        201: "wall_color",
        203: "wall_color",
        204: "room_color_51",
        205: "wall_color",
        207: "wall_color",
        208: "room_color_52",
        209: "wall_color",
        211: "wall_color",
        212: "room_color_53",
        213: "wall_color",
        215: "wall_color",
        216: "room_color_54",
        217: "wall_color",
        219: "wall_color",
        220: "room_color_55",
        221: "wall_color",
        223: "wall_color",
        224: "room_color_56",
        225: "wall_color",
        227: "wall_color",
        228: "room_color_57",
        229: "wall_color",
        231: "wall_color",
        232: "room_color_58",
        233: "wall_color",
        235: "wall_color",
        236: "room_color_59",
        237: "wall_color",
        239: "wall_color",
        240: "wall_color",  # general obstacle?
        241: "wall_color",  # wall
        243: "bg_color",  # bg
        248: "wall_color",
        249: "wall_color",
        251: "wall_color",
        252: "wall_color",
        253: "wall_color",
        255: "bg_color"
    }


class default_colors:
    """Default colors"""

    custom_0 = {
        "wall_color": [255, 255, 255],
        "bg_color": [44, 50, 64],
        "inside_color": [94, 93, 109],
    }

    v0 = {
        "wall_color": [255, 255, 255],
        "bg_color": [44, 50, 64],
        "inside_color": [94, 93, 109],
        "charger": [0, 255, 0]
    }

    v1 = {
        "wall_color": [255, 255, 255],
        "bg_color": [44, 50, 64],
        "room_color": [94, 93, 109],
    }


class ServerError(Exception):
    pass


class ClientIDError(Exception):
    pass


class ClientSecretError(Exception):
    pass


class DeviceIDError(Exception):
    pass

class PixelValueNotDefined(Exception):
    pass

class NotSupportedError(Exception):
    pass