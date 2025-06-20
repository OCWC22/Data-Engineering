#!/usr/bin/env python3
"""
Development script for running code quality checks.
Usage: python scripts/lint.py [--fix] [--format-only] [--check-only]
"""
import os
from pathlib import Path
import subprocess
import sys


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔍 {description}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ {description} - PASSED")
        if result.stdout.strip():
            print(result.stdout)
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr.strip():
            print(result.stderr)
        if result.stdout.strip():
            print(result.stdout)
        return False


def main():
    """Main lint script."""
    fix_mode = "--fix" in sys.argv
    format_only = "--format-only" in sys.argv
    check_only = "--check-only" in sys.argv

    # Change to project root
    os.chdir(Path(__file__).parent.parent)

    success = True

    if not check_only:
        if fix_mode:
            success &= run_command(
                ["poetry", "run", "ruff", "check", ".", "--fix"],
                "Auto-fixing ruff issues",
            )

        success &= run_command(
            ["poetry", "run", "ruff", "format", "."], "Formatting code with ruff"
        )

    if not format_only:
        success &= run_command(
            ["poetry", "run", "ruff", "check", "."], "Checking code with ruff"
        )

        success &= run_command(
            ["poetry", "run", "ruff", "format", "--check", "."],
            "Checking code formatting",
        )

    if success:
        print("\n🎉 All code quality checks passed!")
        sys.exit(0)
    else:
        print("\n💥 Some checks failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
