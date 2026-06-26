from __future__ import annotations

import argparse
import json
import sys

from aiea import Project
from aiea.event import create_and_append
from aiea.exceptions import ProjectNotInitialized


def error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_payload(path: str | None) -> dict:
    if path:
        try:
            with open(path, "r", encoding="utf-8") as file:
                raw = file.read()
        except FileNotFoundError:
            error(f"File not found: {path}")
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


def cmd_create(path: str | None) -> int:
    project = Project.current()

    if not project.context.events_file.exists():
        raise ProjectNotInitialized(
            "AI Engineering Auditor is not initialized in this project. Run: aiea-init"
        )

    payload = read_payload(path)

    event = create_and_append(
        events_file=project.context.events_file,
        payload=payload,
    )

    print(json.dumps(event, ensure_ascii=False))

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="command")

    create = sub.add_parser("create")
    create.add_argument("file", nargs="?")

    args = parser.parse_args()

    if args.command == "create":
        return cmd_create(args.file)

    parser.print_help()
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProjectNotInitialized as exc:
        print()
        print(f"ERROR: {exc}")
        print()
        raise SystemExit(1)