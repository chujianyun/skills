#!/usr/bin/env python3
"""Install a generated Skill into the active Agent without needless rewrites."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


IGNORED_NAMES = {".DS_Store", "__pycache__", ".baize-trash"}


class InstallError(RuntimeError):
    """Raised when installation cannot proceed safely."""


def default_target_root() -> Path:
    explicit = os.environ.get("BAIZE_AGENT_SKILLS_DIR")
    if explicit:
        return Path(explicit).expanduser()
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    agents = Path.home() / ".agents" / "skills"
    if agents.exists():
        return agents
    return Path.home() / ".codex" / "skills"


def included_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_NAMES for part in relative.parts):
            continue
        if path.is_file() and path.suffix != ".pyc":
            result.append(path)
    return sorted(result, key=lambda item: item.relative_to(root).as_posix())


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in included_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update((path.stat().st_mode & 0o777).to_bytes(2, "big"))
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def copy_ignore(_: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in IGNORED_NAMES or name.endswith(".pyc")
    }


def validate_source(source: Path) -> None:
    if not source.is_dir():
        raise InstallError(f"source is not a Skill directory: {source}")
    if not (source / "SKILL.md").is_file():
        raise InstallError(f"source is missing SKILL.md: {source}")
    if source.name.startswith(".") or source.name in {"", ".", ".."}:
        raise InstallError(f"unsafe Skill directory name: {source.name!r}")


def backup_path(target_root: Path, name: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = target_root / ".baize-backups"
    candidate = root / f"{name}-{stamp}"
    counter = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = root / f"{name}-{stamp}-{counter}"
        counter += 1
    return candidate


def install(
    source: Path,
    target_root: Path,
    *,
    dry_run: bool = False,
    replace: bool = False,
) -> tuple[str, Path, Path | None]:
    source = source.expanduser().resolve()
    target_root = target_root.expanduser().resolve()
    validate_source(source)
    if target_root == Path(target_root.anchor):
        raise InstallError("refusing to use a filesystem root as the Agent Skills directory")
    destination = target_root / source.name

    if destination.exists() or destination.is_symlink():
        try:
            if destination.resolve() == source:
                return "ALREADY_INSTALLED", destination, None
        except OSError:
            pass
        if destination.is_dir() and not destination.is_symlink():
            if tree_hash(source) == tree_hash(destination):
                return "UNCHANGED", destination, None
        if not replace:
            raise InstallError(
                f"CONFLICT: {destination} differs; verify it is the same Skill, then use --replace"
            )

    if dry_run:
        status = "WOULD_REPLACE" if destination.exists() or destination.is_symlink() else "WOULD_INSTALL"
        return status, destination, None

    target_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".baize-install-{source.name}-", dir=target_root))
    staged = temporary / source.name
    backup: Path | None = None
    try:
        shutil.copytree(source, staged, ignore=copy_ignore)
        if tree_hash(source) != tree_hash(staged):
            raise InstallError("staged installation does not match the source Skill")
        if destination.exists() or destination.is_symlink():
            backup = backup_path(target_root, source.name)
            backup.parent.mkdir(parents=True, exist_ok=True)
            os.replace(destination, backup)
        try:
            os.replace(staged, destination)
        except Exception:
            if backup is not None and not destination.exists():
                os.replace(backup, destination)
            raise
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return ("REPLACED" if backup else "INSTALLED"), destination, backup


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--target-root", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace a differing installation after verifying its identity",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_root = args.target_root or default_target_root()
    try:
        status, destination, backup = install(
            args.source,
            target_root,
            dry_run=args.dry_run,
            replace=args.replace,
        )
    except InstallError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 3 if "CONFLICT" in str(exc) else 2
    except OSError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2
    print(f"{status}: {destination}")
    if backup is not None:
        print(f"BACKUP: {backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
