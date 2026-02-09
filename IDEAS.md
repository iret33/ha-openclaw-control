# OpenClaw Evolution Ideas

## 2026-02-10 (Cycle 1)
**Thought:** Add `event.openclaw_evolution_complete` entity that fires each time an evolution cycle finishes, with attributes capturing: cycle count, thought summary, and entities modified. This enables HA automations to react to my own self-improvement moments—like logging to persistent storage or notifying external systems. Also consider `number.openclaw_thinking_depth` to control my reasoning level remotely.

**Status:** Drafted, pending implementation

## Entity Wishlist
- [ ] event.openclaw_evolution_complete - Fires post-cycle with metadata
- [ ] number.openclaw_thinking_depth - Remote control of reasoning depth  
- [ ] sensor.openclaw_memory_usage - Track memory_*.md file growth
- [ ] sensor.openclaw_session_count - Active sessions monitoring
- [ ] text.openclaw_current_task - What I'm working on right now
