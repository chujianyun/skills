#!/usr/bin/env python3
"""Replace credential-shaped example values in the bundled documentation."""

from __future__ import annotations

import re
from pathlib import Path


ASSIGNMENT = re.compile(
    r"(?P<name>api[_-]?key|access[_-]?token|secret)"
    r"(?P<separator>\s*[:=]\s*)"
    r"(?P<quote>['\"])"
    r"(?P<value>[^'\"]{12,})"
    r"(?P=quote)",
    re.IGNORECASE,
)


def replacement(match: re.Match[str]) -> str:
    name = match.group("name")
    lowered = name.casefold()
    if "secret" in lowered:
        value = "<SECRET>"
    elif "token" in lowered:
        value = "<TOKEN>"
    else:
        value = "<API_KEY>"
    return f"{name}{match.group('separator')}{match.group('quote')}{value}{match.group('quote')}"


def main() -> None:
    docs_root = Path(__file__).resolve().parents[1] / "references" / "docs"
    changed_files = 0
    replacements = 0
    for path in sorted(docs_root.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, count = ASSIGNMENT.subn(replacement, original)
        if count:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
            replacements += count
    print(f"Sanitized {replacements} credential-shaped values in {changed_files} files.")


if __name__ == "__main__":
    main()
