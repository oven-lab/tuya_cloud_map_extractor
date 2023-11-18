class colors():
    """Number to color"""
    
    custom0 = {
        0: (255, 255, 255), #wall
        127: (44, 50, 64), #bg
        255: (94, 93, 109) #inside
    }
    #obstacle2 unreachable?
    v1 = {
        4: (94, 93, 109), #room
        5: (255, 255, 255), # room obstacle?
        7: (255, 255, 255), # room obstacle 2?
        8: (94, 93, 109), #room 2
        9: (255, 255, 255), # room 2 obstacle?
        11: (255, 255, 255), #room 2 obstacle 2?
        12: (94, 93, 109), # room 3
        13: (255, 255, 255), # room 3 obstacle?
        15: (255, 255, 255), # room 3 obstacle 2?
        16: (94, 93, 109), # room 4
        17: (255, 255, 255), # room 4 obstacle?
        19: (255, 255, 255), # room 4 obstacle 2?
        20: (94, 93, 109), #room 5
        21: (255, 255, 255), #room 5 obstacle?
        23: (255, 255, 255), #room5 obstacle2?
        24: (94, 93, 109), # room 6
        25: (255, 255, 255), # obstacle
        27: (255, 255, 255), # obstacle2
        28: (94, 93, 109), # room 7
        29: (255, 255, 255), # obstacle
        31: (255, 255, 255), # obstacle 2
        32: (94, 93, 109), # room 8
        33: (255, 255, 255), # obstacle
        35: (255, 255, 255), # obstacle 2
        36: (94, 93, 109), # room 9
        37: (255, 255, 255), # obstacle
        39: (255, 255, 255), # obstacle 2
        40: (94, 93, 109), # room 10
        41: (255, 255, 255), # obstacle
        43: (255, 255, 255), # obstacle 2
        44: (94, 93, 109), # room 11
        45: (255, 255, 255), # obstacle
        47: (255, 255, 255), # obstacle 2
        48: (94, 93, 109), # room 12
        49: (255, 255, 255), # obstacle
        51: (255, 255, 255), # obstacle 2
        52: (94, 93, 109), # room 13
        53: (255, 255, 255), # obstacle
        55: (255, 255, 255), # obstacle 2
        56: (94, 93, 109), # room 14
        57: (255, 255, 255), # obstacle
        59: (255, 255, 255), # obstacle 2
        60: (94, 93, 109), # room 15
        61: (255, 255, 255), # obstacle
        63: (255, 255, 255), # obstacle 2
        240: (255, 255, 255), #general obstacle?
        241: (255, 255, 255), #wall
        243: (44, 50, 64) #bg
    }

class ServerError(Exception):
    pass

class ClientIDError(Exception):
    pass

class ClientSecretError(Exception):
    pass

class DeviceIDError(Exception):
    pass
