import numpy as np
import logging

from .pylz4 import uncompress
from .const import (
    default_colors, 
    types,
    BYTE_HEADER_LENGHT_PATH_V1
)
from .common import (
    _highLowToInt,
    _hexStringToNumber,
    _chunk,
    decode_header
)

_LOGGER = logging.getLogger(__name__)

def _deal_pl(point):
    return point - 65536 if point > 32768 else point


def _partition(string, chunk):
    return [string[i:i + chunk] for i in range(0, len(string), chunk)]


def scale_number(scale, value):
    return round(value / 10 ** scale, scale)


def shrink_value(value):
    return scale_number(1, value)


def _numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def _format_path_point(origin_point, reverse_y = True):
    x, y = origin_point['x'], origin_point['y']
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise ValueError(f"path point x or y is not number: x = {x}, y = {y}")
    real_point = [shrink_value(x), -shrink_value(y)] if reverse_y else [shrink_value(x), shrink_value(y)]
    return real_point

def decode_roomArr(mapRoomArr):
    rooms = []
    roomCount = _hexStringToNumber(mapRoomArr.hex()[2:4])[0]
    infoByteLen = 26
    nameByteLen = 20
    bytePos = 2 * 2
    for i in range(roomCount):
        roomInfoStr = mapRoomArr.hex()[
            bytePos : (bytePos + (infoByteLen + nameByteLen + 1) * 2)
        ]
        data = list(
            map(
                lambda x: _highLowToInt(x[0], x[1]),
                _chunk(_hexStringToNumber(roomInfoStr[0:16]), 2),
            )
        )
        data2 = _hexStringToNumber(roomInfoStr[16:28])
        nameLen = _hexStringToNumber(roomInfoStr[52:54])[0]
        vertexNum = _hexStringToNumber(roomInfoStr[-2:])[0]
        vertexStr = mapRoomArr.hex()[
            (bytePos + (infoByteLen + nameByteLen + 1) * 2) : (
                bytePos + (infoByteLen + nameByteLen + 1) * 2 + vertexNum * 2 * 2 * 2
            )
        ]
        bytePos = bytePos + (infoByteLen + nameByteLen + 1) * 2 + vertexNum * 2 * 2 * 2

        rooms.append(
            {
                "ID": data[0],
                "name": bytes.fromhex(
                    roomInfoStr[
                        (infoByteLen * 2 + 1 * 2) : (
                            infoByteLen * 2 + 1 * 2 + nameLen * 2
                        )
                    ]
                ).decode(),
                "order": data[1],
                "sweep_count": data[2],
                "mop_count": data[3],
                "color_order": data2[0],
                "sweep_forbidden": data2[1],
                "mop_forbidden": data2[2],
                "fan": data2[3],
                "water_level": data2[4],
                "y_mode": data2[5],
                "vertexNum": vertexNum,
                "vertexStr": vertexStr,
            }
        )

    return rooms

def decode_path_v1(pathdata):
    header_length = BYTE_HEADER_LENGHT_PATH_V1 // 2
    data_arr = _hexStringToNumber(pathdata)
    path_data_arr = [data_arr[i:i + 4] for i in range(header_length, len(data_arr), 4)]

    path_data = []
    for point in path_data_arr:
        x, y = [_deal_pl(_highLowToInt(high, low)) for high, low in _partition(point, 2)]
        real_point = _format_path_point({'x': x, 'y': y})
        path_data.append(real_point)

    return path_data

def to_array_v1(
    pixellist: list, width: int, height: int, rooms: dict, colors: dict
) -> np.array:
    if colors == {}:
        colors["bg_color"] = default_colors.v1.get("bg_color")
        colors["wall_color"] = default_colors.v1.get("wall_color")
        for i in rooms:
            colors["room_color_" + str(i["ID"])] = default_colors.v1.get("room_color")
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixeltype = types.v1.get(pixellist[width_counter + height_counter * width])
            pixel = colors.get(pixeltype)
            if not pixel:
                pixel = (20, 20, 20)
            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1
    return np.array(pixels, dtype=np.uint8)


def decode_v1(data: str, header: dict):
    _LOGGER.debug(header)
    mapArea = header["width"] * header["height"]
    infoLength = 48 + header["totalcount"] * 2
    encodeDataArray = bytes(_hexStringToNumber(data[48:infoLength]))
    raw = uncompress(encodeDataArray)
    mapDataArr = raw[0:mapArea]
    try:
        mapRoomArr = raw[mapArea:]
        header["roominfo"] = decode_roomArr(mapRoomArr)
    except IndexError:
        header["roominfo"] = []
        _LOGGER.debug("No rooms v1")

    return mapDataArr
