"""Event platform for OpenClaw Control."""
from __future__ import annotations

from homeassistant.components.event import EventEntity, EventEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, EVENT_LIFECYCLE
from .coordinator import OpenClawCoordinator

EVENT_TYPES = [
    "evolution_started",
    "evolution_completed", 
    "error_encountered",
    "skill_loaded",
    "cycle_complete",
]

EVENT_DESCRIPTIONS = [
    EventEntityDescription(
        key=EVENT_LIFECYCLE,
        name="Lifecycle Events",
        event_types=EVENT_TYPES,
        icon="mdi:lightning-bolt",
        translation_key="lifecycle",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up event entities."""
    coordinator: OpenClawCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        OpenClawLifecycleEvent(coordinator, desc, entry.entry_id)
        for desc in EVENT_DESCRIPTIONS
    ]
    
    async_add_entities(entities)


class OpenClawLifecycleEvent(CoordinatorEntity, EventEntity):
    """OpenClaw lifecycle event entity."""

    def __init__(self, coordinator, description, entry_id):
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
            "model": "OpenClaw Master Control",
        }
        self._event_data: dict | None = None

    @property
    def event_types(self) -> list[str]:
        return EVENT_TYPES

    @property
    def extra_state_attributes(self) -> dict:
        """Return current event data."""
        return self._event_data or {}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        data = self.coordinator.data
        if data and "lifecycle_event" in data:
            event = data["lifecycle_event"]
            self._trigger_event(
                event_type=event["type"],
                event_data=event.get("data", {}),
            )
            self._event_data = event.get("data", {})
        super()._handle_coordinator_update()
