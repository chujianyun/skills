#!/usr/bin/env python3
"""Validate one classified Skill and run the official quick validator."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from skill_repository import discover_skills, validate_skill


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    errors = validate_skill(root, args.skill_name)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    skill_dir = discover_skills(root)[args.skill_name]
    quick_validate = (
        Path.home()
        / ".agents"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    if quick_validate.exists():
        result = subprocess.run(
            [sys.executable, str(quick_validate), str(skill_dir)], check=False
        )
        if result.returncode != 0:
            return result.returncode

    print(f"PASS: {skill_dir.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
