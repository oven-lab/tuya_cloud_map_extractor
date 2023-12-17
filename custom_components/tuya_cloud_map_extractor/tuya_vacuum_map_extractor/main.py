"""Downloads and renders vacuum map from tuya servers."""
import base64
import requests
import math

from requests.exceptions import JSONDecodeError
from datetime import datetime

# import lz4.block
import logging
from PIL import Image, ImageDraw
from .v0 import decode_v0, to_array_v0
from .v1 import decode_v1, to_array_v1, decode_path_v1, _format_path_point
from .custom0 import decode_custom0, to_array_custom0, decode_path_custom0, map_to_image
from .tuya import get_download_link
from .const import NotSupportedError
from .common import decode_header

_LOGGER = logging.getLogger(__name__)

def download(url: str) -> requests.models.Response:
    """Downloads map and converts it to a dictionary and bytes object."""

    response = requests.get(url=url, timeout=2.5)
    return response

def parse_map(response: requests.models.Response):
    try:
        data = response.json()
        header, mapDataArr = decode_custom0(data)

    except JSONDecodeError:
        data = response.content.hex()
        header = decode_header(data[0:48])
        if header["version"] == [0]:
            mapDataArr = decode_v0(data, header)
        elif header["version"] == [1]:
            mapDataArr = decode_v1(data, header)
        else:
            raise NotSupportedError("Map version " + str(header["version"]) +" is not supported.")
        
    return header, mapDataArr

def parse_path(response: requests.models.Response, scale=2.0, header={}):
    try:
        data = response.json()
        path_data = decode_path_custom0(data, header)
    except JSONDecodeError:
        data = response.content.hex()
        path_data = decode_path_v1(data)
    
    coords = []
    for coord in path_data:
        for i in coord:
            coords.append(i*scale)

    return coords

def flip(headers: dict, image: Image.Image, settings: dict):
    rotate = settings["rotate"]
    flip_vertical = settings["flip_vertical"]
    flip_horizontal = settings["flip_horizontal"]
    if rotate == 90:
        image = image.transpose(Image.ROTATE_90)
    elif rotate == 180:
        image = image.transpose(Image.ROTATE_180)
    elif rotate == -90:
        image = image.transpose(Image.ROTATE_270)
    if flip_vertical:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_horizontal:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    return headers, image

def render_layout(raw_map: bytes, header: dict, colors: dict) -> Image.Image:
    """Renders the layout map."""

    width = header["width"]
    height = header["height"]

    if isinstance(header["version"], list):
        protoVer = str(header["version"][0])
    else:
        protoVer = header["version"]

    pixellist = []
    for i in raw_map:
        pixellist.append(i)

    if protoVer == "custom0":
        array = to_array_custom0(pixellist, width, height, colors)
    
    elif protoVer == "0":
        array = to_array_v0(pixellist, width, height, colors)

    elif protoVer == "1":
        rooms = header["roominfo"]
        array = to_array_v1(pixellist, width, height, rooms, colors)

    image = Image.fromarray(array)
    return image


def get_map(
    server: str, client_id: str, secret_key: str, device_id: str, colors={}, settings={}, urls={}
) -> Image:
    """Downloads and parses vacuum map from tuya cloud."""
    render_path = settings["path_enabled"]
    last = settings["last"]
    if urls != {}:
        time = datetime.strptime(urls["time"], "%H:%M:%S")
        now = datetime.now().strftime("%H:%M:%S")
        now = datetime.strptime(now, "%H:%M:%S")
        delta = now-time
        minutes_delta = math.ceil(delta.total_seconds() / 60)
        if minutes_delta < 59:
            link = {}
            link["result"] = urls["links"]
        else:
            link = get_download_link(server, client_id, secret_key, device_id)
    else:
        link = get_download_link(server, client_id, secret_key, device_id)

    map_link = link["result"][0]["map_url"]

    response = download(map_link)

    if response.status_code != 200:
        _LOGGER.warning("Got " + str(response.status_code) + " from server whhle downloading map.")

    _LOGGER.debug(
        "Response: "
        + str(response.status_code)
        + str(base64.b64encode(response.content))
        + str(base64.b64encode(bytes(str(link), "utf-8")))
    )

    try:
        header, mapDataArr = parse_map(response)
        image = render_layout(raw_map=mapDataArr, header=header, colors=colors)
    except Exception as e:
        _LOGGER.error(
            "Unsupported data type. Include the following data in a github issue to request the data format to be added: "
            + str(response.status_code)
            + str(base64.b64encode(response.content))
            + str(base64.b64encode(bytes(str(link), "utf-8")))
            + " Thank you!"
        )
        raise e

    if urls == {}:
        header["urls"] = {
            "links": link["result"],
            "time": datetime.now().strftime("%H:%M:%S"),
        }
    else:
        header["urls"] = urls

    if render_path:
        _LOGGER.debug("Rendering path")
        try:
            path_link = link["result"][1]["map_url"]
        except:
            _LOGGER.error("Your vacuum doesn't return a path")
            return flip(header, image, settings)

        if "path_color" not in colors:
            colors["path_color"] = [0, 255, 0]
        
        scale = int(1080/image.size[0])
        image = image.resize((image.size[0]*scale, image.size[1]*scale), resample=Image.BOX)
        response = download(path_link)
        if response.status_code != 200:
            _LOGGER.warning("Got " + str(response.status_code) + " from server while downloading path.")
            raise FileNotFoundError
        
        _LOGGER.debug(
            "Response path: "
            + str(response.status_code)
            + str(base64.b64encode(response.content))
        )

        path = parse_path(response, scale=scale, header=header)
        draw = ImageDraw.Draw(image, 'RGBA')
        draw.line(path, fill=tuple(colors["path_color"]), width=2)

        x, y = header["pileX"], header["pileY"]
        if header["version"] in [[0], [1]]:
            point = _format_path_point({'x': x, 'y': y}, False)
        elif header["version"] == "custom0":
            point = map_to_image([x, y], header["mapResolution"], header["x_min"], header["y_min"])

        x = point[0]*scale
        y = point[1]*scale
        
        draw.ellipse([(x-10, y-10), (x+10, y+10)], outline=(255, 255, 255), fill=(0, 255, 0), width=2)

        if last:
            x, y = path[-2], path[-1]
        else:
            x, y = path[0], path[1]

        draw.ellipse([(x-7, y-7), (x+7, y+7)], outline=(255, 255, 255), fill=(0, 0, 255), width=2)

        if "area" in header and header["version"] == "custom0":
            for area in header["area"]:
                coords = []
                for i in area["vertexs"]:
                    coords.append(i[0]*scale)
                    coords.append(i[1]*scale)
                if area["type"] == "forbid":
                    draw.polygon(coords, outline=(255,255,255), width=1, fill=(255, 210, 0, 128))
                else:
                    draw.polygon(coords, outline=(255,255,255), width=1, fill=(255, 255, 255, 64))

        return flip(header, image, settings)
    
    return flip(header, image, settings)
