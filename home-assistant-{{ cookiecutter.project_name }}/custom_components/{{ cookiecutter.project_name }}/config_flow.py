"""Config flow for {{ cookiecutter.project_name }} integration."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_DEVICE_ID
from homeassistant.helpers import device_registry as dr, selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaConfigFlowHandler,
    SchemaFlowFormStep,
)

from .const import DOMAIN


CONFIG_FLOW = {
    "user": SchemaFlowFormStep(
        vol.Schema(
            {
                vol.Required(CONF_DEVICE_ID): selector.DeviceSelector(
                    selector.DeviceSelectorConfig(integration="zwave_js")
                ),
            }
        )
    )
}

OPTIONS_FLOW = {
    "init": SchemaFlowFormStep(),
}


class {{ cookiecutter.name.split('-')|map('capitalize')|join }}ConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle a config flow for Switch as X."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    VERSION = 1
    MINOR_VERSION = 1

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return config entry title."""
        registry = dr.async_get(self.hass)
        device_entry = registry.async_get(options[CONF_DEVICE_ID])
        return device_entry.name_by_user or device_entry.name
