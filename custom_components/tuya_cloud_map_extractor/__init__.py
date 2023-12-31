"""Tuya cloud map extractor."""

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

PLATFORMS = [Platform.CAMERA]

from .const import (
    DOMAIN,
    CONF_PATH,
    CONF_LAST,
    CONF_ROTATE,
    CONF_ROTATE_0,
    CONF_FLIP_HORIZONTAL,
    CONF_FLIP_VERTICAL,
)
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up epson from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )

    return unload_ok

async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        data = {**config_entry.data}
        data[CONF_PATH] = True
        data[CONF_ROTATE] = CONF_ROTATE_0
        data[CONF_FLIP_HORIZONTAL] = False
        data[CONF_FLIP_VERTICAL] = False

        hass.config_entries.async_update_entry(config_entry, data=data)

    if config_entry.version == 2:
        data = config_entry.data
        data = {**config_entry.data}
        data[CONF_ROTATE] = CONF_ROTATE_0
        data[CONF_FLIP_HORIZONTAL] = False
        data[CONF_FLIP_VERTICAL] = False

        hass.config_entries.async_update_entry(config_entry, data=data)

    _LOGGER.debug("Migration to version %s successful", config_entry.version)

    return True

async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry):
    """Handle options update."""

    if not await async_unload_entry(hass, config_entry):
        return

    data = {**config_entry.data}
    options = {**config_entry.options}

    data[CONF_PATH] = options[CONF_PATH]
    data[CONF_LAST] = options[CONF_LAST]
    data[CONF_ROTATE] = options[CONF_ROTATE]
    data[CONF_FLIP_HORIZONTAL] = options[CONF_FLIP_HORIZONTAL]
    data[CONF_FLIP_VERTICAL] = options[CONF_FLIP_VERTICAL]

    hass.config_entries.async_update_entry(config_entry, data=data)
    await async_setup_entry(hass, config_entry)
