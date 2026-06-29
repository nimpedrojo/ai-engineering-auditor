from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from aiea.event import create_and_append


def error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def framework_root() -> Path:
    return Path(__file__).resolve().parents[2]


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


def validate_project(project_root: Path) -> None:
    if (project_root / ".git").exists():
        return

    markers = [
        "package.json",
        "pom.xml",
        "Cargo.toml",
    ]

    if any((project_root / marker).exists() for marker in markers):
        return

    if any(project_root.glob("*.sln")):
        return

    if (project_root / "src").exists():
        return

    error("Current directory does not appear to be a software project.")


def replace_placeholders(path: Path, values: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")

    for key, value in values.items():
        text = text.replace(key, value)

    path.write_text(text, encoding="utf-8")


def initialize_files(target_dir: Path, project_name: str) -> None:
    now = utc_now()

    values = {
        "__PROJECT_ID__": project_name,
        "__PROJECT_NAME__": project_name,
        "__REPOSITORY__": project_name,
        "__CREATED_AT__": now,
        "__UPDATED_AT__": now,
    }

    replace_placeholders(target_dir / "project.json", values)
    replace_placeholders(target_dir / "state.json", values)


def main() -> int:
    fw_root = framework_root()
    template_dir = fw_root / "templates" / "project-instance"

    if not template_dir.exists():
        error(f"Template directory not found: {template_dir}")

    project_root = find_project_root()
    project_name = project_root.name
    target_dir = project_root / "docs" / "ai-auditor"

    print()
    print("============================================================")
    print(" AI Engineering Auditor")
    print("============================================================")
    print()

    validate_project(project_root)

    if target_dir.exists():
        error("AI Engineering Auditor already initialized.")

    target_dir.mkdir(parents=True, exist_ok=True)

    for item in template_dir.iterdir():
        destination = target_dir / item.name

        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)

    initialize_files(target_dir, project_name)

    create_and_append(
        events_file=target_dir / "events.jsonl",
        payload={
            "eventType": "ProjectInitialized",
            "phase": "Discovery",
            "tool": "aiea-init",
            "title": "AI Engineering Auditor initialized",
            "description": "The project has been initialized successfully.",
        },
    )

    print("✔ AI Engineering Auditor initialized")
    print()
    print(f"Project   {project_name}")
    print(f"Location  {target_dir}")
    print("Status    Ready")
    print()
    print("Next step")
    print("---------")
    print("Run:")
    print()
    print("  aiea-status")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())