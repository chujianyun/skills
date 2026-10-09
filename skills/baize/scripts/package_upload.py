#!/usr/bin/env python3
"""Package Baize for a Skill uploader that accepts only UTF-8 text files."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile


IGNORED_PARTS = {"__pycache__", "__MACOSX", ".git", ".baize-trash"}
LOCAL_ONLY_FILES = {"assets/icon.png", "agents/openai.yaml"}


def package_upload(source: Path, output: Path) -> tuple[int, list[str]]:
    source = source.resolve()
    output = output.resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError("source must contain SKILL.md")
    if output.is_relative_to(source):
        raise ValueError("output must be outside the Skill directory")
    files: list[tuple[str, bytes]] = []
    skipped: list[str] = []
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        name = relative.as_posix()
        if (any(part in IGNORED_PARTS for part in relative.parts)
                or any(part.startswith("._") for part in relative.parts)
                or path.name == ".DS_Store"
                or path.suffix in {".pyc", ".pyo"}
                or name in LOCAL_ONLY_FILES):
            if not path.is_dir():
                skipped.append(name)
            continue
        if path.is_symlink():
            raise ValueError(f"symlinks cannot be packaged: {name}")
        if not path.is_file():
            continue
        data = path.read_bytes()
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"unexpected binary file: {name}") from exc
        if any(ord(char) < 32 and char not in "\t\r\n" for char in content):
            raise ValueError(f"unexpected binary/control characters: {name}")
        files.append((f"{source.name}/{name}", data))

    output.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation preserves existing packages; no implicit overwrite.
    with ZipFile(output, "x", compression=ZIP_DEFLATED) as archive:
        for name, data in files:
            archive.writestr(name, data)
    return len(files), skipped


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        count, skipped = package_upload(source, args.output)
    except (OSError, ValueError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"PACKAGED: {args.output.resolve()} ({count} UTF-8 text files)")
    for name in skipped:
        print(f"EXCLUDED: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
