import time
import csv
import numpy as np
import matplotlib.pyplot as plt

from plant import MotionStage, PositionSensor


class HILTester:
    def __init__(self, sample_time=0.05):
        self.stage = MotionStage(k=0.2)
        self.sensor = PositionSensor(offset=0.01, noise_std=0.002, drift_per_step=0.0)
        self.sample_time = sample_time
        self.log = []

    def run_step(self, target_position, t):
        true_pos = self.stage.update(target_position)
        sensor_reading = self.sensor.read(true_pos)
        error = sensor_reading - target_position

        self.log.append({
            "time": t,
            "target": target_position,
            "true_pos": true_pos,
            "sensor": sensor_reading,
            "error": error
        })

        return true_pos, sensor_reading, error

    def run_sequence(self, positions, settle_time=1.0, measure_time=1.0):
        t = 0.0
        for pos in positions:
            settle_steps = int(settle_time / self.sample_time)
            for _ in range(settle_steps):
                self.run_step(pos, t)
                t += self.sample_time
                time.sleep(self.sample_time)

            measure_steps = int(measure_time / self.sample_time)
            for _ in range(measure_steps):
                self.run_step(pos, t)
                t += self.sample_time
                time.sleep(self.sample_time)

    def save_log(self, filename="hil_motion_log.csv"):
        keys = ["time", "target", "true_pos", "sensor", "error"]
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.log)

    def analyze(self, positions, measure_time=1.0):
        results = []
        measure_samples = int(measure_time / self.sample_time)

        idx = 0
        for pos in positions:
            idx += measure_samples
            segment = self.log[idx: idx + measure_samples]
            idx += measure_samples

            errors = np.array([s["error"] for s in segment])
            mean_error = np.mean(errors)
            max_error = np.max(np.abs(errors))
            std_error = np.std(errors)

            results.append({
                "position": pos,
                "mean_error": mean_error,
                "max_error": max_error,
                "std_error": std_error
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
