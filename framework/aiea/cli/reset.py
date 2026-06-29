from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


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


def main() -> int:
    project_root = find_project_root()
    auditor_dir = project_root / "docs" / "ai-auditor"

    print()
    print("============================================================")
    print(" AI Engineering Auditor")
    print("============================================================")
    print()

    if not auditor_dir.exists():
        error("AI Engineering Auditor is not initialized in this project.")

    print("This will remove:")
    print()
    print(auditor_dir)
    print()
    answer = input("Continue? Type YES: ")

    if answer != "YES":
        error("Reset cancelled.")

    shutil.rmtree(auditor_dir)

    print("✔ AI Engineering Auditor reset completed.")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())