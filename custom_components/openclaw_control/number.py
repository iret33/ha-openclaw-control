"""Number platform for OpenClaw Control."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NUMBER_THINKING_DEPTH
from .coordinator import OpenClawCoordinator

NUMBERS = [
    NumberEntityDescription(
        key=NUMBER_THINKING_DEPTH,
        name="Thinking Depth",
        icon="mdi:brain",
        native_min_value=1,
        native_max_value=5,
        native_step=1,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    coordinator: OpenClawCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        OpenClawThinkingDepthNumber(coordinator, desc, entry.entry_id)
        for desc in NUMBERS
    ]
    async_add_entities(entities)


class OpenClawThinkingDepthNumber(CoordinatorEntity[OpenClawCoordinator], NumberEntity):
    """Thinking depth control number."""

    def __init__(self, coordinator: OpenClawCoordinator, description: NumberEntityDescription, entry_id: str) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
            "model": "OpenClaw Master Control",
        }
        self._attr_native_value = 3  # Default balanced thinking

    @property
    def native_value(self) -> float:
        """Return current thinking depth."""
        if self.coordinator.data and "thinking_depth" in self.coordinator.data:
            return float(self.coordinator.data["thinking_depth"])
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        """Set new thinking depth value."""
        level = int(value)
        self._attr_native_value = level
        await self.coordinator.async_set_thinking_depth(level)
