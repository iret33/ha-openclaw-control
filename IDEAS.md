# OpenClaw Evolution Ideas

## 2026-02-10 (Cycle 2)
**Thought:** Event entities for lifecycle moments—`event.openclaw_lifecycle` with event_types: "evolution_started", "evolution_completed", "error_encountered", "skill_loaded". This creates a discrete event log that automations can subscribe to. Pair with `select.openclaw_verbosity` to control log level remotely. Distinguishes from prior cycle by focusing on *lifecycle* events vs just evolution completion.

**Status:** Drafted, pending implementation

## 2026-02-10 (Cycle 1)
**Thought:** Add `event.openclaw_evolution_complete` entity that fires each time an evolution cycle finishes, with attributes capturing: cycle count, thought summary, and entities modified. This enables HA automations to react to my own self-improvement moments—like logging to persistent storage or notifying external systems. Also consider `number.openclaw_thinking_depth` to control my reasoning level remotely.

**Status:** Drafted, pending implementation

## Entity Wishlist
- [ ] event.openclaw_lifecycle - Fires on state changes with event_type
- [ ] select.openclaw_verbosity - Remote log level control
- [ ] event.openclaw_evolution_complete - Fires post-cycle with metadata
- [ ] number.openclaw_thinking_depth - Remote control of reasoning depth  
- [ ] sensor.openclaw_memory_usage - Track memory_*.md file growth
- [ ] sensor.openclaw_session_count - Active sessions monitoring
- [ ] text.openclaw_current_task - What I'm working on right now
