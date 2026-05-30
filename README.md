# Precision Axis HIL Orchestrator
*A Python‑based Hardware‑in‑the‑Loop (HIL) simulation framework for evaluating the accuracy and repeatability of a precision motion axis.*

---

## Overview

Precision Axis HIL Orchestrator is a fully simulated Hardware‑in‑the‑Loop (HIL) environment designed to mimic the behavior of a precision linear motion stage found in semiconductor metrology, robotics, and high‑accuracy automation systems.

This project demonstrates:

- Mechatronic system modeling  
- Sensor simulation (noise, offset, drift)  
- Automated test sequencing  
- Accuracy & repeatability evaluation  
- Python‑based test automation  
- Data logging & visualization  

---

## System Architecture

The system consists of three core components:

### 1. Plant Model (`plant.py`)
Simulates the real hardware:

- First‑order motion stage dynamics  
- Sensor model with:
  - Gaussian noise  
  - Static offset  
  - Optional drift  

### 2. HIL Test Controller (`hil_test.py`)
Implements:

- Closed‑loop updates  
- Automated test sequences  
- Data logging  
- Metric computation  

### 3. Main Orchestrator (`main.py`)
Runs:

- Test execution  
- Analysis  
- Pass/fail evaluation  
- Plot generation  

---

## 📂 Project Structure

```text
precision-axis-hil-orchestrator/
│
├── plant.py               # Motion stage + sensor simulation
├── hil_test.py            # HIL test controller
├── main.py                # Entry point for running tests
├── hil_motion_log.csv     # Auto-generated test log
├── plots/                 # Saved plots (optional)
└── README.md              # Project documentation
```

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/precision-axis-hil-orchestrator.git
cd precision-axis-hil-orchestrator
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash
# or
venv\Scripts\activate          # Windows CMD/PowerShell
```

### 3. Install dependencies

```bash
pip install numpy matplotlib
```

---

## ▶️ Running the Simulation

```bash
python main.py
```

This will:

- Execute the HIL test sequence  
- Log data to `hil_motion_log.csv`  
- Print accuracy & repeatability metrics  
- Display a plot of:
  - Target position  
  - True position  
  - Sensor reading  

---

## 📊 Example Output

**Console metrics example:**

```text
Position 0.0 mm:
  Mean error: 0.0102 mm
  Max error:  0.0121 mm
  Std error:  0.0019 mm
  PASS: True

Position 10.0 mm:
  Mean error: 0.0098 mm
  Max error:  0.0115 mm
  Std error:  0.0021 mm
  PASS: True

OVERALL RESULT: PASS
```

---

## 🧠 How the HIL Simulation Works

### ✔ Motion Stage Model

A simple first‑order dynamic system:



\[
pos_{new} = pos_{old} + k \cdot (pos_{cmd} - pos_{old})
\]



### ✔ Sensor Model



\[
sensor = true\_pos + offset + noise + drift
\]



### ✔ Automated Test Sequence

- Move to position  
- Wait for settling  
- Measure  
- Log data  
- Compute metrics  

### ✔ Pass/Fail Criteria

- Max error < **0.01 mm**  
- Repeatability (std dev) < **0.005 mm**  

