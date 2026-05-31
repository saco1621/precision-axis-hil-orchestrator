import csv
import numpy as np
import matplotlib.pyplot as plt
from axis_model import MotionAxis, AxisLimits


class HILTester:
    def __init__(self, sample_time=0.05):
        limits = AxisLimits(
            max_vel=500.0,
            max_acc=2000.0,
            max_jerk=8000.0
        )
        self.axis = MotionAxis(limits)

        self.sample_time = sample_time
        self.log = []
        self.current_time = 0.0
        self.last_target = 0.0

        # --- Sensor model parameters ---
        self.noise_std = 0.02          # random noise (mm)
        self.drift_rate = 0.0005       # mm drift per second
        self.encoder_resolution = 0.001  # quantization (mm)

        self.accumulated_drift = 0.0

    def set_target(self, target):
        self.last_target = target

    def simulate_sensor(self, true_pos):
        # Add Gaussian noise
        noisy = true_pos + np.random.normal(0, self.noise_std)

        # Add slow drift
        self.accumulated_drift += self.drift_rate * self.sample_time
        noisy += self.accumulated_drift

        # Quantize to encoder resolution
        quantized = round(noisy / self.encoder_resolution) * self.encoder_resolution

        return quantized

    def log_sample(self, true_pos):
        sensor_reading = self.simulate_sensor(true_pos)
        error = sensor_reading - self.last_target

        self.log.append({
            "time": self.current_time,
            "target": self.last_target,
            "true_pos": true_pos,
            "sensor": sensor_reading,
            "error": error
        })

        self.current_time += self.sample_time

    def save_log(self, filename="hil_motion_log.csv"):
        keys = ["time", "target", "true_pos", "sensor", "error"]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.log)

    def analyze(self, positions, measure_time=1.0):
        results = []
        samples_per_segment = int(measure_time / self.sample_time)

        idx = 0
        for pos in positions:
            idx += samples_per_segment
            segment = self.log[idx: idx + samples_per_segment]
            idx += samples_per_segment

            errors = np.array([s["error"] for s in segment])
            results.append({
                "position": pos,
                "mean_error": np.mean(errors),
                "max_error": np.max(np.abs(errors)),
                "std_error": np.std(errors)
            })

        return results

    def plot_results(self):
        times = [s["time"] for s in self.log]
        targets = [s["target"] for s in self.log]
        true_pos = [s["true_pos"] for s in self.log]
        sensor = [s["sensor"] for s in self.log]

        plt.figure(figsize=(10, 5))
        plt.plot(times, targets, label="Target position")
        plt.plot(times, true_pos, label="True position")
        plt.plot(times, sensor, label="Sensor reading", alpha=0.7)
        plt.xlabel("Time [s]")
        plt.ylabel("Position [mm]")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
