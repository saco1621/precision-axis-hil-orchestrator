import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from hil_test import HILTester
from axis_model import MotionAxis, AxisLimits


def main():
    # -----------------------------
    # 1. Axis limits
    # -----------------------------
    limits = AxisLimits(
        max_vel=500.0,
        max_acc=2000.0,
        max_jerk=8000.0
    )

    axis = MotionAxis(limits)
    axis.reset(position=0.0)

    # -----------------------------
    # 2. Test configuration
    # -----------------------------
    positions = [0.0, 10.0, 20.0, 0.0]
    tester = HILTester(sample_time=0.01)

    dt = 0.01
    settle_time = 1.0
    measure_time = 1.0

    # -----------------------------
    # 3. Setup live animation
    # -----------------------------
    fig, (ax_arm, ax_plot) = plt.subplots(2, 1, figsize=(8, 6))

    # Arm visualization
    ax_arm.set_xlim(-5, 25)
    ax_arm.set_ylim(-1, 1)
    ax_arm.set_title("Live Arm Position")
    arm_line, = ax_arm.plot([], [], lw=6)

    # Live plot
    ax_plot.set_xlim(0, 60)
    ax_plot.set_ylim(-5, 25)
    ax_plot.set_title("Live Position Plot")
    ax_plot.set_xlabel("Time [s]")
    ax_plot.set_ylabel("Position [mm]")

    true_line, = ax_plot.plot([], [], label="True Position")
    target_line, = ax_plot.plot([], [], label="Target")
    ax_plot.legend()

    # Data buffers
    time_data = []
    true_data = []
    target_data = []

    start_time = time.time()
    current_target_index = 0
    current_target = positions[current_target_index]
    tester.set_target(current_target)

    # -----------------------------
    # 4. Animation update function
    # -----------------------------
    def update(frame):
        nonlocal current_target_index, current_target

        # Update physics
        pos, vel, acc = axis.update(dt, current_target)
        tester.log_sample(pos)

        # Switch target when close
        if abs(axis.position - current_target) < 0.05:
            current_target_index += 1
            if current_target_index < len(positions):
                current_target = positions[current_target_index]
                tester.set_target(current_target)

        # Update time series
        t = time.time() - start_time
        time_data.append(t)
        true_data.append(pos)
        target_data.append(current_target)

        # Update arm
        arm_line.set_data([0, pos], [0, 0])

        # Update plot
        true_line.set_data(time_data, true_data)
        target_line.set_data(time_data, target_data)

        ax_plot.set_xlim(max(0, t - 20), t + 2)

        return arm_line, true_line, target_line

    # -----------------------------
    # 5. Start animation
    # -----------------------------
    ani = FuncAnimation(fig, update, interval=10, blit=False)
    plt.tight_layout()
    plt.show()

    # -----------------------------
    # 6. Save log + analyze
    # -----------------------------
    tester.save_log("hil_motion_log.csv")
    results = tester.analyze(positions, measure_time=1.0)

    print("\nAnalysis Results:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
