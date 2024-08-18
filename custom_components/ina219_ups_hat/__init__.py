"""INA219 UPS Hat."""

from __future__ import annotations

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, Platform
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ADDR,
    CONF_BATTERIES_COUNT,
    CONF_BATTERY_CAPACITY,
    CONF_MAX_SOC,
    CONF_MIN_CHARGING_CURRENT,
    CONF_MIN_ONLINE_CURRENT,
    CONF_SCAN_INTERVAL,
    CONF_SMA_SAMPLES,
    DEFAULT_NAME,
    DEFAULT_UNIQUE_ID,
    DOMAIN,
)
from .coordinator import INA219UpsHatCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ADDR): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_UNIQUE_ID, default=DEFAULT_UNIQUE_ID): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=60): int,
                vol.Optional(CONF_MAX_SOC, default=91): cv.positive_int,
                vol.Optional(CONF_BATTERY_CAPACITY, default=3000): cv.positive_int,
                vol.Optional(CONF_BATTERIES_COUNT, default=3): cv.positive_int,
                vol.Optional(CONF_SMA_SAMPLES, default=5): cv.positive_int,
                vol.Optional(CONF_MIN_ONLINE_CURRENT, default=-100): int,
                vol.Optional(CONF_MIN_CHARGING_CURRENT, default=55): cv.positive_int,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, global_config: ConfigType) -> bool:
    """Your controller/hub specific code."""

    if DOMAIN not in global_config:
        return False

    config: ConfigType = global_config[DOMAIN]

    if CONF_SCAN_INTERVAL not in config:
        return False
    config[CONF_SCAN_INTERVAL] = timedelta(seconds=config[CONF_SCAN_INTERVAL])

    coordinator = INA219UpsHatCoordinator(hass, config)
    await coordinator.async_refresh()

    await async_load_platform(
        hass, "sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    await async_load_platform(
        hass, "binary_sensor", DOMAIN, {"coordinator": coordinator}, config
    )

    async def async_update_data(now):
        await coordinator.async_request_refresh()

    async_track_time_interval(hass, async_update_data, config.get(CONF_SCAN_INTERVAL))

    return True
