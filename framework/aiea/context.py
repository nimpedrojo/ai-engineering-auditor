from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass(slots=True)
class ProjectContext:

    project_root: Path
    auditor_dir: Path

    project_file: Path
    state_file: Path
    events_file: Path
    metrics_file: Path
    report_file: Path


def find_project_root() -> Path:

    try:

        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )

        return Path(result.stdout.strip())

    except Exception:

        return Path.cwd()


def load_context() -> ProjectContext:

    project_root = find_project_root()

    auditor = project_root / "docs" / "ai-auditor"

    return ProjectContext(

        project_root=project_root,

        auditor_dir=auditor,

        project_file=auditor / "project.json",

        state_file=auditor / "state.json",

        events_file=auditor / "events.jsonl",

        metrics_file=auditor / "metrics.json",

        report_file=auditor / "report.md",

    )