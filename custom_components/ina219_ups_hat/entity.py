"""INA219 UPS Hat entity."""

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN
from .coordinator import INA219UpsHatCoordinator


class INA219UpsHatEntity:
    """INA219 UPS Hat entity."""

    def __init__(self, coordinator: INA219UpsHatCoordinator) -> None:
        self._coordinator = coordinator
        self._device_id = self._coordinator.id_prefix
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.id_prefix)},
            name=coordinator.name_prefix,
            manufacturer="Some Chinese factory",
        )

    @property
    def name(self):
        return self._coordinator.name_prefix + " " + self.name

    @property
    def unique_id(self):
        return self._coordinator.id_prefix + "_" + self.name

    async def async_update(self):
        await self._coordinator.async_request_refresh()
