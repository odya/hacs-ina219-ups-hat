"""INA219 UPS Hat binary_sensors"""
from __future__ import annotations
from .coordinator import INA219UpsHatCoordinator
from .entity import INA219UpsHatEntity
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up binary sensor platform."""
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    sensors = [
        OnlineBinarySensor(coordinator),
        ChargingBinarySensor(coordinator),
    ]

    async_add_entities(sensors)


class INA219UpsHatBinarySensor(INA219UpsHatEntity, BinarySensorEntity):
    """Base binary sensor"""

    def __init__(self, coordinator: INA219UpsHatCoordinator) -> None:
        super().__init__(coordinator)


class OnlineBinarySensor(INA219UpsHatBinarySensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Online"
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        return self._coordinator.data["online"]


class ChargingBinarySensor(INA219UpsHatBinarySensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        return self._coordinator.data["charging"]
