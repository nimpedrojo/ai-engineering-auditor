#!/usr/bin/env python3

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"

REQUIRED_PAYLOAD_FIELDS = [
    "eventType",
    "phase",
    "tool",
    "title",
]

OPTIONAL_PAYLOAD_FIELDS = [
    "description",
    "taskId",
    "severity",
    "purpose",
    "result",
    "accepted",
    "metadata",
]


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_event_id(events_file: Path) -> str:
    if not events_file.exists():
        return "EVT-000001"

    count = 0

    with events_file.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                count += 1

    return f"EVT-{count + 1:06d}"


def validate_payload(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValueError("Event payload must be a JSON object.")

    missing = [
        field
        for field in REQUIRED_PAYLOAD_FIELDS
        if field not in payload or payload[field] in (None, "")
    ]

    if missing:
        raise ValueError(
            "Missing required event field(s): " + ", ".join(missing)
        )

    if "metadata" in payload and payload["metadata"] is not None:
        if not isinstance(payload["metadata"], dict):
            raise ValueError("metadata must be a JSON object.")


def create_event(
    *,
    events_file: Path,
    payload: dict[str, Any],
) -> dict[str, Any]:
    validate_payload(payload)

    event: dict[str, Any] = {
        "eventId": next_event_id(events_file),
        "timestamp": utc_now(),
        "schemaVersion": SCHEMA_VERSION,
        "eventType": payload["eventType"],
        "phase": payload["phase"],
        "tool": payload["tool"],
        "title": payload["title"],
        "description": payload.get("description", ""),
    }

    for field in OPTIONAL_PAYLOAD_FIELDS:
        if field in payload and payload[field] is not None:
            event[field] = deepcopy(payload[field])

    return event


def append_event(
    events_file: Path,
    event: dict[str, Any],
) -> None:
    events_file.parent.mkdir(parents=True, exist_ok=True)

    with events_file.open("a", encoding="utf-8") as file:
        json.dump(
            event,
            file,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        file.write("\n")


def create_and_append(
    *,
    events_file: Path,
    payload: dict[str, Any],
) -> dict[str, Any]:
    event = create_event(
        events_file=events_file,
        payload=payload,
    )

    append_event(events_file, event)

    return event