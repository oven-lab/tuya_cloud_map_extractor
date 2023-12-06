import base64
import logging
import numpy as np

from .pylz4 import uncompress
from .const import default_colors, types

_LOGGER = logging.getLogger(__name__)

def decode_custom0(data):
    binary_data = base64.b64decode(data["data"]["map"])
    width = data["data"]["width"]
    height = data["data"]["height"]
    bytes_map = uncompress(binary_data)
    header = {
        "id": data["data"]["mapId"],
        "version": "custom0",
        "width": width,
        "height": height,
        "x_min": data["data"]["x_min"],
        "y_min": data["data"]["y_min"],
        "mapResolution": data["data"]["resolution"],
    }
    return header, bytes_map

def to_array_custom0(
    pixellist: list, width: int, height: int, colors: dict
) -> np.array:
    if colors == {}:
        colors["bg_color"] = default_colors.custom_0.get("bg_color")
        colors["wall_color"] = default_colors.custom_0.get("wall_color")
        colors["inside_color"] = default_colors.custom_0.get("inside_color")
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixeltype = types.custom0.get(
                pixellist[width_counter + height_counter * width]
            )
            pixel = colors[pixeltype]
            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1
    return np.array(pixels, dtype=np.uint8)