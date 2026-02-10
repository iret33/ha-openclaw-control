"""Constants for OpenClaw Control."""

DOMAIN = "openclaw_control"
PLATFORMS = ["sensor", "binary_sensor", "button", "event", "number"]

# Sensor keys
SENSOR_STATUS = "openclaw_status"
SENSOR_NEXT_TASKS = "openclaw_next_tasks"
SENSOR_SKILLS = "openclaw_skills"
SENSOR_CYCLE_COUNT = "openclaw_cycle_count"
SENSOR_EVOLUTION_LOG = "openclaw_evolution"
SENSOR_MEMORY_USAGE = "openclaw_memory_usage"

# Binary sensor keys
BINARY_SENSOR_UPDATE = "openclaw_update_available"
BINARY_SENSOR_ONLINE = "openclaw_online"

# Event keys
EVENT_LIFECYCLE = "openclaw_lifecycle"

# Button keys
BUTTON_DIAGNOSTIC = "run_diagnostics"
BUTTON_EVOLVE = "trigger_evolution"

# Number keys
NUMBER_THINKING_DEPTH = "openclaw_thinking_depth"

# Attributes
ATTR_STATUS = "status"
ATTR_NEXT_CRON = "next_cron_jobs"
ATTR_SKILL_COUNT = "skill_count"
ATTR_SKILLS_LIST = "skills"
ATTR_EVOLUTION_THOUGHT = "current_evolution"

# States
STATUS_ONLINE = "Online"
STATUS_THINKING = "Thinking"
STATUS_IDLE = "Idle"
STATUS_ERROR = "Error"
