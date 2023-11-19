"""Downloads and renders vacuum map from tuya servers."""
import base64
import requests

from requests.exceptions import JSONDecodeError

# import lz4.block
import logging
from PIL import Image
from .pylz4 import uncompress
from .v1 import _hexStringToNumber, decode_header_v1, to_array_v1, decode_roomArr
from .tuya import get_download_link
from .const import colors
import numpy as np

_LOGGER = logging.getLogger(__name__)

def download_map(url: dict) -> dict:
    """Downloads map and converts it to a dictionary and bytes object."""

    mapurl = url["result"][0]["map_url"]

    response = requests.get(url=mapurl, timeout=2.5)
    _LOGGER.debug("Response: " + str(response.status_code) + str(base64.b64encode(response.content)) + str(base64.b64encode(bytes(str(url), 'utf-8'))))
    try:
        data = response.json()
        binary_data = base64.b64decode(data["data"]["map"])
        width = data["data"]["width"]
        height = data["data"]["height"]
        bytes_map = uncompress(binary_data)
        header = {
            'id': data["data"]["mapId"],
            'version': 'custom0',
            'width': width,
            'height': height,
            'x_min': data["data"]["x_min"],
            'y_min': data["data"]["y_min"],
            'mapresolution': data["data"]["resolution"]
        }
        return header, bytes_map
    except JSONDecodeError:
        data = response.content.hex()
        header = decode_header_v1(data[0:48])
        _LOGGER.debug(header)
        mapArea = header['width'] * header['height']
        infoLength = 48 + header['totalcount'] * 2
        encodeDataArray = bytes(_hexStringToNumber(data[48:infoLength]))
        raw = uncompress(encodeDataArray)
        mapDataArr = raw[0:mapArea]
        mapRoomArr = raw[mapArea:]
        header["roominfo"] = decode_roomArr(mapRoomArr)

        return header, mapDataArr
    except Exception as error:
        _LOGGER.error('Unsupported data type. Include the following data in a github issue to request the data format to be added: ' + str(response.status_code) + str(base64.b64encode(response.content)) + str(base64.b64encode(bytes(str(url), 'utf-8'))) + ' Thank you!')

def to_array_custom0(pixellist: list, width: int, height: int) -> np.array:
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixel = colors.custom0.get(pixellist[width_counter + height_counter * width])
            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1
    return np.array(pixels, dtype=np.uint8)

def render_layout(headers: dict, raw_map):
    """Renders the layout map."""

    height = headers['height']
    width = headers['width']

    pixellist = []
    for i in raw_map:
        pixellist.append(i)

    if headers["version"] == 'custom0':
        array = to_array_custom0(pixellist, width, height)
    if headers["version"] == [1]:
        array = to_array_v1(pixellist, width, height)

    image = Image.fromarray(array)
    return image

def get_map(server: str, client_id: str, secret_key: str, device_id: str) -> Image:
    """Downloads and parses vacuum map from tuya cloud."""
    map_link = get_download_link(server, client_id, secret_key, device_id)
    header, map = download_map(map_link)
    return render_layout(header, map)

if __name__ == "__main__":
    print("Running as main.py")
    headers, map = download_map(
        get_download_link(
            input('Endpoint: '),
            input('Client ID: '),
            input('Client Secret: '),
            input('Device ID: ')
        )
    )
    vacmap = render_layout(headers, map)
    vacmap.save("./vacmap.png")