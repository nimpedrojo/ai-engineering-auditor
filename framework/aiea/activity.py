from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

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

    def record(
        self,
        *,
        event_type: str,
        title: str,
        tool: str = "Manual",
        description: str = "",
        severity: str | None = None,
        purpose: str | None = None,
        result: str | None = None,
        accepted: bool | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "eventType": event_type,
            "phase": self.phase,
            "tool": tool,
            "title": title,
            "description": description,
        }

        if severity is not None:
            payload["severity"] = severity

        if purpose is not None:
            payload["purpose"] = purpose

        if result is not None:
            payload["result"] = result

        if accepted is not None:
            payload["accepted"] = accepted

        if metadata is not None:
            payload["metadata"] = metadata

        return create_and_append(
            events_file=self.context.events_file,
            payload=payload,
        )

    def add_finding(
        self,
        title: str,
        *,
        tool: str = "Manual",
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="Finding",
            title=title,
            tool=tool,
            description=description,
            metadata=metadata,
        )

    def add_decision(
        self,
        title: str,
        *,
        tool: str = "Manual",
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="Decision",
            title=title,
            tool=tool,
            description=description,
            metadata=metadata,
        )

    def add_issue(
        self,
        title: str,
        *,
        tool: str = "Manual",
        description: str = "",
        severity: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="Issue",
            title=title,
            tool=tool,
            description=description,
            severity=severity,
            metadata=metadata,
        )

    def add_risk(
        self,
        title: str,
        *,
        tool: str = "Manual",
        description: str = "",
        severity: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="Risk",
            title=title,
            tool=tool,
            description=description,
            severity=severity,
            metadata=metadata,
        )

    def add_milestone(
        self,
        title: str,
        *,
        tool: str = "Manual",
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="Milestone",
            title=title,
            tool=tool,
            description=description,
            metadata=metadata,
        )

    def add_ai_interaction(
        self,
        title: str,
        *,
        tool: str,
        purpose: str,
        result: str,
        accepted: bool | None = None,
        description: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.record(
            event_type="AIInteraction",
            title=title,
            tool=tool,
            description=description,
            purpose=purpose,
            result=result,
            accepted=accepted,
            metadata=metadata,
        )

    def finish(self) -> dict[str, Any]:
        if not self.context.state_file.exists():
            raise NoActiveActivity("No active activity found.")

        state = json.loads(self.context.state_file.read_text(encoding="utf-8"))

        if state.get("currentTask") is None:
            raise NoActiveActivity("No active activity found.")

        title = state["currentTask"]
        phase = state.get("currentPhase", "Discovery")
        now = utc_now()

        event = create_and_append(
            events_file=self.context.events_file,
            payload={
                "eventType": "ActivityCompleted",
                "phase": phase,
                "tool": "Manual",
                "title": f"{title} completed",
                "description": "Engineering activity completed.",
            },
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