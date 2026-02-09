"""Button platform for OpenClaw Control."""
from __future__ import annotations

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BUTTON_DIAGNOSTIC, BUTTON_EVOLVE
from .coordinator import OpenClawCoordinator

BUTTONS = [
    ButtonEntityDescription(
        key=BUTTON_DIAGNOSTIC,
        name="Run Diagnostics",
        icon="mdi:stethoscope",
    ),
    ButtonEntityDescription(
        key=BUTTON_EVOLVE,
        name="Trigger Evolution",
        icon="mdi:dna",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up buttons."""
    coordinator: OpenClawCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        OpenClawButton(coordinator, desc, entry.entry_id)
        for desc in BUTTONS
    ]
    async_add_entities(entities)


class OpenClawButton(CoordinatorEntity[OpenClawCoordinator], ButtonEntity):
    """OpenClaw button."""

    def __init__(self, coordinator: OpenClawCoordinator, description: ButtonEntityDescription, entry_id: str) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
        }

    async def async_press(self) -> None:
        """Handle button press."""
        if self.entity_description.key == BUTTON_DIAGNOSTIC:
            self.coordinator.set_evolution_thought("Running self-diagnostics...")
        elif self.entity_description.key == BUTTON_EVOLVE:
            self.coordinator.set_evolution_thought("Manually triggered evolution cycle")
