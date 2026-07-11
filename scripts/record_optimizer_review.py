#!/usr/bin/env python3
"""Record a content-bound `skill-optimizer` pass for one classified Skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.skill_repository import discover_skills
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from skill_repository import discover_skills


IGNORED_NAMES = {".DS_Store", "__pycache__"}


def skill_digest(skill_dir: Path) -> str:
    """Hash stable relative paths and bytes for every distributable Skill file."""
    digest = hashlib.sha256()
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or any(part in IGNORED_NAMES for part in path.parts):
            continue
        if path.suffix == ".pyc":
            continue
        relative = path.relative_to(skill_dir).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def write_optimizer_review(
    root: Path, name: str, skill_dir: Path, *, status: str
) -> Path:
    """Atomically write a publishable optimizer attestation."""
    if status != "passed":
        raise ValueError("Only a passed skill-optimizer review can be recorded")
    report_dir = root / ".skill-publish"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{name}.optimizer.json"
    report = {
        "skill": name,
        "category": skill_dir.parent.name,
        "digest": skill_digest(skill_dir),
        "status": status,
        "reviewer": "skill-optimizer",
        "reviewed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    descriptor, temp_name = tempfile.mkstemp(
        prefix=f".{name}.", suffix=".tmp", dir=report_dir
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        Path(temp_name).replace(report_path)
    except BaseException:
        Path(temp_name).unlink(missing_ok=True)
        raise
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name")
    parser.add_argument("--status", choices=("passed", "failed"), required=True)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    skills = discover_skills(root)
    skill_dir = skills.get(args.skill_name)
    if skill_dir is None:
        parser.error(f"Skill '{args.skill_name}' was not found")
    try:
        report = write_optimizer_review(
            root, args.skill_name, skill_dir, status=args.status
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(report.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
