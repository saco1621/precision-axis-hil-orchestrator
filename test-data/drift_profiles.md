# Drift Profiles  
_For Precision Axis HIL Orchestrator_

Defines slow thermal drift applied to the simulated sensor.

---

## Drift Rates

| Drift Rate (mm/s) | Use Case |
|--------------------|----------|
| 0.0005             | Stable environment |
| 0.0010             | Normal operation |
| 0.0020             | Stress testing |

---

## Notes
- Drift accumulates over time:  
  `sensor = sensor + drift_rate * dt`
- Used to evaluate long‑term stability and compensation algorithms.
