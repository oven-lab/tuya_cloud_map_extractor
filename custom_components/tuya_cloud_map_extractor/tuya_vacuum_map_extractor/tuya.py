import datetime
import hmac
import requests

from .const import ServerError, ClientIDError, ClientSecretError, DeviceIDError

def _get_sign(client_id: str, secret_key: str, url: str, t: int, token: str):
    empty_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    signstr = client_id + token + t + "GET" + "\n" + empty_hash + "\n" + "" + "\n" + url
    return hmac.new(
        secret_key.encode(), msg=signstr.encode(), digestmod="sha256"
    ).hexdigest()

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

def get_download_link(
    server: str, client_id: str, secret_key: str, device_id: str
) -> str:
    """Gets the download link of the real time map."""

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

    return response
