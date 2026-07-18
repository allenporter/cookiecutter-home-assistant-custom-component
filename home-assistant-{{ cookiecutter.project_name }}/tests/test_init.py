"""Tests for the {{ cookiecutter.domain }} component."""

import pytest

from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
)


@pytest.fixture(autouse=True)
def mock_setup_integration(config_entry: MockConfigEntry) -> None:
    """Setup the integration"""
