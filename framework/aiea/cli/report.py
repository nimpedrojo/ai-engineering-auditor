from __future__ import annotations

import json

from aiea import Project
from aiea.exceptions import ProjectNotInitialized
from aiea.report import generate_report, read_events


def main() -> int:
    project = Project.current()

    if not project.context.project_file.exists():
        raise ProjectNotInitialized(
            "AI Engineering Auditor is not initialized in this project. Run: aiea-init"
        )

    project_data = json.loads(project.context.project_file.read_text(encoding="utf-8"))
    state_data = json.loads(project.context.state_file.read_text(encoding="utf-8"))
    events = read_events(project.context.events_file)

    report = generate_report(
        project=project_data,
        state=state_data,
        events=events,
    )

    project.context.report_file.write_text(report, encoding="utf-8")

    print()
    print("✔ Report generated")
    print()
    print(f"Report    {project.context.report_file}")
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