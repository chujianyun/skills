#!/usr/bin/env python3
"""Search a generated Wiki Skill's Markdown corpus without dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Match:
    score: int
    path: Path
    snippets: list[tuple[int, str]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Keywords, an exact product term, or an API/class name")
    parser.add_argument(
        "--prefix",
        default="",
        help="Restrict paths below references/docs, for example guides/configuration",
    )
    parser.add_argument("--max-results", type=int, default=8)
    parser.add_argument("--snippets", type=int, default=3)
    return parser.parse_args()


def tokenize(query: str) -> list[str]:
    return [part.casefold() for part in re.findall(r"[\w.-]+", query) if len(part) > 1]


def score_file(
    path: Path,
    docs_root: Path,
    query: str,
    terms: list[str],
    snippet_limit: int,
) -> Match | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None

    relative = path.relative_to(docs_root)
    relative_text = relative.as_posix().casefold()
    folded = text.casefold()
    headings = "\n".join(
        line for line in folded.splitlines() if line.lstrip().startswith("#")
    )
    phrase = query.casefold().strip()

    score = 0
    if phrase and phrase in relative_text:
        score += 30
    if phrase and phrase in headings:
        score += 20
    if phrase and phrase in folded:
        score += 12
    for term in terms:
        if term in relative_text:
            score += 10
        if term in headings:
            score += 6
        score += min(folded.count(term), 8)

    if score == 0:
        return None

    snippets: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        line_folded = line.casefold()
        if (phrase and phrase in line_folded) or any(
            term in line_folded for term in terms
        ):
            snippets.append((number, line.strip()[:240]))
            if len(snippets) >= snippet_limit:
                break
    return Match(score=score, path=relative, snippets=snippets)


def main() -> int:
    args = parse_args()
    if args.max_results < 1 or args.snippets < 1:
        print("--max-results and --snippets must be positive", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parents[1]
    docs_root = (skill_root / "references" / "docs").resolve()
    search_root = (docs_root / args.prefix).resolve()
    if docs_root not in (search_root, *search_root.parents):
        print("--prefix must stay inside references/docs", file=sys.stderr)
        return 2
    if not search_root.exists():
        print(f"Search prefix does not exist: {args.prefix}", file=sys.stderr)
        return 2

    terms = tokenize(args.query)
    if not terms:
        print("Query must contain searchable letters or numbers", file=sys.stderr)
        return 2

    matches = [
        match
        for path in search_root.rglob("*.md")
        if (match := score_file(path, docs_root, args.query, terms, args.snippets))
    ]
    matches.sort(key=lambda item: (-item.score, item.path.as_posix()))
    if not matches:
        print(f"No matches for: {args.query}")
        print("Try a synonym, product term, API/class name, or a broader --prefix.")
        return 1

    for match in matches[: args.max_results]:
        print(f"[{match.score:>3}] references/docs/{match.path.as_posix()}")
        for line_number, snippet in match.snippets:
            print(f"      L{line_number}: {snippet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
