#!/usr/bin/env python3
"""Search curated QwenWork notes and the official page catalog, offline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def note_entries(root: Path) -> list[dict]:
    entries = []
    for path in sorted(root.glob("*.md")):
        if path.name in {"INDEX.md", "SOURCE.md"}:
            continue
        title = path.stem
        start, body = 1, []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                if body:
                    entries.append({"title": title, "text": "\n".join(body),
                                    "location": f"references/{path.name}:{start}",
                                    "kind": "本地知识"})
                title, start, body = line[3:], number, []
            else:
                body.append(line)
        if body:
            entries.append({"title": title, "text": "\n".join(body),
                            "location": f"references/{path.name}:{start}",
                            "kind": "本地知识"})
    return entries


def search(root: Path, query: str, scope: str) -> list[dict]:
    terms = list(dict.fromkeys(re.findall(r"[\w.-]+", query.casefold())))
    if not terms:
        raise ValueError("请输入中文或英文关键词；多个关键词用空格分隔。")
    entries = note_entries(root) if scope in {"all", "notes"} else []
    if scope in {"all", "index"}:
        catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
        entries.extend({"title": p["title"], "text": p["section"] + " " + p["url"],
                        "location": p["url"], "kind": "官方入口（需读取正文）"}
                       for p in catalog["pages"])
    matches = []
    for entry in entries:
        heading = entry["title"].casefold()
        haystack = heading + "\n" + entry["text"].casefold()
        hits = sum(term in haystack for term in terms)
        if not hits:
            continue
        score = hits * 10 + sum(5 for term in terms if term in heading)
        if hits == len(terms):
            score += 20
        if entry["kind"] == "本地知识":
            score += 3
        entry["score"] = score
        entry["snippet"] = next((line.strip()[:220] for line in entry["text"].splitlines()
                                 if any(t in line.casefold() for t in terms)), "")
        matches.append(entry)
    return sorted(matches, key=lambda item: (-item["score"], item["location"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="2–5 个空格分隔的关键词，如 定时任务 休眠")
    parser.add_argument("--scope", choices=("all", "notes", "index"), default="all")
    parser.add_argument("--limit", type=int, default=6)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit 必须大于零")
    root = Path(__file__).resolve().parents[1] / "references"
    try:
        matches = search(root, args.query, args.scope)
    except (OSError, ValueError) as exc:
        print(f"检索失败：{exc}", file=sys.stderr)
        return 2
    if not matches:
        print("未找到匹配项。请换同义词或查看 references/INDEX.md；无结果不代表功能不存在。")
        return 1
    for entry in matches[:args.limit]:
        print(f"[{entry['kind']}] {entry['title']}\n  {entry['location']}")
        if entry["snippet"]:
            print(f"  {entry['snippet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
