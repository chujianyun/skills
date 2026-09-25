#!/usr/bin/env python3
"""Generate a WeChat Official Account QR code URL from an account ID."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = "https://open.weixin.qq.com/qr/code?username="
VALID_ID = re.compile(r"^[A-Za-z0-9_-]{3,128}$")


def normalize_account_id(raw: str) -> str:
    value = raw.strip()
    parsed = urllib.parse.urlparse(value)

    if parsed.scheme and parsed.netloc:
        query = urllib.parse.parse_qs(parsed.query)
        usernames = query.get("username")
        if usernames:
            value = usernames[0].strip()

    value = urllib.parse.unquote(value).strip()
    if not value:
        raise ValueError("公众号ID不能为空")
    if not VALID_ID.fullmatch(value):
        raise ValueError("公众号ID只能包含英文字母、数字、下划线或短横线")
    return value


def qr_url(account_id: str) -> str:
    return BASE_URL + urllib.parse.quote(account_id, safe="")


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        output.write_bytes(response.read())


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a WeChat Official Account follow QR code URL."
    )
    parser.add_argument("account_id", help="公众号ID, such as gh_11eec77a7c51, or a QR URL")
    parser.add_argument("--download", action="store_true", help="Download the QR image")
    parser.add_argument(
        "--output",
        help="Output image path when --download is used. Defaults to ~/Downloads/wechat-qrcodes/<account_id>.jpg",
    )
    args = parser.parse_args()

    try:
        account_id = normalize_account_id(args.account_id)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    url = qr_url(account_id)
    print(f"公众号ID：{account_id}")
    print(f"二维码链接：{url}")

    if args.download:
        output = Path(args.output).expanduser() if args.output else Path("~/Downloads/wechat-qrcodes").expanduser() / f"{account_id}.jpg"
        download(url, output)
        resolved = output.resolve()
        print()
        print(f"本地图片：{resolved}")
        print()
        print(f"![微信公众号二维码]({resolved})")
    else:
        print()
        print(f"![微信公众号二维码]({url})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
