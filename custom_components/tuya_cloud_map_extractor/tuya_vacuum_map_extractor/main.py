"""Downloads and renders vacuum map from tuya servers."""
import base64
import datetime
import hmac
import requests

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
    """Downloads map and converts it to a dictionary object."""

    response = requests.get(url=url, timeout=2.5)
    _LOGGER.debug("Response. " + str(response.status_code) + str(response.content))
    return response.json()


def render_layout(raw_map: dict):
    """Renders the layout map."""
    binary_data = base64.b64decode(raw_map["data"]["map"])

    width = raw_map["data"]["width"]
    height = raw_map["data"]["height"]
    size = width * height
    bytes_map = uncompress(binary_data)
    pixellist = []
    for i in bytes_map:
        pixellist.append(i)

    pixels = []
    height_counter = 0

    while height_counter < height:
        width_counter = 0
        line = []
        while width_counter < width:
            if pixellist[width_counter + height_counter * width] == 0:
                pixel = (255, 255, 255)
            elif pixellist[width_counter + height_counter * width] == 127:
                pixel = (44, 50, 64)
            elif pixellist[width_counter + height_counter * width] == 255:
                pixel = (94, 93, 109)
            else:
                pixel = (0, 0, 255)
            line.append(pixel)
            width_counter = width_counter + 1
        pixels.append(line)
        height_counter = height_counter + 1

    array = np.array(pixels, dtype=np.uint8)
    image = Image.fromarray(array).transpose(method=Image.FLIP_TOP_BOTTOM)
    return image


def _get_sign(client_id: str, secret_key: str, url: str, t: int, token: str):
    empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    signstr = client_id + token + t + "GET" + "\n" + empty_hash + "\n" + "" + "\n" + url
    return hmac.new(
        secret_key.encode(), msg=signstr.encode(), digestmod="sha256"
    ).hexdigest()

def _get_token(server: str, client_id: str, secret_key: str) -> str:
    url = "/v1.0/token?grant_type=1"
    response = tuyarequest(
        server=server, url=url, client_id=client_id, secret_key=secret_key
    )
    _LOGGER.debug(response)
    if not response["success"]:
        if response["msg"] == "clientId is invalid":
            raise ClientIDError("Invalid Client ID")
        if response["msg"] == "sign invalid":
            raise ClientSecretError("Invalid Client Secret")
        if "cross-region access is not allowed" in response["msg"]:
            raise ServerError("Wrong server region. Cross-region access is not allowed.")
        raise RuntimeError("Request failed - Response: ", response)
    return response["result"]["access_token"]


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
    return render_layout(download_map(map_link))

def debug_file(server: str, client_id: str, secret_key: str, device_id: str) -> bytes:
    """Gets the latest file from the tuya servers."""
    token = _get_token(server, client_id, secret_key)

    url = "/v1.0/users/sweepers/file/" + device_id + "/list?fileType=pic&pageNo=1&pageSize=1"
    response = tuyarequest(
        server=server,
        url=url,
        client_id=client_id,
        secret_key=secret_key,
        token=token,
    )

    _LOGGER.debug(response)

    if not response["success"]:
        if response["msg"] == "permission deny":
            raise DeviceIDError("Invalid Device ID")
        raise RuntimeError("Request failed - Response: ", response)
    
    ids = response["result"]["datas"][0]["id"]

    url = "/v1.0/users/sweepers/file/" + device_id + "/download?id=" + str(ids)
    response = tuyarequest(
        server=server,
        url=url,
        client_id=client_id,
        secret_key=secret_key,
        token=token,
    )
    _LOGGER.debug(response)
    url = response["result"]["app_map"]

    response = requests.get(url, timeout=2.5)
    return response.content

if __name__ == "__main__":
    print("Running as main.py")
    vacmap = render_layout(
        download_map(
            get_download_link(
                input("Server: "),
                input("Client ID: "),
                input("Client Secret: "),
                input("Device ID: "),
            )
        )
    )
    vacmap.save("./vacmap.png")
