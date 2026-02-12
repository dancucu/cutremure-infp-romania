"""The Cutremure INFP integration."""
import asyncio
import logging
from datetime import timedelta
from typing import Optional

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cutremure_infp"
DEFAULT_SCAN_INTERVAL = 60  # seconds
API_URL = "https://fastapi.infp.ro/v1/?product=shakemap4"
PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cutremure INFP from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = CutremureCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class CutremureCoordinator(DataUpdateCoordinator):
    """Coordinator for Cutremure INFP."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.config_entry = config_entry
        self._last_earthquake_id: Optional[str] = None
        
        scan_interval = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self):
        """Fetch data from the API."""
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(API_URL, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    raise UpdateFailed(f"API returned status {response.status}")

                data = await response.json()

                if not isinstance(data, list) or len(data) == 0:
                    raise UpdateFailed("Invalid API response format")

                return data

        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout fetching data: {err}") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
