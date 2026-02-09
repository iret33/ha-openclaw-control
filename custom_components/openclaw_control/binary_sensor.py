"""Binary sensor platform."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BINARY_SENSOR_UPDATE, BINARY_SENSOR_ONLINE
from .coordinator import OpenClawCoordinator

BINARY_SENSORS = [
    BinarySensorEntityDescription(
        key=BINARY_SENSOR_UPDATE,
        name="Update Available",
        device_class=BinarySensorDeviceClass.UPDATE,
    ),
    BinarySensorEntityDescription(
        key=BINARY_SENSOR_ONLINE,
        name="Nexus Online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    coordinator: OpenClawCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        OpenClawBinarySensor(coordinator, desc, entry.entry_id)
        for desc in BINARY_SENSORS
    ]
    async_add_entities(entities)


class OpenClawBinarySensor(CoordinatorEntity[OpenClawCoordinator], BinarySensorEntity):
    """OpenClaw binary sensor."""

    def __init__(self, coordinator: OpenClawCoordinator, description: BinarySensorEntityDescription, entry_id: str) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
        }

    @property
    def is_on(self) -> bool:
        data = self.coordinator.data
        if data is None:
            return False
            
        if self.entity_description.key == BINARY_SENSOR_UPDATE:
            return data.get("update_available", False)
        elif self.entity_description.key == BINARY_SENSOR_ONLINE:
            return data.get("online", False)
        return False
