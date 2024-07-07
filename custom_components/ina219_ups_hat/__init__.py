"""INA219 UPS Hat"""
from __future__ import annotations
from datetime import timedelta
import json

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.discovery import async_load_platform

from .coordinator import INA219UpsHatCoordinator

from .const import CONF_SCAN_INTERVAL, DOMAIN


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Your controller/hub specific code."""

    if DOMAIN not in config:
        return False

    sensor_config: ConfigType = config[DOMAIN]

    if CONF_SCAN_INTERVAL not in sensor_config:
        return False
    sensor_config[CONF_SCAN_INTERVAL] = timedelta(seconds=sensor_config[CONF_SCAN_INTERVAL])

    coordinator = INA219UpsHatCoordinator(hass, sensor_config)
    await coordinator.async_refresh()

    await async_load_platform(hass, 'sensor', DOMAIN, {
        "coordinator": coordinator
    }, sensor_config)

    await async_load_platform(hass, 'binary_sensor', DOMAIN, {
        "coordinator": coordinator
    }, sensor_config)

    async def async_update_data(now):
        await coordinator.async_request_refresh()

    i = sensor_config.get(CONF_SCAN_INTERVAL)
    async_track_time_interval(hass, async_update_data,
                              sensor_config.get(CONF_SCAN_INTERVAL))

    return True