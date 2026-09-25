#!/usr/bin/env python3
"""Create a local workspace for an arXiv paper and download its assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, parse, request
from xml.etree import ElementTree


DEFAULT_BASE_DIR = Path("~/Documents/working/papers").expanduser()
USER_AGENT = "paper-interpreter/1.0 (+https://arxiv.org)"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local arXiv paper workspace and download PDF/source."
    )
    parser.add_argument("url", help="arXiv URL, such as https://arxiv.org/abs/2401.00001")
    parser.add_argument(
        "base_dir",
        nargs="?",
        default=str(DEFAULT_BASE_DIR),
        help="Base directory for paper folders. Defaults to ~/Documents/working/papers",
    )
    return parser.parse_args()


def extract_arxiv_id(url: str) -> str:
    parsed = parse.urlparse(url)
    if "arxiv.org" not in parsed.netloc:
        raise ValueError(f"Unsupported domain: {parsed.netloc or url}")

    path = parsed.path.strip("/")
    if not path:
        raise ValueError(f"Could not extract arXiv ID from URL: {url}")

    if path.startswith(("abs/", "pdf/", "html/", "e-print/")):
        paper_id = path.split("/", 1)[1]
    else:
        paper_id = path

    if paper_id.endswith(".pdf"):
        paper_id = paper_id[:-4]

    paper_id = paper_id.strip()
    if not paper_id:
        raise ValueError(f"Could not extract arXiv ID from URL: {url}")
    return paper_id


def http_get(url: str) -> request.addinfourl:
    req = request.Request(url, headers={"User-Agent": USER_AGENT})
    return request.urlopen(req, timeout=30)


def fetch_metadata(arxiv_id: str) -> dict[str, Any]:
    encoded_id = parse.quote(arxiv_id, safe="")
    api_url = f"https://export.arxiv.org/api/query?id_list={encoded_id}"
    with http_get(api_url) as response:
        xml_bytes = response.read()

    root = ElementTree.fromstring(xml_bytes)
    entry = root.find("atom:entry", ATOM_NS)
    if entry is None:
        raise RuntimeError(f"No metadata returned for arXiv ID: {arxiv_id}")

    def text(path: str) -> str:
        node = entry.find(path, ATOM_NS)
        if node is None or node.text is None:
            return ""
        return " ".join(node.text.split())

    authors = [
        " ".join(author.text.split())
        for author in entry.findall("atom:author/atom:name", ATOM_NS)
        if author.text
    ]
    categories = [
        cat.attrib["term"]
        for cat in entry.findall("atom:category", ATOM_NS)
        if cat.attrib.get("term")
    ]

    primary_category_node = entry.find("arxiv:primary_category", ATOM_NS)
    primary_category = (
        primary_category_node.attrib.get("term", "") if primary_category_node is not None else ""
    )

    return {
        "arxiv_id": arxiv_id,
        "title": text("atom:title"),
        "abstract": text("atom:summary"),
        "authors": authors,
        "published": text("atom:published"),
        "updated": text("atom:updated"),
        "comment": text("arxiv:comment"),
        "journal_ref": text("arxiv:journal_ref"),
        "doi": text("arxiv:doi"),
        "primary_category": primary_category,
        "categories": categories,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "source_url": f"https://arxiv.org/e-print/{arxiv_id}",
    }


def sanitize_folder_name(title: str, fallback: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", " ", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    if not cleaned:
        cleaned = fallback.replace("/", "-")
    return cleaned[:120].rstrip(" .")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_to_path(url: str, destination: Path) -> Path:
    with http_get(url) as response, destination.open("wb") as fh:
        while True:
            chunk = response.read(1024 * 64)
            if not chunk:
                break
            fh.write(chunk)
    return destination


def infer_source_filename(headers: Any) -> str:
    content_disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', content_disposition)
    if match:
        return match.group(1)

    content_type = headers.get_content_type()
    if "gzip" in content_type:
        return "source.tar.gz"
    if "tar" in content_type:
        return "source.tar"
    if content_type == "application/pdf":
        return "source.pdf"
    return "source"


def download_source(url: str, paper_dir: Path) -> Path | None:
    try:
        with http_get(url) as response:
            filename = infer_source_filename(response.headers)
            destination = paper_dir / filename
            with destination.open("wb") as fh:
                while True:
                    chunk = response.read(1024 * 64)
                    if not chunk:
                        break
                    fh.write(chunk)
        return destination
    except error.HTTPError as exc:
        if exc.code in {403, 404}:
            return None
        raise


def maybe_extract_source(source_path: Path | None, paper_dir: Path) -> Path | None:
    if source_path is None or not source_path.exists():
        return None

    extract_dir = paper_dir / "source"
    ensure_dir(extract_dir)
    try:
        with tarfile.open(source_path, "r:*") as archive:
            base = extract_dir.resolve()
            for member in archive.getmembers():
                target = (extract_dir / member.name).resolve()
                if not str(target).startswith(str(base) + "/") and target != base:
                    raise RuntimeError(f"Unsafe archive member path: {member.name}")
            archive.extractall(extract_dir)
        return extract_dir
    except (tarfile.TarError, RuntimeError):
        return None


def write_metadata(metadata: dict[str, Any], metadata_path: Path) -> None:
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def maybe_create_report(report_path: Path, metadata: dict[str, Any]) -> None:
    if report_path.exists():
        return

    authors = "、".join(metadata["authors"]) if metadata["authors"] else "未知"
    categories = ", ".join(metadata["categories"]) if metadata["categories"] else "未知"
    created_at = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    report = f"""# {metadata['title']}

- arXiv ID: {metadata['arxiv_id']}
- 原始链接: {metadata['abs_url']}
- 作者: {authors}
- 发布时间: {metadata['published'] or '未知'}
- 更新时间: {metadata['updated'] or '未知'}
- 学科分类: {categories}

## 一句话总结

待补充。

## 论文要解决什么问题

待补充。

## 核心思路

待补充。

```mermaid
flowchart TD
    A[研究问题] --> B[核心方法]
    B --> C[实验验证]
    C --> D[结论]
```

## 方法细拆

待补充。

## 训练 / 推理流程

待补充。

## 实验设置与结果

待补充。

## 这篇论文真正的贡献

待补充。

## 局限与适用边界

待补充。

## 对后续研究/应用的启发

待补充。

## 术语表

待补充。

## 原始摘要

{metadata['abstract'] or '无'}

## 复查记录

- {created_at}: 初始化论文目录并创建报告骨架。
"""
    report_path.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    base_dir = Path(args.base_dir).expanduser().resolve()
    ensure_dir(base_dir)

    arxiv_id = extract_arxiv_id(args.url)
    metadata = fetch_metadata(arxiv_id)
    folder_name = sanitize_folder_name(metadata["title"], arxiv_id)
    paper_dir = base_dir / folder_name
    ensure_dir(paper_dir)

    # 使用论文标题作为文件名
    paper_filename = sanitize_folder_name(metadata["title"], arxiv_id) + ".pdf"
    pdf_path = download_to_path(metadata["pdf_url"], paper_dir / paper_filename)
    source_path = download_source(metadata["source_url"], paper_dir)
    source_extract_dir = maybe_extract_source(source_path, paper_dir)
    report_filename = sanitize_folder_name(metadata["title"], arxiv_id) + "_报告.md"
    report_path = paper_dir / report_filename

    metadata["paper_dir"] = str(paper_dir)
    metadata["pdf_path"] = str(pdf_path)
    metadata["source_path"] = str(source_path) if source_path else None
    metadata["source_extract_dir"] = str(source_extract_dir) if source_extract_dir else None
    metadata["report_path"] = str(report_path)
    metadata["downloaded_at"] = datetime.now(timezone.utc).isoformat()

    write_metadata(metadata, paper_dir / "metadata.json")
    maybe_create_report(report_path, metadata)

    print(
        json.dumps(
            {
                "paper_dir": str(paper_dir),
                "report_path": str(report_path),
                "pdf_path": str(pdf_path),
                "source_path": str(source_path) if source_path else None,
                "source_extract_dir": str(source_extract_dir) if source_extract_dir else None,
                "metadata_path": str(paper_dir / "metadata.json"),
                "arxiv_id": arxiv_id,
                "title": metadata["title"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(130)
