#!/usr/bin/env python3
"""Rebuild references/INDEX.md from the bundled documentation tree."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path


def title_and_url(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    url_match = re.search(r"^>\s+(https?://\S+)", text, re.MULTILINE)
    title_match = re.search(r"title:\s*([^|\n-][^|\n]*?)\s*(?:\||---|$)", text)
    if not title_match:
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.parent.name.replace("_", " ")
    url = url_match.group(1) if url_match else ""
    return title, url


def main() -> None:
    skill_root = Path(__file__).resolve().parents[1]
    refs_root = skill_root / "references"
    docs_root = refs_root / "docs"
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(docs_root.rglob("*.md")):
        rel = path.relative_to(docs_root)
        groups[rel.parts[0]].append(rel)

    lines = [
        "# LlamaIndex 文档索引",
        "",
        "本索引由 `scripts/build_index.py` 生成。路径均相对于 `references/docs/`；优先用 `scripts/search_docs.py` 全文检索，只在需要浏览主题结构时读取本文件。",
        "",
        f"共 {sum(len(paths) for paths in groups.values())} 篇 Markdown 文档。",
        "",
    ]
    for group, paths in groups.items():
        lines.extend([f"## {group}", ""])
        for rel in paths:
            title, url = title_and_url(docs_root / rel)
            suffix = f" — <{url}>" if url else ""
            lines.append(f"- `{rel.as_posix()}` — {title}{suffix}")
        lines.append("")

    (refs_root / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
