import numpy as np

class MotionStage:
    def __init__(self, k=0.2, initial_pos=0.0):
        self.position = initial_pos
        self.k = k

    def update(self, target_position):
        self.position = self.position + self.k * (target_position - self.position)
        return self.position


class PositionSensor:
    def __init__(self, offset=0.01, noise_std=0.002, drift_per_step=0.0):
        self.offset = offset
        self.noise_std = noise_std
        self.drift = 0.0
        self.drift_per_step = drift_per_step

    def read(self, true_position):
        noise = np.random.normal(0, self.noise_std)
        self.drift += self.drift_per_step
        return true_position + self.offset + noise + self.drift
