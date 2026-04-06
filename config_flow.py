import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD


class ZTERouterMeshConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="ZTE Router Mesh",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME, default="admin"): str,
                vol.Required(CONF_PASSWORD): str,
            }),
        )
