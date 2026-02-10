"""Coordinator for OpenClaw Control."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN, SENSOR_STATUS, SENSOR_NEXT_TASKS, SENSOR_SKILLS,
    SENSOR_CYCLE_COUNT, SENSOR_MEMORY_USAGE, STATUS_ONLINE, STATUS_IDLE
)

_LOGGER = logging.getLogger(__name__)


class OpenClawCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator for OpenClaw self-monitoring."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self._cycle_count = 0
        self._evolution_thought = "Initializing Nexus..."
        self._lifecycle_event: dict | None = None
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> dict:
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
        
        # Lifecycle event for this cycle
        self._lifecycle_event = {
            "type": "cycle_complete",
            "data": {
                "cycle": self._cycle_count,
                "timestamp": dt_util.utcnow().isoformat(),
            }
        }
        
        # Calculate memory usage (mock for now - will scan workspace/memory/)
        memory_usage = self._calculate_memory_usage()
        
        return {
            SENSOR_STATUS: STATUS_ONLINE if self._cycle_count > 0 else STATUS_IDLE,
            SENSOR_NEXT_TASKS: next_tasks,
            SENSOR_SKILLS: {
                "count": len(skills),
                "list": skills,
            },
            SENSOR_CYCLE_COUNT: self._cycle_count,
            SENSOR_MEMORY_USAGE: memory_usage,
            "evolution_thought": self._evolution_thought,
            "update_available": False,
            "online": True,
            "lifecycle_event": self._lifecycle_event,
        }

    def _calculate_memory_usage(self) -> dict:
        """Calculate memory folder size and metadata."""
        import os
        from pathlib import Path
        
        # Get workspace memory path
        workspace = Path("/home/wsl2/.openclaw/workspace")
        memory_path = workspace / "memory"
        
        if not memory_path.exists():
            return {
                "size_mb": 0.0,
                "file_count": 0,
                "status": "no_memory_folder",
            }
        
        total_size = 0
        file_count = 0
        files = []
        
        try:
            for item in memory_path.iterdir():
                if item.is_file():
                    stat = item.stat()
                    total_size += stat.st_size
                    file_count += 1
                    files.append({
                        "name": item.name,
                        "size": stat.st_size,
                        "modified": stat.st_mtime,
                    })
        except (OSError, PermissionError):
            return {
                "size_mb": 0.0,
                "file_count": 0,
                "status": "access_error",
            }
        
        # Sort by modification time for oldest/newest
        files.sort(key=lambda x: x["modified"])
        
        return {
            "size_mb": round(total_size / (1024 * 1024), 2),
            "file_count": file_count,
            "status": "ok",
            "oldest_file": files[0]["name"] if files else None,
            "newest_file": files[-1]["name"] if files else None,
        }

    async def async_shutdown(self) -> None:
        """Shutdown."""
        await super().async_shutdown()

    def set_evolution_thought(self, thought: str) -> None:
        """Set current evolution thought."""
        self._evolution_thought = thought
        if self.data:
            new_data = dict(self.data)
            new_data["evolution_thought"] = thought
            self.async_set_updated_data(new_data)

    def fire_lifecycle_event(self, event_type: str, event_data: dict | None = None) -> None:
        """Fire a lifecycle event."""
        self._lifecycle_event = {
            "type": event_type,
            "data": event_data or {},
        }
        if self.data:
            new_data = dict(self.data)
            new_data["lifecycle_event"] = self._lifecycle_event
            self.async_set_updated_data(new_data)
