import base64
import logging
import numpy as np

from .pylz4 import uncompress
from .const import default_colors, types, PixelValueNotDefined

_LOGGER = logging.getLogger(__name__)

def map_to_image(point: list, resolution, x_min, y_min):
    x_min_calc = x_min/resolution
    y_min_calc = y_min/resolution
    return [abs(point[0] / 1000 / resolution - x_min_calc), abs(point[1] / 1000 / resolution - y_min_calc)]

def image_to_map(point: list, resolution, x_min, y_min):
    x_min_calc = x_min/resolution
    y_min_calc = y_min/resolution
    return [(point[0] + x_min_calc) * resolution * 1000,(point[1] + y_min_calc) * resolution * 1000]

def create_calibration_points(resolution, x_min, y_min):
    cal_points = []
    points = [[0, 0], [0, 20], [20, 0]]
    for point in points:
        cal = image_to_map(point, resolution, x_min, y_min)
        cal_points.append({
            "vacuum": {"x": point[0], "y": point[1]},
            "map": {"x": cal[0], "y": cal[1]}
        })

    return cal_points

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
        "calibrationPoints": create_calibration_points(data["data"]["resolution"], data["data"]["x_min"], data["data"]["y_min"])
    }
    if "pathId" in data["data"]:
        header["path_id"] = data["data"]["pathId"]
    
    header["roominfo"] = decode_roomArr(data["data"]["area"], header)

    return header, bytes_map

def decode_roomArr(areas: dict, header: dict):
    rooms = []
    for area in areas:
        room = {
            "id": area["id"],
            "type": area["active"],
            "mode": area["mode"],
            "tag": area["tag"],
            "name": area["name"]
        }
        if "forbidType" in area:
            room["forbidType"] = area["forbidType"]
        room_vertexs = []
        for vertex in area["vertexs"]:
            room_vertexs.append(map_to_image(vertex, header["mapResolution"], header["x_min"], header["y_min"]))
        room["vertexs"] = room_vertexs
        rooms.append(room)

    return rooms

def decode_path_custom0(data, header):
    resolution = header["mapResolution"]
    x_min = header["x_min"]
    y_min = header["y_min"]
    coords = []
    for i in data["data"]["posArray"]:
        coord = map_to_image(i, resolution, x_min, y_min)
        coords.append(coord)
    return coords

def to_array_custom0(
    pixellist: list, width: int, height: int, colors: dict
) -> np.array:
    if colors == {}:
        colors["bg_color"] = default_colors.custom_0.get("bg_color")
        colors["wall_color"] = default_colors.custom_0.get("wall_color")
        colors["inside_color"] = default_colors.custom_0.get("inside_color")
    colors["room_color"] = colors["inside_color"]
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixeltype = types.custom0.get(
                pixellist[width_counter + height_counter * width]
            )

            if pixeltype != None:
                pixel = colors[pixeltype]
            else:
                raise PixelValueNotDefined

            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1
    return np.array(pixels, dtype=np.uint8)