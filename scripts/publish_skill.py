#!/usr/bin/env python3
"""Publish an optimized Skill to the internal market, then commit and push it."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from scripts.record_optimizer_review import skill_digest
    from scripts.skill_repository import discover_skills, validate_skill
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from record_optimizer_review import skill_digest
    from skill_repository import discover_skills, validate_skill


class PublishError(RuntimeError):
    """A safe, user-actionable publishing failure."""


def _resolve_publisher(value: str | None) -> str:
    if not value:
        raise PublishError(
            "SKILLS_MARKET_PUBLISHER is not configured; market upload is required"
        )
    candidate = Path(value).expanduser()
    resolved = str(candidate.resolve()) if candidate.parent != Path(".") else shutil.which(value)
    if not resolved or not Path(resolved).is_file() or not os.access(resolved, os.X_OK):
        raise PublishError(f"SKILLS_MARKET_PUBLISHER is not executable: {value}")
    return resolved


def _verify_optimizer_report(
    report_path: Path, name: str, skill_dir: Path
) -> None:
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublishError(
            f"optimizer report is missing: {report_path}; run record_optimizer_review.py"
        ) from exc
    except json.JSONDecodeError as exc:
        raise PublishError(f"optimizer report is invalid JSON: {report_path}") from exc

    expected = {
        "skill": name,
        "category": skill_dir.parent.name,
        "status": "passed",
        "reviewer": "skill-optimizer",
    }
    mismatches = [key for key, value in expected.items() if report.get(key) != value]
    if mismatches:
        raise PublishError(
            "optimizer report does not match the publish request: " + ", ".join(mismatches)
        )
    if report.get("digest") != skill_digest(skill_dir):
        raise PublishError(
            "optimizer report is stale because Skill content changed after review"
        )


def _git(root: Path, *args: str, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=capture,
        text=True,
    )


def _git_preflight(root: Path, skill_dir: Path) -> str:
    branch_result = _git(root, "branch", "--show-current")
    if branch_result.returncode != 0:
        raise PublishError("current directory is not a Git repository")
    branch = branch_result.stdout.strip()
    if not branch:
        raise PublishError("publishing from detached HEAD is forbidden")
    if branch in {"main", "master"}:
        raise PublishError(f"publishing directly from '{branch}' is forbidden")

    status = _git(root, "status", "--porcelain", "--untracked-files=normal")
    if status.returncode != 0:
        raise PublishError("unable to inspect Git working tree")
    skill_prefix = skill_dir.relative_to(root).as_posix()
    allowed_exact = {
        "README.md",
        ".claude-plugin/marketplace.json",
        "config/skill-categories.json",
    }
    unrelated: list[str] = []
    for line in status.stdout.splitlines():
        path = line[3:].strip().strip('"')
        if path.startswith(".skill-publish/"):
            continue
        if path in allowed_exact or path == skill_prefix or path.startswith(skill_prefix + "/"):
            continue
        unrelated.append(path)
    if unrelated:
        raise PublishError(
            "unrelated working-tree changes must be handled before publishing: "
            + ", ".join(unrelated)
        )
    return branch


def _run_market(
    root: Path, publisher: str, name: str, skill_dir: Path, timeout: int = 300
) -> None:
    command = [
        publisher,
        "--skill-dir",
        str(skill_dir.resolve()),
        "--name",
        name,
        "--category",
        skill_dir.parent.name,
    ]
    try:
        result = subprocess.run(command, cwd=root, check=False, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise PublishError(f"market upload timed out after {timeout} seconds") from exc
    if result.returncode != 0:
        raise PublishError(f"market upload failed with exit code {result.returncode}")


def _commit_and_push(root: Path, name: str, skill_dir: Path, branch: str) -> None:
    paths = [
        skill_dir.relative_to(root).as_posix(),
        "README.md",
        ".claude-plugin/marketplace.json",
        "config/skill-categories.json",
    ]
    add = _git(root, "add", "--", *paths)
    if add.returncode != 0:
        raise PublishError(f"Git staging failed: {add.stderr.strip()}")
    staged = _git(root, "diff", "--cached", "--quiet")
    if staged.returncode == 0:
        raise PublishError("market upload succeeded, but there are no Skill changes to commit")
    if staged.returncode != 1:
        raise PublishError("unable to inspect staged Git changes")
    commit = _git(root, "commit", "-m", f"publish: {name}")
    if commit.returncode != 0:
        raise PublishError(f"Git commit failed: {commit.stderr.strip()}")
    push = _git(root, "push", "-u", "origin", branch, capture=False)
    if push.returncode != 0:
        raise PublishError(
            f"Git push failed after local commit; retry: git push -u origin {branch}"
        )


def publish_skill(
    root: Path,
    name: str,
    *,
    publisher: str | None,
    report_path: Path | None = None,
    no_git: bool = False,
) -> None:
    """Execute the guarded publication flow for one Skill."""
    root = root.resolve()
    publisher_path = _resolve_publisher(publisher)
    try:
        skills = discover_skills(root)
    except ValueError as exc:
        raise PublishError(str(exc)) from exc
    skill_dir = skills.get(name)
    if skill_dir is None:
        raise PublishError(f"Skill '{name}' was not found")
    report_path = report_path or root / ".skill-publish" / f"{name}.optimizer.json"
    _verify_optimizer_report(report_path, name, skill_dir)

    errors = validate_skill(root, name)
    if errors:
        raise PublishError("deterministic validation failed: " + "; ".join(errors))

    branch = ""
    if not no_git:
        branch = _git_preflight(root, skill_dir)
    _run_market(root, publisher_path, name, skill_dir)
    if not no_git:
        _commit_and_push(root, name, skill_dir, branch)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--no-git", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        publish_skill(
            root,
            args.skill_name,
            publisher=os.environ.get("SKILLS_MARKET_PUBLISHER"),
            report_path=args.report,
            no_git=args.no_git,
        )
    except PublishError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"PUBLISHED: {args.skill_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
