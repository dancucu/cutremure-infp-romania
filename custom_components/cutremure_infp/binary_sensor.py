"""Binary sensor platform for Cutremure INFP."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CutremureCoordinator
from .const import DOMAIN, CONF_MAGNITUDE_THRESHOLD

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensor platform."""
    coordinator: CutremureCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    binary_sensor = CutremureNotificationSensor(coordinator, config_entry)
    async_add_entities([binary_sensor])


class CutremureNotificationSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor that triggers when earthquake magnitude threshold is exceeded."""

    _attr_device_class = BinarySensorDeviceClass.MOTION
    _attr_icon = "mdi:alert"

    def __init__(
        self,
        coordinator: CutremureCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "Earthquake Alert"
        self._attr_unique_id = f"{DOMAIN}_alert"
        self._attr_attribution = "Data provided by INFP"
        self._last_earthquake_id: Optional[str] = None

    @property
    def is_on(self) -> bool:
        """Return True if earthquake magnitude exceeds the threshold."""
        if not self.coordinator.data or len(self.coordinator.data) == 0:
            return False

        earthquake = self.coordinator.data[0]
        magnitude_threshold = self._config_entry.options.get(
            CONF_MAGNITUDE_THRESHOLD, 3.0
        )

        magnitude = float(earthquake.get("mag", 0))

        return magnitude >= magnitude_threshold

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes for the sensor."""
        if not self.coordinator.data or len(self.coordinator.data) == 0:
            return {}

        earthquake = self.coordinator.data[0]
        magnitude_threshold = self._config_entry.options.get(
            CONF_MAGNITUDE_THRESHOLD, 3.0
        )

        return {
            "magnitude": float(earthquake.get("mag", 0)),
            "magnitude_threshold": magnitude_threshold,
            "location": earthquake.get("locstring"),
            "depth": float(earthquake.get("depth", 0)),
            "time": earthquake.get("time"),
            "latitude": float(earthquake.get("lat", 0)),
            "longitude": float(earthquake.get("lon", 0)),
            "attribution": "INFP - Institutul Național pentru Fizica Pământului",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None
