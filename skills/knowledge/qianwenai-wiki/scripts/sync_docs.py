#!/usr/bin/env python3
"""Download every page listed by the official Qianwen AI Platform llms.txt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen


INDEX_URL = "https://platform.qianwenai.com/docs/llms.txt"
DOC_PREFIX = "https://platform.qianwenai.com/docs/"
LINK_RE = re.compile(r"https://platform\.qianwenai\.com/docs/[^)\s]+")
USER_AGENT = "qianwenai-wiki-sync/1.0 (+offline documentation snapshot)"
SECRET_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(
        r"(?i)((?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*)(['\"])[^'\"\n]{12,}(['\"])"
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replace", action="store_true", help="Replace an existing verified snapshot")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent downloads (default: 8)")
    parser.add_argument("--timeout", type=float, default=30.0, help="Per-request timeout in seconds")
    parser.add_argument("--retries", type=int, default=3, help="Attempts per URL")
    return parser.parse_args()


def fetch(url: str, timeout: float, retries: int) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
        try:
            with urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                data = response.read()
                if not data.strip():
                    raise RuntimeError("empty response")
                return data
        except (HTTPError, URLError, TimeoutError, RuntimeError, OSError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 ** (attempt - 1), 4))
    raise RuntimeError(f"failed after {retries} attempts: {url}: {last_error}")


def relative_path(url: str) -> Path:
    if not url.startswith(DOC_PREFIX):
        raise ValueError(f"URL outside official docs prefix: {url}")
    parsed = urlparse(url)
    raw = unquote(parsed.path.removeprefix("/docs/"))
    posix = PurePosixPath(raw)
    if not raw or posix.is_absolute() or any(part in {"", ".", ".."} for part in posix.parts):
        raise ValueError(f"unsafe document path: {url}")
    if posix.suffix not in {".md", ".json"}:
        raise ValueError(f"unsupported document type: {url}")
    return Path(*posix.parts)


def sanitize(data: bytes) -> tuple[bytes, int, int]:
    """Redact key-shaped literals and normalize tabs for repository-safe text."""
    text = data.decode("utf-8")
    replacements = 0
    normalized_tabs = text.count("\t")

    def redact_sk(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1
        return "sk-REDACTED"

    def redact_assignment(match: re.Match[str]) -> str:
        nonlocal replacements
        replacements += 1
        return f"{match.group(1)}{match.group(2)}REDACTED{match.group(3)}"

    text = SECRET_PATTERNS[0].sub(redact_sk, text)
    text = SECRET_PATTERNS[1].sub(redact_assignment, text)
    text = text.replace("\t", "    ")
    return text.encode("utf-8"), replacements, normalized_tabs


def install_snapshot(staged: Path, target: Path, replace: bool) -> None:
    if target.exists() and any(target.iterdir()):
        if not replace:
            raise RuntimeError(f"snapshot already exists at {target}; rerun with --replace after confirmation")
        backup = target.with_name(f"{target.name}.backup-{os.getpid()}")
        target.replace(backup)
        try:
            staged.replace(target)
        except Exception:
            backup.replace(target)
            raise
        shutil.rmtree(backup)
    else:
        if target.exists():
            target.rmdir()
        staged.replace(target)


def main() -> int:
    args = parse_args()
    if args.workers < 1 or args.workers > 32 or args.timeout <= 0 or args.retries < 1:
        print("workers must be 1..32; timeout and retries must be positive", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parents[1]
    references = skill_root / "references"
    docs_target = references / "docs"
    if docs_target.exists() and any(docs_target.iterdir()) and not args.replace:
        print(f"snapshot already exists at {docs_target}; rerun with --replace after confirmation", file=sys.stderr)
        return 2

    try:
        index_bytes = fetch(INDEX_URL, args.timeout, args.retries)
        index_text = index_bytes.decode("utf-8")
        urls = sorted(set(LINK_RE.findall(index_text)))
        if not urls:
            raise RuntimeError("official index contained no document links")
        paths = [relative_path(url) for url in urls]
        if len(set(paths)) != len(paths):
            raise RuntimeError("multiple source URLs map to the same local path")

        with tempfile.TemporaryDirectory(prefix=".qianwenai-sync-", dir=skill_root) as temp_dir:
            staged_root = Path(temp_dir)
            staged_docs = staged_root / "docs"
            staged_docs.mkdir()
            results: list[dict[str, object]] = []

            def download(url: str, rel: Path) -> dict[str, object]:
                source_data = fetch(url, args.timeout, args.retries)
                data, sanitized_replacements, normalized_tabs = sanitize(source_data)
                if rel.suffix == ".json":
                    json.loads(data.decode("utf-8"))
                destination = staged_docs / rel
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                return {
                    "path": rel.as_posix(),
                    "source_url": url,
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "source_bytes": len(source_data),
                    "source_sha256": hashlib.sha256(source_data).hexdigest(),
                    "sanitized_replacements": sanitized_replacements,
                    "normalized_tabs": normalized_tabs,
                }

            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = {executor.submit(download, url, rel): url for url, rel in zip(urls, paths)}
                for completed, future in enumerate(as_completed(futures), start=1):
                    results.append(future.result())
                    if completed % 50 == 0 or completed == len(futures):
                        print(f"Downloaded {completed}/{len(futures)}", file=sys.stderr)

            results.sort(key=lambda item: str(item["path"]))
            if len(results) != len(urls):
                raise RuntimeError(f"downloaded {len(results)} of {len(urls)} indexed documents")

            snapshot = {
                "source_index": INDEX_URL,
                "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "document_count": len(results),
                "markdown_count": sum(str(item["path"]).endswith(".md") for item in results),
                "json_count": sum(str(item["path"]).endswith(".json") for item in results),
                "total_bytes": sum(int(item["bytes"]) for item in results),
                "source_total_bytes": sum(int(item["source_bytes"]) for item in results),
                "sanitized_replacements": sum(int(item["sanitized_replacements"]) for item in results),
                "normalized_tabs": sum(int(item["normalized_tabs"]) for item in results),
                "index_sha256": hashlib.sha256(index_bytes).hexdigest(),
                "files": results,
            }
            index_header = (
                "<!-- Offline snapshot of the official Qianwen AI Platform llms.txt. "
                f"Fetched {snapshot['fetched_at']}; {len(results)} documents. -->\n\n"
            )
            (staged_root / "INDEX.md").write_text(index_header + index_text, encoding="utf-8")
            (staged_root / "SNAPSHOT.json").write_text(
                json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

            references.mkdir(exist_ok=True)
            install_snapshot(staged_docs, docs_target, args.replace)
            for name in ("INDEX.md", "SNAPSHOT.json"):
                source = staged_root / name
                target = references / name
                if target.exists() and not args.replace:
                    raise RuntimeError(f"{target} already exists; rerun with --replace after confirmation")
                source.replace(target)

        print(
            f"Snapshot complete: {snapshot['document_count']} documents "
            f"({snapshot['markdown_count']} Markdown, {snapshot['json_count']} JSON), "
            f"{snapshot['total_bytes']} bytes"
        )
        return 0
    except (RuntimeError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
