#!/usr/bin/env python3
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path("/Users/liuwangyang/Documents/coding/our/skills/skills/claudian-installer")
SKILL_MD = ROOT / "SKILL.md"
ASSETS = ROOT / "assets"
MANIFEST = ASSETS / "manifest.json"
FILES = ["main.js", "manifest.json", "styles.css"]
API_URL = "https://api.github.com/repos/YishenTu/claudian/releases/latest"
VERSION_HEADING = "## Bundled Version"
VERSION_RE = re.compile(r"^Current bundled Claudian version:\s*(?P<version>\S+)\s*$", re.MULTILINE)


def normalize_version(value: str) -> str:
    return value.strip().lstrip("vV")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def read_manifest_version() -> str:
    data = json.loads(read_text(MANIFEST))
    version = data.get("version")
    if not version:
        raise RuntimeError("manifest.json missing version")
    return normalize_version(str(version))


def read_recorded_version(skill_text: str) -> str | None:
    m = VERSION_RE.search(skill_text)
    return normalize_version(m.group("version")) if m else None


def ensure_version_line(skill_text: str, version: str) -> str:
    block = f"{VERSION_HEADING}\n\nCurrent bundled Claudian version: {version}\n"
    if VERSION_RE.search(skill_text):
        return VERSION_RE.sub(f"Current bundled Claudian version: {version}", skill_text, count=1)
    anchor = "## Installation Workflow"
    if anchor in skill_text:
        return skill_text.replace(anchor, block + "\n" + anchor, 1)
    return skill_text.rstrip() + "\n\n" + block + "\n"


def fetch_latest_release() -> dict:
    req = urllib.request.Request(API_URL, headers={"User-Agent": "claudian-installer-updater"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def collect_asset_urls(release: dict) -> tuple[str, dict[str, str]]:
    tag = normalize_version(release.get("tag_name") or release.get("name") or "")
    if not tag:
        raise RuntimeError("latest release missing tag_name")
    assets = {}
    for item in release.get("assets", []):
        name = item.get("name")
        url = item.get("browser_download_url")
        if name in FILES and url:
            assets[name] = url
    missing = [name for name in FILES if name not in assets]
    if missing:
        raise RuntimeError(f"latest release missing assets: {', '.join(missing)}")
    return tag, assets


def download(url: str, path: Path) -> None:
    result = subprocess.run(
        ["curl", "-L", "--fail", "--silent", "--show-error", url, "-o", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"download failed for {url}: {result.stderr.strip() or result.stdout.strip()}")


def atomic_replace(src: Path, dest: Path) -> None:
    tmp_dest = dest.with_suffix(dest.suffix + ".tmp")
    shutil.copy2(src, tmp_dest)
    os.replace(tmp_dest, dest)


def main() -> int:
    skill_text = read_text(SKILL_MD)
    manifest_version = read_manifest_version()
    recorded_version = read_recorded_version(skill_text)
    inserted_missing_version = False

    if not recorded_version:
        recorded_version = manifest_version
        skill_text = ensure_version_line(skill_text, recorded_version)
        write_text(SKILL_MD, skill_text)
        inserted_missing_version = True

    release = fetch_latest_release()
    latest_version, asset_urls = collect_asset_urls(release)

    summary = {
        "skill": str(ROOT),
        "recorded_version": recorded_version,
        "manifest_version": manifest_version,
        "latest_version": latest_version,
        "inserted_missing_version": inserted_missing_version,
        "updated": False,
        "changed_files": [],
    }

    if latest_version == recorded_version:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    with tempfile.TemporaryDirectory(prefix="claudian-release-") as tmp:
        tmpdir = Path(tmp)
        for name, url in asset_urls.items():
            download(url, tmpdir / name)

        downloaded_manifest = json.loads(read_text(tmpdir / "manifest.json"))
        downloaded_version = normalize_version(str(downloaded_manifest.get("version", "")))
        if downloaded_version != latest_version:
            raise RuntimeError(
                f"downloaded manifest version {downloaded_version!r} != release version {latest_version!r}"
            )

        for name in FILES:
            atomic_replace(tmpdir / name, ASSETS / name)

    final_manifest_version = read_manifest_version()
    if final_manifest_version != latest_version:
        raise RuntimeError(
            f"post-update manifest version {final_manifest_version!r} != release version {latest_version!r}"
        )

    updated_skill_text = ensure_version_line(read_text(SKILL_MD), latest_version)
    write_text(SKILL_MD, updated_skill_text)

    summary["updated"] = True
    summary["changed_files"] = FILES
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
