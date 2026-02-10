"""Sensor platform for OpenClaw Control."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN, SENSOR_STATUS, SENSOR_NEXT_TASKS, SENSOR_SKILLS,
    SENSOR_CYCLE_COUNT, SENSOR_EVOLUTION_LOG, SENSOR_MEMORY_USAGE
)
from .coordinator import OpenClawCoordinator

SENSORS = [
    SensorEntityDescription(
        key=SENSOR_STATUS,
        name="OpenClaw Status",
        icon="mdi:brain",
    ),
    SensorEntityDescription(
        key=SENSOR_CYCLE_COUNT,
        name="Evolution Cycles",
        icon="mdi:counter",
    ),
    SensorEntityDescription(
        key=SENSOR_EVOLUTION_LOG,
        name="Current Evolution",
        icon="mdi:lightbulb",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    coordinator: OpenClawCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        OpenClawStatusSensor(coordinator, desc, entry.entry_id)
        for desc in SENSORS
    ]
    entities.append(OpenClawNextTasksSensor(coordinator, entry.entry_id))
    entities.append(OpenClawSkillsSensor(coordinator, entry.entry_id))
    entities.append(OpenClawMemoryUsageSensor(coordinator, entry.entry_id))
    
    async_add_entities(entities)


class OpenClawStatusSensor(CoordinatorEntity[OpenClawCoordinator], SensorEntity):
    """OpenClaw status sensor."""

    def __init__(self, coordinator: OpenClawCoordinator, description: SensorEntityDescription, entry_id: str) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
            "model": "OpenClaw Master Control",
        }

    @property
    def native_value(self) -> str | int | None:
        data = self.coordinator.data
        if data is None:
            return None
            
        if self.entity_description.key == SENSOR_STATUS:
            return data.get(SENSOR_STATUS)
        elif self.entity_description.key == SENSOR_CYCLE_COUNT:
            return data.get(SENSOR_CYCLE_COUNT, 0)
        elif self.entity_description.key == SENSOR_EVOLUTION_LOG:
            return data.get("evolution_thought", "Thinking...")
        return None


class OpenClawNextTasksSensor(CoordinatorEntity[OpenClawCoordinator], SensorEntity):
    """Next scheduled tasks sensor."""

    def __init__(self, coordinator: OpenClawCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{SENSOR_NEXT_TASKS}"
        self._attr_name = "Next Tasks"
        self._attr_icon = "mdi:calendar-clock"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
        }

    @property
    def native_value(self) -> str:
        data = self.coordinator.data
        if data and SENSOR_NEXT_TASKS in data:
            tasks = data[SENSOR_NEXT_TASKS]
            return f"{len(tasks)} scheduled"
        return "Unknown"

    @property
    def extra_state_attributes(self) -> dict[str, list[str]]:
        data = self.coordinator.data
        if data and SENSOR_NEXT_TASKS in data:
            tasks = data[SENSOR_NEXT_TASKS]
            return {"tasks": [t["name"] for t in tasks[:3]]}
        return {}


class OpenClawSkillsSensor(CoordinatorEntity[OpenClawCoordinator], SensorEntity):
    """Active skills sensor."""

    def __init__(self, coordinator: OpenClawCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{SENSOR_SKILLS}"
        self._attr_name = "Active Skills"
        self._attr_icon = "mdi:puzzle"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
        }

    @property
    def native_value(self) -> int:
        data = self.coordinator.data
        if data and SENSOR_SKILLS in data:
            return data[SENSOR_SKILLS].get("count", 0)
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, list[str]]:
        data = self.coordinator.data
        if data and SENSOR_SKILLS in data:
            return {"skills": data[SENSOR_SKILLS].get("list", [])}
        return {}


class OpenClawMemoryUsageSensor(CoordinatorEntity[OpenClawCoordinator], SensorEntity):
    """Memory usage sensor for Agent Health monitoring."""

    def __init__(self, coordinator: OpenClawCoordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_{SENSOR_MEMORY_USAGE}"
        self._attr_name = "Memory Usage"
        self._attr_icon = "mdi:memory"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "OpenClaw Nexus",
            "manufacturer": "iret33",
        }

    @property
    def native_value(self) -> float:
        data = self.coordinator.data
        if data and SENSOR_MEMORY_USAGE in data:
            return data[SENSOR_MEMORY_USAGE].get("size_mb", 0.0)
        return 0.0

    @property
    def native_unit_of_measurement(self) -> str:
        return "MB"

    @property
    def extra_state_attributes(self) -> dict[str, str | int | None]:
        data = self.coordinator.data
        if data and SENSOR_MEMORY_USAGE in data:
            mem_data = data[SENSOR_MEMORY_USAGE]
            return {
                "file_count": mem_data.get("file_count", 0),
                "status": mem_data.get("status", "unknown"),
                "oldest_file": mem_data.get("oldest_file"),
                "newest_file": mem_data.get("newest_file"),
            }
        return {}
