# Motion Targets  
_For Precision Axis HIL Orchestrator_

This file defines the commanded motion positions used during HIL testing.

---

## Target Positions

| Target (mm) | Purpose |
|-------------|---------|
| 0.0         | Home position stability |
| 5.0         | Mid‑range accuracy |
| 10.0        | Full‑range accuracy |
| 20.0        | Long‑travel behavior |
| -1.0        | Negative limit boundary test |
| 21.0        | Positive limit boundary test |

---

## Notes
- Targets are chosen to test both **normal operating range** and **limit boundary behavior**.
- Values outside the physical range trigger **soft/hard limit clamping** in the axis model.
