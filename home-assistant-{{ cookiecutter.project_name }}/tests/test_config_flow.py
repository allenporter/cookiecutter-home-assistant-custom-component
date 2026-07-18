"""Tests for the config flow."""

from unittest.mock import patch


from homeassistant import config_entries
from homeassistant.const import (
    CONF_DEVICE_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import device_registry as dr

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.{{ cookiecutter.domain }}.const import DOMAIN


async def test_select_device(
    hass: HomeAssistant,
    zwave_device_id: str,
) -> None:
    """Test selecting a device in the configuration flow."""
    # Create a mock zwave_js config entry to link the device to
    zwave_entry = MockConfigEntry(
        domain="zwave_js",
        data={},
    )
    zwave_entry.add_to_hass(hass)

    # Create a device in the registry so that it can be found by config_flow
    device_registry = dr.async_get(hass)
    device_entry = device_registry.async_get_or_create(
        config_entry_id=zwave_entry.entry_id,
        identifiers={("zwave_js", zwave_device_id)},
        name="Device name",
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") is None

    with patch(
        f"custom_components.{DOMAIN}.async_setup_entry", return_value=True
    ) as mock_setup:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_DEVICE_ID: device_entry.id,
            },
        )
        await hass.async_block_till_done()

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == "Device name"
    assert result.get("data") == {}
    assert result.get("options") == {
        CONF_DEVICE_ID: device_entry.id,
    }
    assert len(mock_setup.mock_calls) == 1
