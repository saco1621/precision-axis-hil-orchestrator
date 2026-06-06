# Backlash Profiles  
_For Precision Axis HIL Orchestrator_

Defines mechanical dead‑zone behavior during direction reversal.

---

## Backlash Values

| Backlash (mm) | Use Case |
|----------------|----------|
| 0.02           | High‑precision mechanics |
| 0.03           | Standard linear stage |
| 0.05           | Worn or loose mechanics |

---

## Notes
- Backlash introduces a **dead zone** where motor motion does not immediately move the load.
- Used to test controller robustness during **direction changes**.
