import numpy as np

from .const import default_colors, types
from .pylz4 import uncompress


def _hexStringToNumber(bits):
    number = []
    for i in [bits[i : i + 2] for i in range(0, len(bits), 2)]:
        number.append(int(i, 16))
    return number


def _chunk(In, n):
    out = []
    for i in [In[i : i + n] for i in range(0, len(In), n)]:
        out.append(i)
    return out


def _highLowToInt(high, low):
    return low + (high << 8)


def _numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def decode_header_v1(header: str):
    maxmin = list(
        map(lambda x: _highLowToInt(x[0], x[1]), _chunk(_hexStringToNumber(header), 2))
    )
    return {
        "id": list(
            map(
                lambda x: _highLowToInt(x[0], x[1]),
                _chunk(_hexStringToNumber(header[2:6]), 2),
            )
        ),
        "version": _hexStringToNumber(header[0:2]),
        "roomeditable": True,
        "type": _hexStringToNumber(header[6:8]),
        "width": maxmin[2],
        "height": maxmin[3],
        "originx": maxmin[4],
        "originy": maxmin[5],
        "mapResolution": maxmin[6],
        "pileX": maxmin[7],
        "pileY": maxmin[8],
        "totalcount": int(header[36:44], 16),
        "compressbeforelength": int(header[36:44], 16),
        "compressafterlenght": maxmin[11],
    }


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
