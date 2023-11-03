
from .const import DOMAIN
from .coordinator import INA219UpsHatCoordinator
from homeassistant.helpers.device_registry import DeviceInfo


class INA219UpsHatEntity():
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
        return self._coordinator.name_prefix + ' ' + self._name

    @property
    def unique_id(self):
        return self._coordinator.id_prefix + '_' + self._name

    async def async_update(self):
        await self._coordinator.async_request_refresh()
