#!/usr/bin/env python3
"""Lightweight OpenAI API connectivity test for the workflow.

Reads credentials from:
1. current environment, or
2. ~/.config/unilabos/openai.env

This script is intentionally dependency-free.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


SECRET_ENV_PATH = Path.home() / ".config" / "unilabos" / "openai.env"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def main() -> int:
    load_env_file(SECRET_ENV_PATH)

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    if not api_key:
        print(f"Missing OPENAI_API_KEY. Fill it in at: {SECRET_ENV_PATH}", file=sys.stderr)
        return 2

    url = f"{base_url}/models"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code} from {url}", file=sys.stderr)
        print(body[:1000], file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1

    data = payload.get("data", [])
    print(f"API ok: listed {len(data)} models from {base_url}")
    for item in data[:10]:
        model_id = item.get("id")
        if model_id:
            print(f"- {model_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
