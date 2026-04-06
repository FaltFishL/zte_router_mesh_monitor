from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import ZTERouterClient, ZTECoordinator
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD


async def async_setup_entry(hass, config_entry, async_add_entities):
    config = config_entry.data

    client = ZTERouterClient(
        config[CONF_HOST],
        config[CONF_USERNAME],
        config[CONF_PASSWORD],
    )

    coordinator = ZTECoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        ZTERouterSensor(coordinator)
    ])


class ZTERouterSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "ZTE Router Mesh Devices"

    @property
    def state(self):
        return len(self.coordinator.data)

    @property
    def extra_state_attributes(self):
        return {
            "devices": self.coordinator.data
        }
