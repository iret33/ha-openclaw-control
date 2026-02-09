"""Coordinator for OpenClaw Control."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN, SENSOR_STATUS, SENSOR_NEXT_TASKS, SENSOR_SKILLS,
    SENSOR_CYCLE_COUNT, STATUS_ONLINE, STATUS_IDLE
)

_LOGGER = logging.getLogger(__name__)


class OpenClawCoordinator(DataUpdateCoordinator):
    """Coordinator for OpenClaw self-monitoring."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self._cycle_count = 0
        self._evolution_thought = "Initializing Nexus..."
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update OpenClaw self-monitoring data."""
        self._cycle_count += 1
        
        # Get next cron jobs from HA (mock for now)
        next_tasks = [
            {"name": "agent-swarm-hourly", "next": "In 15 minutes"},
            {"name": "daily-repo-deep-scan", "next": "In 3 hours"},
            {"name": "ha-esphome-contribution", "next": "In 45 minutes"},
        ]
        
        # Active skills (mock)
        skills = [
            "healthcheck", "skill-creator", "tmux", "weather",
            "ha-agent-swarm", "esphome-agent-panel"
        ]
        
        return {
            SENSOR_STATUS: STATUS_ONLINE if self._cycle_count > 0 else STATUS_IDLE,
            SENSOR_NEXT_TASKS: next_tasks,
            SENSOR_SKILLS: {
                "count": len(skills),
                "list": skills,
            },
            SENSOR_CYCLE_COUNT: self._cycle_count,
            "evolution_thought": self._evolution_thought,
            "update_available": False,
            "online": True,
        }

    async def async_shutdown(self):
        """Shutdown."""
        await super().async_shutdown()

    def set_evolution_thought(self, thought: str):
        """Set current evolution thought."""
        self._evolution_thought = thought
        self.async_set_updated_data(self.data)
