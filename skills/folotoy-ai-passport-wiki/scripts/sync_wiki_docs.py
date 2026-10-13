#!/usr/bin/env python3
"""Synchronize staged Wiki Markdown into a generated Skill using SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import parse_qsl, urlsplit


SENSITIVE_QUERY_PARTS = (
    "token",
    "secret",
    "signature",
    "credential",
    "session",
    "cookie",
    "auth",
    "api_key",
    "apikey",
    "access_key",
)


class SyncError(RuntimeError):
    """Raised when a staged corpus cannot be applied safely."""


class StaleFilesError(SyncError):
    """Raised when upstream removals require explicit prune authorization."""


@dataclass
class Page:
    title: str
    source_url: str
    source_path: str
    local_path: str
    summary: str
    keywords: list[str]
    content: bytes
    content_hash: str


@dataclass
class Asset:
    source_url: str
    local_path: str
    content: bytes
    content_hash: str


@dataclass
class StagedCorpus:
    source_root: str
    coverage: dict[str, Any]
    pages: list[Page]
    assets: list[Asset]


@dataclass
class SyncSummary:
    status: str
    added_documents: int
    changed_documents: int
    unchanged_documents: int
    removed_documents: int
    added_assets: int
    changed_assets: int
    unchanged_assets: int
    removed_assets: int


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def normalize_markdown(text: str) -> str:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def safe_relative(raw: Any, *, markdown: bool) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise SyncError("local_path must be a non-empty string")
    path = PurePosixPath(raw.strip())
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise SyncError(f"unsafe local_path: {raw!r}")
    normalized = path.as_posix()
    if markdown and path.suffix.casefold() != ".md":
        raise SyncError(f"document local_path must end in .md: {normalized}")
    return normalized


def safe_staged_file(root: Path, relative: str) -> Path:
    root = root.resolve()
    candidate = (root / Path(*PurePosixPath(relative).parts)).resolve()
    if root not in (candidate, *candidate.parents):
        raise SyncError(f"staged path escapes its root: {relative}")
    if not candidate.is_file():
        raise SyncError(f"staged file is missing: {candidate}")
    return candidate


def validate_url(raw: Any, label: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise SyncError(f"{label} must be a non-empty URL")
    value = raw.strip()
    if any(character.isspace() for character in value) or any(
        character in value for character in "<>"
    ):
        raise SyncError(f"{label} contains unsafe URL characters")
    split = urlsplit(value)
    if split.scheme not in {"http", "https"} or not split.netloc:
        raise SyncError(f"{label} must use http or https: {value}")
    if split.username or split.password:
        raise SyncError(f"{label} must not contain URL credentials")
    for key, _ in parse_qsl(split.query, keep_blank_values=True):
        folded = key.casefold()
        if any(part in folded for part in SENSITIVE_QUERY_PARTS):
            raise SyncError(f"{label} contains a sensitive query parameter: {key}")
    return value


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SyncError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SyncError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SyncError(f"JSON root must be an object: {path}")
    return data


def normalized_coverage(raw: Any, page_count: int, allow_partial: bool) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise SyncError("inventory.coverage must be an object")
    discovered = raw.get("discovered")
    captured = raw.get("captured")
    failed = raw.get("failed", [])
    excluded = raw.get("excluded", [])
    if not isinstance(discovered, int) or discovered < 0:
        raise SyncError("coverage.discovered must be a non-negative integer")
    if not isinstance(captured, int) or captured < 0:
        raise SyncError("coverage.captured must be a non-negative integer")
    if not isinstance(failed, list) or not isinstance(excluded, list):
        raise SyncError("coverage.failed and coverage.excluded must be arrays")
    if captured != page_count:
        raise SyncError(
            f"coverage.captured ({captured}) does not match pages ({page_count})"
        )
    if discovered != captured + len(failed):
        raise SyncError(
            "coverage.discovered must equal captured plus the number of failed pages"
        )
    if (failed or discovered != captured) and not allow_partial:
        raise SyncError(
            f"INCOMPLETE: {len(failed)} failed page(s); refusing to modify the Skill"
        )
    return {
        "discovered": discovered,
        "captured": captured,
        "failed": sorted(failed, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False)),
        "excluded": sorted(excluded, key=lambda item: json.dumps(item, sort_keys=True, ensure_ascii=False)),
        "complete": not failed and discovered == captured,
    }


def load_staged_corpus(staging_dir: Path, allow_partial: bool = False) -> StagedCorpus:
    staging_dir = staging_dir.resolve()
    inventory = read_json(staging_dir / "inventory.json")
    if inventory.get("schema_version") != 1:
        raise SyncError("inventory.schema_version must be 1")
    source_root = validate_url(inventory.get("source_root"), "inventory.source_root")
    raw_pages = inventory.get("pages")
    raw_assets = inventory.get("assets", [])
    if not isinstance(raw_pages, list) or not raw_pages:
        raise SyncError("inventory.pages must be a non-empty array")
    if not isinstance(raw_assets, list):
        raise SyncError("inventory.assets must be an array")
    coverage = normalized_coverage(
        inventory.get("coverage"), len(raw_pages), allow_partial
    )

    pages: list[Page] = []
    seen_paths: set[str] = set()
    seen_urls: set[str] = set()
    for index, raw in enumerate(raw_pages):
        if not isinstance(raw, dict):
            raise SyncError(f"pages[{index}] must be an object")
        title = raw.get("title")
        if not isinstance(title, str) or not title.strip():
            raise SyncError(f"pages[{index}].title must be a non-empty string")
        source_url = validate_url(raw.get("source_url"), f"pages[{index}].source_url")
        source_path = raw.get("source_path", urlsplit(source_url).path or "/")
        if not isinstance(source_path, str) or not source_path:
            raise SyncError(f"pages[{index}].source_path must be a non-empty string")
        local_path = safe_relative(raw.get("local_path"), markdown=True)
        if local_path in seen_paths:
            raise SyncError(f"duplicate document local_path: {local_path}")
        if source_url in seen_urls:
            raise SyncError(f"duplicate document source_url: {source_url}")
        seen_paths.add(local_path)
        seen_urls.add(source_url)

        source_file = safe_staged_file(staging_dir / "docs", local_path)
        try:
            normalized = normalize_markdown(source_file.read_text(encoding="utf-8"))
        except UnicodeDecodeError as exc:
            raise SyncError(f"document is not UTF-8: {source_file}") from exc
        if not normalized.strip():
            raise SyncError(f"document is empty: {source_file}")
        summary = raw.get("summary", "")
        if not isinstance(summary, str):
            raise SyncError(f"pages[{index}].summary must be a string")
        keywords = raw.get("keywords", [])
        if not isinstance(keywords, list) or not all(
            isinstance(item, str) for item in keywords
        ):
            raise SyncError(f"pages[{index}].keywords must be an array of strings")
        data = normalized.encode("utf-8")
        pages.append(
            Page(
                title=title.strip(),
                source_url=source_url,
                source_path=source_path,
                local_path=local_path,
                summary=summary.strip(),
                keywords=sorted({item.strip() for item in keywords if item.strip()}),
                content=data,
                content_hash=sha256(data),
            )
        )

    assets: list[Asset] = []
    seen_asset_paths: set[str] = set()
    for index, raw in enumerate(raw_assets):
        if not isinstance(raw, dict):
            raise SyncError(f"assets[{index}] must be an object")
        source_url = validate_url(raw.get("source_url"), f"assets[{index}].source_url")
        local_path = safe_relative(raw.get("local_path"), markdown=False)
        if local_path in seen_asset_paths:
            raise SyncError(f"duplicate asset local_path: {local_path}")
        seen_asset_paths.add(local_path)
        content = safe_staged_file(staging_dir / "assets", local_path).read_bytes()
        if not content:
            raise SyncError(f"asset is empty: {local_path}")
        assets.append(
            Asset(
                source_url=source_url,
                local_path=local_path,
                content=content,
                content_hash=sha256(content),
            )
        )

    pages.sort(key=lambda item: item.local_path)
    assets.sort(key=lambda item: item.local_path)
    return StagedCorpus(
        source_root=source_root,
        coverage=coverage,
        pages=pages,
        assets=assets,
    )


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def current_file_hash(path: Path, markdown: bool) -> str | None:
    if not path.is_file():
        return None
    if markdown:
        try:
            data = normalize_markdown(path.read_text(encoding="utf-8")).encode("utf-8")
        except UnicodeDecodeError:
            return None
    else:
        data = path.read_bytes()
    return sha256(data)


def comparable(entry: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in entry.items() if key != "updated_at"}


def render_tree(paths: list[str]) -> list[str]:
    tree: dict[str, Any] = {}
    for raw in paths:
        cursor = tree
        parts = PurePosixPath(raw).parts
        for part in parts[:-1]:
            node = cursor.setdefault(part, {})
            if not isinstance(node, dict):
                raise SyncError(f"path collision while rendering tree: {raw}")
            cursor = node
        cursor[parts[-1]] = None

    lines = ["docs/"]

    def visit(node: dict[str, Any], prefix: str) -> None:
        names = sorted(node, key=lambda name: (node[name] is None, name.casefold()))
        for position, name in enumerate(names):
            last = position == len(names) - 1
            lines.append(f"{prefix}{'└── ' if last else '├── '}{name}")
            child = node[name]
            if isinstance(child, dict):
                visit(child, prefix + ("    " if last else "│   "))

    visit(tree, "")
    return lines


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def render_index(
    title: str,
    source_root: str,
    entries: dict[str, dict[str, Any]],
) -> bytes:
    top_counts = Counter(
        PurePosixPath(path).parts[0] if len(PurePosixPath(path).parts) > 1 else "(root)"
        for path in entries
    )
    lines = [
        f"# {title} 文档索引",
        "",
        "本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。",
        "",
        f"- 来源：<{source_root}>",
        f"- 文档数：{len(entries)}",
        "",
        "## 顶层目录",
        "",
    ]
    for group, count in sorted(top_counts.items(), key=lambda item: item[0].casefold()):
        lines.append(f"- `{group}`：{count} 篇")
    lines.extend(["", "## 目录树", "", "```text", *render_tree(list(entries)), "```", ""])
    lines.extend(
        [
            "## 全部文档",
            "",
            "| 路径 | 标题 | 摘要 / 关键词 | 来源 |",
            "|---|---|---|---|",
        ]
    )
    for path, entry in sorted(entries.items()):
        summary = entry.get("summary", "")
        keywords = entry.get("keywords", [])
        detail = summary
        if keywords:
            suffix = ", ".join(keywords)
            detail = f"{detail}；{suffix}" if detail else suffix
        lines.append(
            "| `{}` | {} | {} | [原文]({}) |".format(
                path.replace("`", "\\`"),
                escape_cell(str(entry.get("title", ""))),
                escape_cell(detail),
                "<" + str(entry.get("source_url", "")) + ">",
            )
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def detect_untracked(root: Path, expected: set[str]) -> list[str]:
    if not root.exists():
        return []
    found = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    }
    return sorted(found - expected)


def sync_skill(
    skill_root: Path,
    staging_dir: Path,
    *,
    dry_run: bool = False,
    prune: bool = False,
    allow_partial: bool = False,
) -> SyncSummary:
    skill_root = skill_root.resolve()
    manifest_path = skill_root / "references" / "wiki-manifest.json"
    manifest = read_json(manifest_path)
    if manifest.get("schema_version") != 1:
        raise SyncError("wiki-manifest.schema_version must be 1")
    wiki = manifest.get("wiki")
    if not isinstance(wiki, dict):
        raise SyncError("wiki-manifest.wiki must be an object")
    title = wiki.get("title")
    manifest_source = wiki.get("source_root")
    if not isinstance(title, str) or not title:
        raise SyncError("wiki-manifest.wiki.title is missing")
    if not isinstance(manifest_source, str) or not manifest_source:
        raise SyncError("wiki-manifest.wiki.source_root is missing")

    corpus = load_staged_corpus(staging_dir, allow_partial=allow_partial)
    if corpus.source_root.rstrip("/") != manifest_source.rstrip("/"):
        raise SyncError(
            "inventory.source_root does not match the generated Skill manifest"
        )

    old_documents = manifest.get("documents", {})
    old_assets = manifest.get("assets", {})
    if not isinstance(old_documents, dict) or not isinstance(old_assets, dict):
        raise SyncError("wiki-manifest documents/assets must be objects")

    docs_root = skill_root / "references" / "docs"
    assets_root = skill_root / "references" / "assets"
    untracked_docs = detect_untracked(docs_root, set(old_documents))
    untracked_assets = detect_untracked(assets_root, set(old_assets))
    if untracked_docs or untracked_assets:
        details = ", ".join(
            [*(f"docs/{item}" for item in untracked_docs), *(f"assets/{item}" for item in untracked_assets)]
        )
        raise SyncError(f"untracked live files require review before sync: {details}")

    now = utc_now()
    new_documents: dict[str, dict[str, Any]] = {}
    changed_page_content: dict[str, bytes] = {}
    added_documents = changed_documents = unchanged_documents = 0
    for page in corpus.pages:
        base = {
            "title": page.title,
            "source_url": page.source_url,
            "source_path": page.source_path,
            "local_path": page.local_path,
            "summary": page.summary,
            "keywords": page.keywords,
            "content_hash": page.content_hash,
        }
        old = old_documents.get(page.local_path)
        live_hash = current_file_hash(docs_root / page.local_path, markdown=True)
        if isinstance(old, dict) and comparable(old) == base and live_hash == page.content_hash:
            new_documents[page.local_path] = old
            unchanged_documents += 1
        else:
            new_documents[page.local_path] = {**base, "updated_at": now}
            if live_hash != page.content_hash:
                changed_page_content[page.local_path] = page.content
            if old is None:
                added_documents += 1
            else:
                changed_documents += 1

    new_assets: dict[str, dict[str, Any]] = {}
    changed_asset_content: dict[str, bytes] = {}
    added_assets = changed_assets = unchanged_assets = 0
    for asset in corpus.assets:
        base = {
            "source_url": asset.source_url,
            "local_path": asset.local_path,
            "content_hash": asset.content_hash,
        }
        old = old_assets.get(asset.local_path)
        live_hash = current_file_hash(assets_root / asset.local_path, markdown=False)
        if isinstance(old, dict) and comparable(old) == base and live_hash == asset.content_hash:
            new_assets[asset.local_path] = old
            unchanged_assets += 1
        else:
            new_assets[asset.local_path] = {**base, "updated_at": now}
            if live_hash != asset.content_hash:
                changed_asset_content[asset.local_path] = asset.content
            if old is None:
                added_assets += 1
            else:
                changed_assets += 1

    stale_documents = sorted(set(old_documents) - set(new_documents))
    stale_assets = sorted(set(old_assets) - set(new_assets))
    if (stale_documents or stale_assets) and not prune:
        raise StaleFilesError(
            "STALE_REQUIRES_APPROVAL: "
            f"{len(stale_documents)} document(s) and {len(stale_assets)} asset(s) "
            "would leave the live tree; rerun with --prune only after authorization"
        )

    new_manifest = {
        "schema_version": 1,
        "wiki": wiki,
        "coverage": corpus.coverage,
        "documents": new_documents,
        "assets": new_assets,
        "created_at": manifest.get("created_at", now),
    }
    index_bytes = render_index(title, manifest_source, new_documents)
    current_index = skill_root / "references" / "INDEX.md"
    index_changed = not current_index.is_file() or current_index.read_bytes() != index_bytes

    manifest_comparable = {
        key: value for key, value in manifest.items() if key != "last_sync_at"
    }
    semantic_change = manifest_comparable != new_manifest
    any_change = bool(
        changed_page_content
        or changed_asset_content
        or stale_documents
        or stale_assets
        or index_changed
        or semantic_change
    )
    if not any_change:
        return SyncSummary(
            status="UNCHANGED",
            added_documents=0,
            changed_documents=0,
            unchanged_documents=unchanged_documents,
            removed_documents=0,
            added_assets=0,
            changed_assets=0,
            unchanged_assets=unchanged_assets,
            removed_assets=0,
        )

    if dry_run:
        return SyncSummary(
            status="DRY_RUN",
            added_documents=added_documents,
            changed_documents=changed_documents,
            unchanged_documents=unchanged_documents,
            removed_documents=len(stale_documents),
            added_assets=added_assets,
            changed_assets=changed_assets,
            unchanged_assets=unchanged_assets,
            removed_assets=len(stale_assets),
        )

    for relative, content in changed_page_content.items():
        atomic_write(docs_root / relative, content)
    for relative, content in changed_asset_content.items():
        atomic_write(assets_root / relative, content)

    if stale_documents or stale_assets:
        archive_root = skill_root / "references" / ".baize-trash" / now.replace(":", "")
        for relative in stale_documents:
            source = docs_root / relative
            if source.exists():
                destination = archive_root / "docs" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))
        for relative in stale_assets:
            source = assets_root / relative
            if source.exists():
                destination = archive_root / "assets" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(destination))

    new_manifest["last_sync_at"] = now
    manifest_bytes = (
        json.dumps(new_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    atomic_write(current_index, index_bytes)
    atomic_write(manifest_path, manifest_bytes)
    return SyncSummary(
        status="CHANGED",
        added_documents=added_documents,
        changed_documents=changed_documents,
        unchanged_documents=unchanged_documents,
        removed_documents=len(stale_documents),
        added_assets=added_assets,
        changed_assets=changed_assets,
        unchanged_assets=unchanged_assets,
        removed_assets=len(stale_assets),
    )


def print_summary(summary: SyncSummary) -> None:
    print(summary.status)
    print(
        "documents: "
        f"added={summary.added_documents} changed={summary.changed_documents} "
        f"unchanged={summary.unchanged_documents} removed={summary.removed_documents}"
    )
    print(
        "assets: "
        f"added={summary.added_assets} changed={summary.changed_assets} "
        f"unchanged={summary.unchanged_assets} removed={summary.removed_assets}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", required=True, type=Path)
    parser.add_argument("--staging-dir", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Archive files removed upstream; requires prior authorization",
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Accept failed pages; use only after the user accepts an incomplete snapshot",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        summary = sync_skill(
            args.skill_root,
            args.staging_dir,
            dry_run=args.dry_run,
            prune=args.prune,
            allow_partial=args.allow_partial,
        )
    except StaleFilesError as exc:
        print(str(exc), file=sys.stderr)
        return 3
    except SyncError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2
    print_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
