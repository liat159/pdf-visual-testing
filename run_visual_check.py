
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

TEST_PATH = PROJECT_ROOT / "tests" / "test_report_visual.py"
COMPARISON_SCRIPT = PROJECT_ROOT / "tools" / "create_visual_comparison.py"


def main():
    print("\n=== Step 1: Run visual regression test ===\n")

    test_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(TEST_PATH),
            "-v",
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )

    print("\n=== Step 2: Generate local HTML comparison ===\n")

    comparison_result = subprocess.run(
        [
            sys.executable,
            str(COMPARISON_SCRIPT),
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if comparison_result.returncode != 0:
        print(
            "\nWARNING: The HTML comparison report "
            "could not be generated."
        )

    if test_result.returncode != 0:
        print("\nRESULT: Visual regression test FAILED.")
        return test_result.returncode

    print("\nRESULT: Visual regression test PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
