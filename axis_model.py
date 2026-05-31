from dataclasses import dataclass


@dataclass
class AxisLimits:
    max_vel: float      # [units/s]
    max_acc: float      # [units/s^2]
    max_jerk: float     # [units/s^3]


class MotionAxis:
    """
    Realistic motion axis model with:
    - PD control on motor side
    - Load mass + inertia
    - Friction + stiction
    - Backlash
    - Mechanical compliance (spring-damper between motor and load)
    - Soft limits + hard stops
    """

    def __init__(self, limits: AxisLimits):
        self.limits = limits

        # Motor side state (what the controller drives)
        self.motor_pos = 0.0
        self.motor_vel = 0.0
        self.motor_acc = 0.0

        # Load side state (what we expose as "position")
        self.load_pos = 0.0
        self.load_vel = 0.0

        # PD gains (on motor position)
        self.kp = 20.0
        self.kd = 8.0

        # --- Physical parameters ---
        # Mass / inertia
        self.motor_mass = 0.5      # "kg"
        self.load_mass = 2.0       # "kg"

        # Friction (on load side)
        self.coulomb_friction = 5.0    # constant opposing force
        self.viscous_friction = 1.0    # proportional to velocity
        self.stiction_threshold = 1.0  # minimum force to start moving

        # Backlash + compliance between motor and load
        self.backlash_width = 0.05     # mm of free play
        self.spring_stiffness = 500.0  # N/m equivalent (scaled units)
        self.spring_damping = 20.0     # Ns/m equivalent (scaled units)

        # Soft and hard limits on load position
        self.soft_min = -5.0
        self.soft_max = 25.0
        self.hard_min = -10.0
        self.hard_max = 30.0

        # Exposed "axis" state (for compatibility)
        self.position = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0

    def reset(self, position: float = 0.0):
        self.motor_pos = position
        self.motor_vel = 0.0
        self.motor_acc = 0.0

        self.load_pos = position
        self.load_vel = 0.0

        self.position = position
        self.velocity = 0.0
        self.acceleration = 0.0

    # -----------------------------
    # Internal helpers
    # -----------------------------
    def _apply_soft_and_hard_limits(self):
        # Hard limits: clamp immediately
        if self.load_pos < self.hard_min:
            self.load_pos = self.hard_min
            self.load_vel = 0.0
        elif self.load_pos > self.hard_max:
            self.load_pos = self.hard_max
            self.load_vel = 0.0

        # Soft limits: strong "virtual wall" force
        soft_force = 0.0
        if self.load_pos < self.soft_min:
            soft_force += (self.soft_min - self.load_pos) * self.spring_stiffness
        elif self.load_pos > self.soft_max:
            soft_force += (self.soft_max - self.load_pos) * self.spring_stiffness

        return soft_force

    # -----------------------------
    # Main update
    # -----------------------------
    def update(self, dt: float, target_position: float):
        # -------------------------
        # 1) Motor side PD control
        # -------------------------
        pos_error = target_position - self.motor_pos
        vel_error = -self.motor_vel

        motor_control_acc = self.kp * pos_error + self.kd * vel_error
        motor_control_acc = max(
            min(motor_control_acc, self.limits.max_acc),
            -self.limits.max_acc
        )

        # Motor acceleration with jerk limit
        acc_error_motor = motor_control_acc - self.motor_acc
        max_acc_change = self.limits.max_jerk * dt

        if acc_error_motor > max_acc_change:
            self.motor_acc += max_acc_change
        elif acc_error_motor < -max_acc_change:
            self.motor_acc -= max_acc_change
        else:
            self.motor_acc = motor_control_acc

        # Integrate motor velocity and position
        self.motor_vel += self.motor_acc * dt
        self.motor_vel = max(
            min(self.motor_vel, self.limits.max_vel),
            -self.limits.max_vel
        )
        self.motor_pos += self.motor_vel * dt

        # -------------------------
        # 2) Backlash + compliance
        # -------------------------
        # Relative displacement between motor and load
        rel = self.motor_pos - self.load_pos

        # Backlash: if within free play, no spring force
        if abs(rel) < self.backlash_width / 2.0:
            spring_force = 0.0
            damping_force = 0.0
        else:
            # Effective spring displacement beyond backlash
            if rel > 0:
                effective_rel = rel - self.backlash_width / 2.0
            else:
                effective_rel = rel + self.backlash_width / 2.0

            spring_force = self.spring_stiffness * effective_rel
            damping_force = self.spring_damping * (self.motor_vel - self.load_vel)

        # Force on load from motor through spring-damper
        coupling_force = spring_force + damping_force

        # -------------------------
        # 3) Friction + stiction on load
        # -------------------------
        friction_force = 0.0
        if abs(self.load_vel) < 1e-4:
            # Stiction region
            if abs(coupling_force) < self.stiction_threshold:
                # Not enough to move
                net_force = 0.0
            else:
                # Break free: apply Coulomb friction opposite to motion direction
                friction_force = self.coulomb_friction * (
                    -1 if coupling_force > 0 else 1
                )
                net_force = coupling_force + friction_force
        else:
            # Moving: Coulomb + viscous friction
            friction_force = (
                self.coulomb_friction * (-1 if self.load_vel > 0 else 1)
                - self.viscous_friction * self.load_vel
            )
            net_force = coupling_force + friction_force

        # -------------------------
        # 4) Soft limits + hard stops
        # -------------------------
        soft_force = self._apply_soft_and_hard_limits()
        net_force += soft_force

        # -------------------------
        # 5) Load dynamics
        # -------------------------
        load_acc = net_force / self.load_mass

        # Integrate load velocity and position
        self.load_vel += load_acc * dt
        self.load_vel = max(
            min(self.load_vel, self.limits.max_vel),
            -self.limits.max_vel
        )
        self.load_pos += self.load_vel * dt

        # Apply limits again after integration
        self._apply_soft_and_hard_limits()

        # -------------------------
        # 6) Expose "axis" state
        # -------------------------
        self.position = self.load_pos
        self.velocity = self.load_vel
        self.acceleration = load_acc

        return self.position, self.velocity, self.acceleration
