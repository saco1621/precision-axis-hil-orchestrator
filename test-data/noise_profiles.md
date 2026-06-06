# Noise Profiles  
_For Precision Axis HIL Orchestrator_

Defines Gaussian noise levels applied to the simulated sensor output.

---

## Noise Levels

| Profile | σ (mm) | Use Case |
|---------|--------|----------|
| Low     | 0.001  | High‑precision metrology |
| Medium  | 0.005  | Standard automation |
| High    | 0.010  | Stress testing |

---

## Notes
- Noise is applied as:  
  `sensor = true_pos + N(0, σ)`
- Higher noise levels are used to test **robustness** and **filtering behavior**.
