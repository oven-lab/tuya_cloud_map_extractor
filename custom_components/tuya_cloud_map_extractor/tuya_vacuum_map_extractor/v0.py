import re
import numpy as np

from .pylz4 import uncompress
from .common import _hexStringToNumber
from .const import bitmapTypeHexMap, types, default_colors

def to_array_v0(
    pixellist: list, width: int, height: int, colors: dict
) -> np.array:
    if colors == {}:
        colors["bg_color"] = default_colors.v0.get("bg_color")
        colors["wall_color"] = default_colors.v0.get("wall_color")
        colors["inside_color"] = default_colors.v0.get("inside_color")
        colors["charger"] = default_colors.v0.get("charger")
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixeltype = types.v0.get(pixellist[width_counter + height_counter * width])
            pixel = colors.get(pixeltype)
            if not pixel:
                pixel = [20, 20, 20]
            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1
    return np.array(pixels, dtype=np.uint8)

def decode_v0(data: str, header: dict):
    encodeDataArray = bytes(_hexStringToNumber(data[48:]))
    decodeDataArray = uncompress(encodeDataArray)
    mapArea = header["width"] * header["height"]
    mapDataStr = ''.join(
        ''.join(
            ''.join(bitmapTypeHexMap[x] for x in re.findall(r'\w{2}', format(d, '08b')))
        )
        for d in decodeDataArray
        )[:mapArea * 2]

    return bytes.fromhex(mapDataStr)