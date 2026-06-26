from __future__ import annotations

import argparse
import sys

from aiea import Project
from aiea.activity import (
    ActivityAlreadyRunning,
    NoActiveActivity,
)
from aiea.exceptions import (
    ProjectNotInitialized,
)


def cmd_status(project: Project) -> int:

    activity = project.current_activity()

    print()

    print("Current Activity")
    print("----------------")

    if activity is None:
        print("None")
    else:
        print(activity.title)

    return 0


def cmd_start(project: Project, title: str) -> int:

    activity = project.start_activity(title)

    print()

    print("✔ Activity started")
    print()

    print(f"Activity    {activity.title}")

    return 0


def cmd_close(project: Project) -> int:

    activity = project.current_activity()

    if activity is None:
        raise NoActiveActivity(
            "No active activity."
        )

    activity.finish()

    print()

    print("✔ Activity completed")
    print()

    print(f"Activity    {activity.title}")

    return 0


def main() -> int:

    parser = argparse.ArgumentParser()

    sub = parser.add_subparsers(dest="command")

    start = sub.add_parser("start")
    start.add_argument("title")

    sub.add_parser("status")

    sub.add_parser("close")

    args = parser.parse_args()

    project = Project.current()

    if args.command == "status":
        return cmd_status(project)

    if args.command == "start":
        return cmd_start(project, args.title)

    if args.command == "close":
        return cmd_close(project)

    parser.print_help()

    return 1


if __name__ == "__main__":

    try:

        raise SystemExit(main())

    except (
        ProjectNotInitialized,
        ActivityAlreadyRunning,
        NoActiveActivity,
    ) as exc:

        print()

        print(f"ERROR: {exc}")

        print()

        raise SystemExit(1)