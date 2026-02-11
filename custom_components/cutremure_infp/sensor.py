"""Sensor platform for Cutremure INFP."""
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    ATTR_ATTRIBUTION,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import CutremureCoordinator
from .const import DOMAIN, CONF_MAGNITUDE_THRESHOLD

_LOGGER = logging.getLogger(__name__)

ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"
ATTR_MAGNITUDE = "magnitude"
ATTR_DEPTH = "depth"
ATTR_TIME = "time"
ATTR_LOCATION = "location"
ATTR_EVENT_TYPE = "event_type"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator: CutremureCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = [
        CutremureSensor(
            coordinator,
            config_entry,
            "Latest Earthquake",
            "latest_earthquake",
        ),
        CutremureDetailsSensor(
            coordinator,
            config_entry,
            "Earthquake Magnitude",
            "magnitude",
        ),
        CutremureDetailsSensor(
            coordinator,
            config_entry,
            "Earthquake Depth",
            "depth",
        ),
    ]

    async_add_entities(sensors)


class CutremureSensor(CoordinatorEntity, SensorEntity):
    """Sensor for latest earthquake."""

    def __init__(
        self,
        coordinator: CutremureCoordinator,
        config_entry: ConfigEntry,
        name: str,
        key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_attribution = "Data provided by INFP"

    @property
    def native_value(self) -> Optional[str]:
        """Return the state of the sensor."""
        if self.coordinator.data and len(self.coordinator.data) > 0:
            earthquake = self.coordinator.data[0]
            return f"{earthquake.get('locstring', 'N/A')} - Mag: {earthquake.get('mag', 'N/A')}"
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes for the sensor."""
        if not self.coordinator.data or len(self.coordinator.data) == 0:
            return {}

        earthquake = self.coordinator.data[0]

        return {
            ATTR_LOCATION: earthquake.get("locstring"),
            ATTR_MAGNITUDE: float(earthquake.get("mag", 0)),
            ATTR_DEPTH: float(earthquake.get("depth", 0)),
            ATTR_LATITUDE: float(earthquake.get("lat", 0)),
            ATTR_LONGITUDE: float(earthquake.get("lon", 0)),
            ATTR_TIME: earthquake.get("time"),
            ATTR_EVENT_TYPE: earthquake.get("event_type"),
            ATTR_ATTRIBUTION: "INFP - Institutul Național pentru Fizica Pământului",
        }

    @property
    def icon(self) -> str:
        """Return the icon for the sensor."""
        return "mdi:alert"

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None


class CutremureDetailsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for earthquake details."""

    def __init__(
        self,
        coordinator: CutremureCoordinator,
        config_entry: ConfigEntry,
        name: str,
        key: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{key}"
        self._attr_attribution = "Data provided by INFP"

        if key == "magnitude":
            self._attr_icon = "mdi:gauge"
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif key == "depth":
            self._attr_icon = "mdi:earth"
            self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if self.coordinator.data and len(self.coordinator.data) > 0:
            earthquake = self.coordinator.data[0]
            if self._key == "magnitude":
                return float(earthquake.get("mag", 0))
            elif self._key == "depth":
                return float(earthquake.get("depth", 0))
        return None

    @property
    def native_unit_of_measurement(self) -> Optional[str]:
        """Return the unit of measurement."""
        if self._key == "magnitude":
            return ""
        elif self._key == "depth":
            return "km"
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra attributes for the sensor."""
        if not self.coordinator.data or len(self.coordinator.data) == 0:
            return {}

        earthquake = self.coordinator.data[0]

        return {
            ATTR_LOCATION: earthquake.get("locstring"),
            ATTR_TIME: earthquake.get("time"),
            ATTR_LATITUDE: float(earthquake.get("lat", 0)),
            ATTR_LONGITUDE: float(earthquake.get("lon", 0)),
            ATTR_ATTRIBUTION: "INFP - Institutul Național pentru Fizica Pământului",
        }

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None
