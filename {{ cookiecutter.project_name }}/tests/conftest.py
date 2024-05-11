"""Fixtures for the custom component."""

from collections.abc import Generator
import logging
from unittest.mock import patch

import pytest

from homeassistant.const import Platform, CONF_DEVICE_ID
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from homeassistant.helpers import device_registry as dr

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)

from custom_components.{{ cookiecutter.project_name }}.const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None, None, None]:
    """Enable custom integration."""
    _ = enable_custom_integrations  # unused
    yield


@pytest.fixture(name="platforms")
def mock_platforms() -> list[Platform]:
    """Fixture for platforms loaded by the integration."""
    return []


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: HomeAssistant,
    config_entry: MockConfigEntry,
    platforms: list[Platform],
) -> None:
    """Set up the integration."""

    with patch(f"custom_components.{DOMAIN}.PLATFORMS", platforms):
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
        yield


@pytest.fixture(name="config_entry")
async def mock_config_entry(
    hass: HomeAssistant, zwave_device_id: str
) -> MockConfigEntry:
    """Fixture to create a configuration entry."""
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={},
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
