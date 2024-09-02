"""INA219 UPS Hat coordinator."""

import logging

from homeassistant import core
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_ADDR,
    CONF_BATTERIES_COUNT,
    CONF_BATTERY_CAPACITY,
    CONF_MAX_SOC,
    CONF_MIN_CHARGING_CURRENT,
    CONF_MIN_ONLINE_CURRENT,
    CONF_SMA_SAMPLES,
    DEFAULT_OCV,
)
from .ina219.config import get_ina219_class
from .ina219_wrapper import INA219Wrapper
from .soc.provider import SocOcvProvider

_LOGGER = logging.getLogger(__name__)


class INA219UpsHatCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: core.HomeAssistant, config: ConfigType) -> None:
        """Initialize coordinator."""

        self.name_prefix = config.get(CONF_NAME)
        self.id_prefix = config.get(CONF_UNIQUE_ID)

        self._addr = config.get(CONF_ADDR)
        self._max_soc = config.get(CONF_MAX_SOC)
        self._battery_capacity = config.get(CONF_BATTERY_CAPACITY)
        self._batteries_count = config.get(CONF_BATTERIES_COUNT)
        self._sma_samples = config.get(CONF_SMA_SAMPLES)
        self._min_online_current = config.get(CONF_MIN_ONLINE_CURRENT)
        self._min_charging_current = config.get(CONF_MIN_CHARGING_CURRENT)

        INA219 = get_ina219_class()
        self._ina219 = INA219(addr=int(self._addr))
        self._ina219_wrapper = INA219Wrapper(self._ina219, self._sma_samples)

        self._socOcvProvider = SocOcvProvider(hass, DEFAULT_OCV)

        super().__init__(
            hass,
            _LOGGER,
            name="ina219_ups_hat",
            update_method=self._update_data,
        )

    async def _update_data(self):
        try:
            ina219_wrapper = self._ina219_wrapper
            ina219_wrapper.measureINAValues()

            bus_voltage = (
                ina219_wrapper.getBusVoltageSMA_V()
            )  # voltage on V- (load side)
            shunt_voltage = (
                ina219_wrapper.getShuntVoltageSMA_mV() / 1000
            )  # voltage between V+ and V- across the shunt
            total_voltage = bus_voltage + shunt_voltage
            current = ina219_wrapper.getCurrentSMA_mA()  # current in mA
            # power = ina219_wrapper.getPowerSMA_W()  # power in W

            smooth_bus_voltage = ina219_wrapper.getBusVoltageSMAx2_V()
            # smooth_current = ina219_wrapper.getCurrentSMAx2_mA()

            soc = self._socOcvProvider.get_soc_from_voltage(
                smooth_bus_voltage / self._batteries_count
            )

            power_calculated = bus_voltage * (current / 1000)

            current_lowres = round(current / 1000, 2) * 1000  # current in mA
            online = bool(current_lowres > self._min_online_current)
            charging = bool(current_lowres > self._min_charging_current)

            if self._battery_capacity is None:
                remaining_battery_capacity = None
                remaining_time = None
            else:
                remaining_battery_capacity = (self._battery_capacity / 100.0) * soc
                remaining_battery_capacity = (self._battery_capacity / 100.0) * soc
                if not online:
                    remaining_time = round(
                        10
                        * (remaining_battery_capacity / 1000)
                        / -(bus_voltage * (current / 1000)),  # Smooth power
                        3,
                    )
                else:
                    remaining_time = None

            return {
                "voltage": round(total_voltage, 2),
                "current": round(current / 1000, 2),
                "power": round(power_calculated, 2),
                "soc": round(soc, 1),
                "remaining_battery_capacity": round(
                    (remaining_battery_capacity * total_voltage) / 1000, 2
                ),  # in Wh
                "remaining_time": remaining_time,
                "online": online,
                "charging": charging,
            }
        except Exception as e:
            raise UpdateFailed(f"Error updating data: {e}")
