from __future__ import annotations

from aiea import Project
from aiea.exceptions import ProjectNotInitialized


def main() -> int:
    project = Project.current()
    status = project.status()

    print()
    print("AI Engineering Auditor")
    print("----------------------")
    print(f"Status            {status.status}")
    print(f"Phase             {status.current_phase}")
    print(f"Current Activity  {status.current_activity or 'None'}")
    print(f"Events            {status.total_events}")
    print()

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProjectNotInitialized as exc:
        print()
        print(f"ERROR: {exc}")
        print()
        raise SystemExit(1)