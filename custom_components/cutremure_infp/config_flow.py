"""Config flow for Cutremure INFP integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_MAGNITUDE_THRESHOLD

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_MAGNITUDE_THRESHOLD, default=3.0): vol.All(
            vol.Coerce(float), vol.Range(min=0.0, max=10.0)
        ),
        vol.Optional(CONF_SCAN_INTERVAL, default=60): vol.All(
            vol.Coerce(int), vol.Range(min=10, max=3600)
        ),
    }
)


class CutremureConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Cutremure INFP."""

    VERSION = 1
    DOMAIN = DOMAIN

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title="Cutremure INFP", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> "CutremureOptionsFlow":
        """Create the options flow."""
        return CutremureOptionsFlow(config_entry)


class CutremureOptionsFlow(config_entries.OptionFlow):
    """Handle options for Cutremure INFP."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_MAGNITUDE_THRESHOLD,
                    default=self.config_entry.options.get(
                        CONF_MAGNITUDE_THRESHOLD, 3.0
                    ),
                ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=10.0)),
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, 60),
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=3600)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
