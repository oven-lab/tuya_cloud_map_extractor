"""Downloads and renders vacuum map from tuya servers."""
import base64
import requests

from requests.exceptions import JSONDecodeError

# import lz4.block
import logging
from PIL import Image, ImageDraw
from .v1 import decode_v1, to_array_v1, decode_path_v1
from .custom0 import decode_custom0, to_array_custom0
from .tuya import get_download_link

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
        header, mapDataArr = decode_v1(data)

    return header, mapDataArr

def parse_path(response: requests.models.Response, scale=2.0):
    try:
        data = response.json()
        path_data = [[]]
    except JSONDecodeError:
        data = response.content.hex()
        path_data = decode_path_v1(data)
    
    coords = []
    for coord in path_data:
        for i in coord:
            coords.append(i*scale)

    return coords



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
    if protoVer == "1":
        rooms = header["roominfo"]
        array = to_array_v1(pixellist, width, height, rooms, colors)

    image = Image.fromarray(array)
    return image


def get_map(
    server: str, client_id: str, secret_key: str, device_id: str, colors={}, path_settings={}
) -> Image:
    """Downloads and parses vacuum map from tuya cloud."""

    render_path = path_settings["path_enabled"]
    last = path_settings["last"]

    link = get_download_link(server, client_id, secret_key, device_id)
    map_link = link["result"][0]["map_url"]
    try:
        path_link = link["result"][1]["map_url"]
    except:
        _LOGGER.error("Your vacuum doesn't return a path")

    response = download(map_link)

    if response.status_code != 200:
        _LOGGER.warning("Got " + response.status_code + " from server whhle downloading map.")

    _LOGGER.debug(
        "Response: "
        + str(response.status_code)
        + str(base64.b64encode(response.content))
        + str(base64.b64encode(bytes(str(map_link), "utf-8")))
    )

    try:
        header, mapDataArr = parse_map(response)
    except Exception as e:
        _LOGGER.error(
            "Unsupported data type. Include the following data in a github issue to request the data format to be added: "
            + str(response.status_code)
            + str(base64.b64encode(response.content))
            + str(base64.b64encode(bytes(str(map_link), "utf-8")))
            + " Thank you!"
        )
        _LOGGER.error(e)

    image = render_layout(raw_map=mapDataArr, header=header, colors=colors)

    if render_path:
        _LOGGER.debug("Rendering path")

        if "path_color" not in colors:
            colors["path_color"] = [0, 255, 0]
        
        scale = int(1080/image.size[0])
        image = image.resize((image.size[0]*scale, image.size[1]*scale), resample=Image.BOX)
        response = download(path_link)
        if response.status_code != 200:
            _LOGGER.warning("Got " + response.status_code + " from server while downloading path.")
        path = parse_path(response, scale=scale)
        draw = ImageDraw.Draw(image)
        draw.line(path, fill=tuple(colors["path_color"]), width=1)

        if last:
            x, y = path[-2], path[-1]
        else:
            x, y = path[0], path[1]

        draw.ellipse([(x-5, y-5), (x+5, y+5)], outline=(255, 255, 255), fill=(0, 0, 255), width=1)

        return header, image
    
    return header, image


if __name__ == "__main__":
    print("Running as main.py")
    _server = input("Endpoint: ")
    _client_id = input("Client ID: ")
    _secret_key = input("Client Secret: ")
    _device_id = input("Device ID: ")
    _render_path = input("Render path?")
    if _render_path.lower() in ['true', '1', 't', 'y', 'yes']:
        _render_bool = True
    else:
        _render_bool = False
    _colors = {}
    headers, map_data = get_map(
        _server,
        _client_id,
        _secret_key,
        _device_id,
        _colors,
        _render_bool,
    )
    map_data.save('vacmap.png')