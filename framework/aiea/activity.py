from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime

from .context import ProjectContext
from .event import create_and_append
from .exceptions import AIEAError


class ActivityAlreadyRunning(AIEAError):
    """Raised when trying to start an activity while another is active."""


class NoActiveActivity(AIEAError):
    """Raised when trying to access or finish an activity when none is active."""


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(slots=True)
class Activity:
    context: ProjectContext
    title: str
    phase: str

    def finish(self) -> dict:
        if not self.context.state_file.exists():
            raise NoActiveActivity("No active activity found.")

        state = json.loads(self.context.state_file.read_text(encoding="utf-8"))

        if state.get("currentTask") is None:
            raise NoActiveActivity("No active activity found.")

        title = state["currentTask"]
        phase = state.get("currentPhase", "Discovery")
        now = utc_now()

        payload = {
            "eventType": "ActivityCompleted",
            "phase": phase,
            "tool": "Manual",
            "title": f"{title} completed",
            "description": "Engineering activity completed.",
        }

        event = create_and_append(
            events_file=self.context.events_file,
            payload=payload,
        )

        state["status"] = "Ready"
        state["currentTask"] = None
        state["currentAIInteraction"] = None
        state["updatedAt"] = now

        self.context.state_file.write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        return event