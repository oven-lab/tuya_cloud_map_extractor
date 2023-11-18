from __future__ import annotations

import logging
from typing import Any
from .tuya_vacuum_map_extractor import (
    get_map,
    debug_file,
    ClientIDError,
    ClientSecretError,
    DeviceIDError,
    ServerError,
)

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_NAME,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DEVICE_ID,
)

import voluptuous as vol

from .const import (
    DOMAIN,
    CONF_SERVER,
    CONF_SERVER_CHINA,
    CONF_SERVER_WEST_AMERICA,
    CONF_SERVER_EAST_AMERICA,
    CONF_SERVER_CENTRAL_EUROPE,
    CONF_SERVER_WEST_EUROPE,
    CONF_SERVER_INDIA,
)

CONF_SERVERS = {
    CONF_SERVER_CHINA: "China",
    CONF_SERVER_WEST_AMERICA: "Western America",
    CONF_SERVER_EAST_AMERICA: "Eastern America",
    CONF_SERVER_CENTRAL_EUROPE: "Central Europe",
    CONF_SERVER_WEST_EUROPE: "Western Europe",
    CONF_SERVER_INDIA: "India",
}

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        default_server = CONF_SERVER_CENTRAL_EUROPE
        default_name = "Vacuum map"
        default_client_id = ""
        default_client_secret = ""
        default_device_id = ""

        errors = {}
        if user_input is not None:
            try:
                info = await validate(self.hass, user_input)
                return self.async_create_entry(
                    title=user_input.pop(CONF_NAME), data=user_input
                )
            except ClientIDError:
                errors[CONF_CLIENT_ID] = "client_id"
            except ClientSecretError:
                errors[CONF_CLIENT_SECRET] = "client_secret"
            except DeviceIDError:
                errors[CONF_DEVICE_ID] = "device_id"
            except ServerError:
                errors[CONF_SERVER] = "server"
            except Exception as error:
                _LOGGER.exception(error)
                errors["base"] = "unknown"

            default_name = user_input["name"]
            default_client_id = user_input["client_id"]
            default_client_secret = user_input["client_secret"]
            default_device_id = user_input["device_id"]
            default_server = user_input["server"]

        DATA_SCHEMA = {
            vol.Required(CONF_NAME, default=default_name): str,
            vol.Required(CONF_SERVER, default=default_server): vol.In(CONF_SERVERS),
            vol.Required(CONF_CLIENT_ID, default=default_client_id): str,
            vol.Required(CONF_CLIENT_SECRET, default=default_client_secret): str,
            vol.Required(CONF_DEVICE_ID, default=default_device_id): str,
        }

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(DATA_SCHEMA), errors=errors
        )


async def validate(hass: HomeAssistant, data: dict):
    """Validate the user input"""
    await hass.async_add_executor_job(
        get_map,
        data["server"],
        data["client_id"],
        data["client_secret"],
        data["device_id"],
    )

async def get_file(hass: HomeAssistant, data: dict):
    return await hass.async_add_executor_job(
        debug_file,
        data["server"],
        data["client_id"],
        data["client_secret"],
        data["device_id"]
    )
