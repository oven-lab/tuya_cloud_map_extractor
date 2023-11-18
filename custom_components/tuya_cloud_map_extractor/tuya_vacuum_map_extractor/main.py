"""Downloads and renders vacuum map from tuya servers."""
import base64
import datetime
import hmac
import requests

from requests.exceptions import JSONDecodeError

# import lz4.block
import logging
from PIL import Image
from .pylz4 import uncompress
import numpy as np

_LOGGER = logging.getLogger(__name__)

class ServerError(Exception):
    pass

class ClientIDError(Exception):
    pass

class ClientSecretError(Exception):
    pass

class DeviceIDError(Exception):
    pass

class colors():
    """num to color"""
    
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

def get_download_link(
    server: str, client_id: str, secret_key: str, device_id: str, token=""
) -> str:
    """Gets the download link of the real time map."""

    if token == "":
        url = "/v1.0/token?grant_type=1"
        response = tuyarequest(
            server=server, url=url, client_id=client_id, secret_key=secret_key
        )

        if not response["success"]:
            if response["msg"] == "clientId is invalid":
                raise ClientIDError("Invalid Client ID")
            elif response["msg"] == "sign invalid":
                raise ClientSecretError("Invalid Client Secret")
            elif "cross-region access is not allowed" in response["msg"]:
                raise ServerError("Wrong server region. Cross-region access is not allowed.")
            else:
                raise RuntimeError("Request failed - Response: ", response)

        access_token = response["result"]["access_token"]

    url = "/v1.0/users/sweepers/file/" + device_id + "/realtime-map"
    response = tuyarequest(
        server=server,
        url=url,
        client_id=client_id,
        secret_key=secret_key,
        token=access_token,
    )

    if not response["success"]:
        if response["msg"] == "permission deny":
            raise DeviceIDError("Invalid Device ID")
        else:
            raise RuntimeError("Request failed - Response: ", response)

    return response["result"][0]["map_url"]


def download_map(url: str) -> dict:
    """Downloads map and converts it to a dictionary and bytes object."""

    response = requests.get(url=url, timeout=2.5)
    _LOGGER.debug("Response. " + str(response.status_code) + str(response.content))
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

        return header, mapDataArr

def decode_header_v1(header: str):
    maxmin = list(map(lambda x: _highLowToInt(x[0], x[1]), _chunk(_hexStringToNumber(header), 2)))
    return {
        'id': list(map(lambda x: _highLowToInt(x[0], x[1]), _chunk(_hexStringToNumber(header[2:6]), 2))),   
        'version': _hexStringToNumber(header[0:2]),
        'roomeditable': True,   
        'type': _hexStringToNumber(header[6:8]),
        'width': maxmin[2],
        'height': maxmin[3],
        'originx': maxmin[4],
        'originy': maxmin[5],
        'mapResolution': maxmin[6],
        'pileX': maxmin[7],
        'pileY': maxmin[8],
        'totalcount': int(header[36:44], 16),
        'compressbeforelength': int(header[36:44], 16),
        'compressafterlenght': maxmin[11]
    }

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
    
def to_array_v1(pixellist: list, width: int, height: int) -> np.array:
    pixels = []
    height_counter = 0
    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            pixel = colors.v1.get(pixellist[width_counter + height_counter * width])
            if not pixel: 
                pixel = (20, 20, 20)
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


def _get_sign(client_id: str, secret_key: str, url: str, t: int, token: str):
    empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    signstr = client_id + token + t + "GET" + "\n" + empty_hash + "\n" + "" + "\n" + url
    return hmac.new(
        secret_key.encode(), msg=signstr.encode(), digestmod="sha256"
    ).hexdigest()

def _hexStringToNumber(bits):
    number = []
    for i in [bits[i:i+2] for i in range(0, len(bits), 2)]:
        number.append(int(i, 16))
    return number

def _chunk(In, n):
    out = []
    for i in [In[i:i+n] for i in range(0, len(In), n)]:
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

def tuyarequest(
    server: str, url: str, client_id: str, secret_key: str, token=""
) -> dict:
    """Handles authentication with provided token and makes request to tuya servers."""

    t = str(int(round(datetime.datetime.timestamp(datetime.datetime.now()) * 1000, 0)))
    sign = _get_sign(
        client_id=client_id, secret_key=secret_key, url=url, t=t, token=token
    )
    headers = {
        "sign_method": "HMAC-SHA256",
        "client_id": client_id,
        "t": t,
        "sign": sign.upper(),
    }
    if token != "":
        headers["access_token"] = token
    return requests.get(url=server + url, headers=headers, timeout=2.5).json()


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
