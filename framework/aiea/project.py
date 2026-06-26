from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime

from .activity import Activity, ActivityAlreadyRunning
from .context import ProjectContext, load_context
from .event import create_and_append
from .exceptions import ProjectNotInitialized


@dataclass(slots=True)
class ProjectStatus:
    status: str
    current_phase: str
    current_activity: str | None
    total_events: int


class Project:

    def __init__(self, context: ProjectContext):

        self.context = context

    @classmethod
    def current(cls) -> "Project":

        return cls(load_context())

    def status(self) -> ProjectStatus:

        if not self.context.state_file.exists():
            raise ProjectNotInitialized(
                "AI Engineering Auditor is not initialized in this project. Run: aiea-init"
            )

        state = json.loads(
            self.context.state_file.read_text(
                encoding="utf-8"
            )
        )

        total_events = 0

        if self.context.events_file.exists():

            with self.context.events_file.open(
                encoding="utf-8"
            ) as file:

                total_events = sum(
                    1
                    for line in file
                    if line.strip()
                )

        return ProjectStatus(

            status=state["status"],

            current_phase=state["currentPhase"],

            current_activity=state.get("currentTask"),

            total_events=total_events,

        )

    def start_activity(
        self,
        title: str,
        phase: str | None = None,
    ) -> Activity:

        if not self.context.state_file.exists():
            raise ProjectNotInitialized(
                "AI Engineering Auditor is not initialized in this project. Run: aiea-init"
            )

        state = json.loads(
            self.context.state_file.read_text(
                encoding="utf-8"
            )
        )

        if state.get("currentTask") is not None:
            raise ActivityAlreadyRunning(
                f"Activity already running: {state['currentTask']}"
            )

        current_phase = phase or state.get(
            "currentPhase",
            "Discovery",
        )

        now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

        state["status"] = "TaskActive"
        state["currentPhase"] = current_phase
        state["currentTask"] = title
        state["currentAIInteraction"] = None
        state["updatedAt"] = now

        self.context.state_file.write_text(
            json.dumps(
                state,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        create_and_append(
            events_file=self.context.events_file,
            payload={
                "eventType": "ActivityStarted",
                "phase": current_phase,
                "tool": "Manual",
                "title": title,
                "description": "Engineering activity started.",
            },
        )

        return Activity(
            context=self.context,
            title=title,
            phase=current_phase,
        )

    def current_activity(self) -> Activity | None:

        if not self.context.state_file.exists():
            raise ProjectNotInitialized(
                "AI Engineering Auditor is not initialized in this project. Run: aiea-init"
            )

        state = json.loads(
            self.context.state_file.read_text(
                encoding="utf-8"
            )
        )

        title = state.get("currentTask")

        if title is None:
            return None

        return Activity(
            context=self.context,
            title=title,
            phase=state.get(
                "currentPhase",
                "Discovery",
            ),
        )