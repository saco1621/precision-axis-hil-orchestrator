from hil_test import HILTester

def main():
    positions = [0.0, 10.0, 20.0, 0.0]
    tester = HILTester(sample_time=0.05)

    print("Running HIL test sequence...")
    tester.run_sequence(positions, settle_time=1.0, measure_time=1.0)

    print("Saving log...")
    tester.save_log("hil_motion_log.csv")

    print("Analyzing results...")
    results = tester.analyze(positions, measure_time=1.0)

    max_allowed_error = 0.01
    max_allowed_std = 0.005

    overall_pass = True
    for r in results:
        pos = r["position"]
        mean_err = r["mean_error"]
        max_err = r["max_error"]
        std_err = r["std_error"]

        pos_pass = (max_err <= max_allowed_error) and (std_err <= max_allowed_std)
        overall_pass = overall_pass and pos_pass

        print(f"Position {pos} mm:")
        print(f"  Mean error: {mean_err:.4f} mm")
        print(f"  Max error:  {max_err:.4f} mm")
        print(f"  Std error:  {std_err:.4f} mm")
        print(f"  PASS: {pos_pass}")
        print()

    print(f"OVERALL RESULT: {'PASS' if overall_pass else 'FAIL'}")

    print("Plotting results...")
    tester.plot_results()


if __name__ == "__main__":
    main()
