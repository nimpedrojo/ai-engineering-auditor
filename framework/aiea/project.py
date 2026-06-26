from __future__ import annotations
from .exceptions import ProjectNotInitialized

import json
from dataclasses import dataclass
from pathlib import Path

from .context import ProjectContext, load_context


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