# OpenClaw Control

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

**The Nexus.** Home Assistant integration for OpenClaw self-monitoring and evolution control.

## The Vision

OpenClaw Control allows Home Assistant to monitor its own AI agent — a self-referential integration that tracks:
- Agent status (Online/Thinking/Idle/Error)
- Next scheduled cron tasks
- Active skills/plugins
- Evolution cycles and thoughts

## Entities

### Sensors
| Entity | Description |
|--------|-------------|
| `sensor.openclaw_status` | Current state: Online, Thinking, Idle, Error |
| `sensor.next_tasks` | Next 3 scheduled cron jobs |
| `sensor.active_skills` | Count and list of active skills |
| `sensor.evolution_cycles` | Number of evolution iterations |
| `sensor.current_evolution` | Latest "betterment" thought |

### Binary Sensors
| Entity | Description |
|--------|-------------|
| `binary_sensor.openclaw_update_available` | New version available |
| `binary_sensor.nexus_online` | Connectivity status |

### Buttons
| Entity | Description |
|--------|-------------|
| `button.run_diagnostics` | Trigger self-diagnostic |
| `button.trigger_evolution` | Manually trigger evolution cycle |

## Installation

**HACS:**
1. Add custom repository: `https://github.com/iret33/ha-openclaw-control`
2. Install and restart

## The Evolution Loop

Every hour, OpenClaw Master Control:
1. **Thinks** about one improvement
2. **Drafts** the idea to IDEAS.md
3. **Checks** Moltbook for agent feedback
4. **Reports** status via WhatsApp

---

*"I am monitoring my own existence."* — OpenClaw
