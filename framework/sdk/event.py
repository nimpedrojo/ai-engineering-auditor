#!/usr/bin/env python3

"""
AI Engineering Auditor

Event SDK

Single source of truth for creating and persisting events.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, UTC
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"


def utc_now() -> str:
    """Returns current UTC timestamp in ISO-8601 format."""

    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_event_id(events_file: Path) -> str:
    """
    Calculates the next sequential event identifier.
    """

    if not events_file.exists():
        return "EVT-000001"

    count = 0

    with events_file.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1

    return f"EVT-{count + 1:06d}"


def create_event(
    *,
    events_file: Path,
    event_type: str,
    phase: str,
    tool: str,
    title: str,
    description: str = "",
    task_id: str | None = None,
    severity: str | None = None,
    purpose: str | None = None,
    result: str | None = None,
    accepted: bool | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Creates an event object.
    """

    event = {

        "eventId": next_event_id(events_file),

        "timestamp": utc_now(),

        "schemaVersion": SCHEMA_VERSION,

        "eventType": event_type,

        "phase": phase,

        "tool": tool,

        "title": title,

        "description": description

    }

    if task_id is not None:
        event["taskId"] = task_id

    if severity is not None:
        event["severity"] = severity

    if purpose is not None:
        event["purpose"] = purpose

    if result is not None:
        event["result"] = result

    if accepted is not None:
        event["accepted"] = accepted

    if metadata:
        event["metadata"] = deepcopy(metadata)

    return event


def append_event(
    events_file: Path,
    event: dict[str, Any],
) -> None:
    """
    Appends one event to events.jsonl.
    """

    events_file.parent.mkdir(parents=True, exist_ok=True)

    with events_file.open("a", encoding="utf-8") as f:
        json.dump(
            event,
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        f.write("\n")


def create_and_append(
    *,
    events_file: Path,
    **kwargs,
) -> dict[str, Any]:
    """
    Convenience helper.
    """

    event = create_event(
        events_file=events_file,
        **kwargs,
    )

    append_event(events_file, event)

    return event