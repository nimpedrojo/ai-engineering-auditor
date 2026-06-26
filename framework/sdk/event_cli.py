#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

from event import create_and_append


def error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def read_payload() -> dict:
    if len(sys.argv) > 2:
        error("Too many arguments.")

    if len(sys.argv) == 2:
        path = Path(sys.argv[1])
        if not path.exists():
            error(f"File not found: {path}")
        raw = path.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    if not raw.strip():
        error("No JSON payload provided.")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        error(f"Invalid JSON: {exc}")

    if not isinstance(payload, dict):
        error("Payload must be a JSON object.")

    return payload


def main() -> None:
    events_file = Path.cwd() / "docs" / "ai-auditor" / "events.jsonl"

    if not events_file.parent.exists():
        error("AI Engineering Auditor is not initialized in this project.")

    payload = read_payload()

    try:
        event = create_and_append(
            events_file=events_file,
            payload=payload,
        )
    except Exception as exc:
        error(str(exc))

    print(json.dumps(event, ensure_ascii=False))


if __name__ == "__main__":
    main()