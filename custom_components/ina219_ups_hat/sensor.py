"""INA219 UPS Hat sensors"""

from homeassistant.components.sensor.const import SensorDeviceClass, SensorStateClass
from homeassistant import core
from homeassistant.components.sensor import SensorEntity, PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIQUE_ID,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTime,
    UnitOfEnergy,
)

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.helpers.entity_platform import AddEntitiesCallback
import logging
import voluptuous as vol

from .entity import INA219UpsHatEntity
from .coordinator import INA219UpsHatCoordinator
from .const import (
    CONF_ADDR,
    CONF_BATTERIES_COUNT,
    CONF_BATTERY_CAPACITY,
    CONF_MAX_SOC,
    CONF_SCAN_INTERVAL,
    CONF_SMA_SAMPLES,
    CONF_MIN_ONLINE_CURRENT,
    CONF_MIN_CHARGING_CURRENT,
    DEFAULT_NAME,
    DOMAIN,
)


_LOGGER = logging.getLogger(__name__)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_ADDR): cv.string,
        vol.Optional(CONF_MAX_SOC, default=91): cv.positive_int,
        vol.Optional(CONF_BATTERY_CAPACITY, 9000): cv.positive_int,
        vol.Optional(CONF_BATTERIES_COUNT, default=3): cv.positive_int,
        vol.Optional(CONF_SMA_SAMPLES, default=5): cv.positive_int,
        vol.Optional(CONF_MIN_ONLINE_CURRENT, default=-100): int,
        vol.Optional(CONF_MIN_CHARGING_CURRENT, default=50): cv.positive_int,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)


async def async_setup_platform(
    hass: core.HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    # We only want this platform to be set up via discovery.
    if discovery_info is None:
        return

    coordinator = discovery_info.get("coordinator")

    sensors = [
        VoltageSensor(coordinator),
        CurrentSensor(coordinator),
        PowerSensor(coordinator),
        SocSensor(coordinator),
        RemainingCapacitySensor(coordinator),
        RemainingTimeSensor(coordinator),
    ]
    async_add_entities(sensors)


class INA219UpsHatSensor(INA219UpsHatEntity, SensorEntity):
    """Base sensor"""

    def __init__(self, coordinator: INA219UpsHatCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_suggested_display_precision = 2


class VoltageSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Voltage"
        self._attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
        self._attr_device_class = SensorDeviceClass.VOLTAGE

    @property
    def native_value(self):
        return self._coordinator.data["voltage"]


class CurrentSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Current"
        self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
        self._attr_device_class = SensorDeviceClass.CURRENT

    @property
    def native_value(self):
        return self._coordinator.data["current"]


class PowerSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Power"
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER

    @property
    def native_value(self):
        return self._coordinator.data["power"]


class SocSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "SoC"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self):
        return self._coordinator.data["soc"]


class RemainingCapacitySensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Remaining Capacity"
        self._attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
        self._attr_device_class = SensorDeviceClass.ENERGY_STORAGE
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        return self._coordinator.data["remaining_battery_capacity"]


class RemainingTimeSensor(INA219UpsHatSensor):
    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._name = "Remaining Time"
        self._attr_native_unit_of_measurement = UnitOfTime.HOURS
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_suggested_display_precision = 0

    @property
    def native_value(self):
        return self._coordinator.data["remaining_time"]
