import logging
import requests
from datetime import timedelta
from bs4 import BeautifulSoup

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ZTERouterClient:
    def __init__(self, host, username, password):
        self.base_url = f"http://{host}"
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self):
        url = f"{self.base_url}/login"

        data = {
            "username": self.username,
            "password": self.password,
        }

        r = self.session.post(url, data=data, timeout=5)
        return r.status_code == 200

    def fetch(self):
        if not self.login():
            _LOGGER.error("Login failed")
            return []

        url = f"{self.base_url}/status"

        r = self.session.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        devices = []

        rows = soup.select("table tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            devices.append({
                "name": cols[0].text.strip(),
                "mac": cols[1].text.strip(),
                "ipv4": cols[2].text.strip(),
                "ipv6": cols[3].text.strip(),
                "port": cols[4].text.strip(),
            })

        return devices


class ZTECoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client):
        super().__init__(
            hass,
            _LOGGER,
            name="zte_router_mesh",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(self.client.fetch)
