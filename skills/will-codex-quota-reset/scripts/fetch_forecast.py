#!/usr/bin/env python3
"""Fetch and trim the Will Codex Quota Reset forecast."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Mapping
from typing import Any


API_URL = "https://www.willcodexquotareset.com/api/forecast"
REFERER = "https://www.willcodexquotareset.com/"
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_RETRIES = 1


class ForecastError(RuntimeError):
    """Raised when the forecast cannot be fetched or validated."""


def fetch_payload_once(timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        API_URL,
        headers={
            "Accept": "application/json",
            "Referer": REFERER,
            "User-Agent": "will-codex-quota-reset-skill/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if not 200 <= status < 300:
                raise ForecastError(f"API returned HTTP {status}")
            body = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as exc:
        raise ForecastError(f"API returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", exc)
        raise ForecastError(f"network request failed: {reason}") from exc
    except TimeoutError as exc:
        raise ForecastError(f"request timed out after {timeout:g} seconds") from exc

    try:
        payload = json.loads(body.decode(charset))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ForecastError("API response is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise ForecastError("API response root must be a JSON object")
    return payload


def fetch_payload(timeout: float, retries: int) -> dict[str, Any]:
    last_error: ForecastError | None = None
    for attempt in range(retries + 1):
        try:
            return fetch_payload_once(timeout)
        except ForecastError as exc:
            last_error = exc
            retryable = (
                str(exc).startswith("network request failed:")
                or str(exc).startswith("request timed out")
                or str(exc).startswith("API returned HTTP 429")
                or str(exc).startswith("API returned HTTP 5")
            )
            if attempt == retries or not retryable:
                raise
            time.sleep(min(0.5 * (attempt + 1), 2.0))
    raise last_error or ForecastError("forecast request failed")


def require_value(forecast: Mapping[str, Any], key: str) -> Any:
    if key not in forecast:
        raise ForecastError(f"API response is missing forecast.{key}")
    return forecast[key]


def select_key_information(payload: Mapping[str, Any]) -> dict[str, Any]:
    forecast = payload.get("forecast")
    if not isinstance(forecast, Mapping):
        raise ForecastError("API response is missing the forecast object")

    score = require_value(forecast, "score")
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ForecastError("forecast.score must be a number")
    if not 0 <= score <= 100:
        raise ForecastError("forecast.score must be between 0 and 100")

    days_since_reset = require_value(forecast, "daysSinceReset")
    hours_since_reset = require_value(forecast, "hoursSinceReset")
    for key, value in (
        ("daysSinceReset", days_since_reset),
        ("hoursSinceReset", hours_since_reset),
    ):
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, (int, float))
        ):
            raise ForecastError(f"forecast.{key} must be a number or null")

    return {
        "source": API_URL,
        "fetchedAt": payload.get("fetchedAt"),
        "forecast": {
            "score": score,
            "daysSinceReset": days_since_reset,
            "hoursSinceReset": hours_since_reset,
            "hoursSinceResetAnnouncement": forecast.get(
                "hoursSinceResetAnnouncement"
            ),
            "latestResetAt": forecast.get("latestResetAt"),
            "resetAnnounced": forecast.get("resetAnnounced"),
            "breakdown": forecast.get("breakdown", []),
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch the Codex quota-reset forecast from willcodexquotareset.com."
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="print the complete API response instead of selected forecast fields",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="print JSON on one line",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"request timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS:g})",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=DEFAULT_RETRIES,
        help=f"network retries after the first attempt (default: {DEFAULT_RETRIES})",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.retries < 0:
        parser.error("--retries must be zero or greater")
    return args


def main() -> int:
    args = parse_args()
    try:
        payload = fetch_payload(args.timeout, args.retries)
        result = payload if args.raw else select_key_information(payload)
    except ForecastError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    json.dump(
        result,
        sys.stdout,
        ensure_ascii=False,
        indent=None if args.compact else 2,
        separators=(",", ":") if args.compact else None,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
