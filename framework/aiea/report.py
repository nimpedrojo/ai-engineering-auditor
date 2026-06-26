from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path


def read_events(events_file: Path) -> list[dict]:
    events: list[dict] = []

    if not events_file.exists():
        return events

    for line_number, line in enumerate(
        events_file.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append(
                {
                    "eventId": f"INVALID-LINE-{line_number}",
                    "eventType": "InvalidEvent",
                    "title": f"Invalid JSON at line {line_number}",
                    "tool": "Unknown",
                    "phase": "Unknown",
                }
            )

    return events


def counter_section(title: str, counter: Counter) -> list[str]:
    lines = [f"## {title}", ""]

    if not counter:
        return lines + ["No data.", ""]

    lines += ["| Item | Count |", "|------|-------|"]

    for key, value in sorted(counter.items()):
        lines.append(f"| {key} | {value} |")

    return lines + [""]


def events_section(title: str, events: list[dict]) -> list[str]:
    lines = [f"## {title}", ""]

    if not events:
        return lines + ["No entries recorded.", ""]

    lines += ["| Event | Title | Tool | Phase |", "|-------|-------|------|-------|"]

    for event in events:
        lines.append(
            f"| {event.get('eventId', '')} | "
            f"{event.get('title', '')} | "
            f"{event.get('tool', '')} | "
            f"{event.get('phase', '')} |"
        )

    return lines + [""]


def generate_report(
    *,
    project: dict,
    state: dict,
    events: list[dict],
) -> str:
    event_types = Counter(event.get("eventType", "Unknown") for event in events)
    tools = Counter(event.get("tool", "Unknown") for event in events)
    phases = Counter(event.get("phase", "Unknown") for event in events)

    ai_events = [event for event in events if event.get("eventType") == "AIInteraction"]
    findings = [event for event in events if event.get("eventType") == "Finding"]
    decisions = [event for event in events if event.get("eventType") == "Decision"]
    risks = [event for event in events if event.get("eventType") == "Risk"]
    issues = [event for event in events if event.get("eventType") == "Issue"]
    milestones = [event for event in events if event.get("eventType") == "Milestone"]

    ai_by_tool = Counter(event.get("tool", "Unknown") for event in ai_events)
    ai_by_result = Counter(event.get("result", "Unknown") for event in ai_events)

    accepted_ai = sum(1 for event in ai_events if event.get("accepted") is True)
    rejected_ai = sum(1 for event in ai_events if event.get("accepted") is False)

    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        "# AI Engineering Auditor Report",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"- Project: **{project.get('name', 'Unknown')}**",
        f"- Status: **{state.get('status', 'Unknown')}**",
        f"- Current phase: **{state.get('currentPhase', 'Unknown')}**",
        f"- Total events: **{len(events)}**",
        f"- AI interactions: **{len(ai_events)}**",
        f"- Findings: **{len(findings)}**",
        f"- Decisions: **{len(decisions)}**",
        f"- Risks: **{len(risks)}**",
        f"- Issues: **{len(issues)}**",
        "",
        "This report is generated from recorded evidence in `docs/ai-auditor/events.jsonl`.",
        "",
        "---",
        "",
    ]

    lines += counter_section("Events by Type", event_types)
    lines += counter_section("Events by Tool", tools)
    lines += counter_section("Events by Phase", phases)
    lines += counter_section("AI Interactions by Tool", ai_by_tool)
    lines += counter_section("AI Interactions by Result", ai_by_result)

    lines += [
        "## AI Acceptance",
        "",
        f"- Accepted AI interactions: **{accepted_ai}**",
        f"- Rejected AI interactions: **{rejected_ai}**",
        "",
        "---",
        "",
    ]

    lines += events_section("Findings", findings)
    lines += events_section("Decisions", decisions)
    lines += events_section("Risks", risks)
    lines += events_section("Issues", issues)
    lines += events_section("Milestones", milestones)
    lines += events_section("AI Interactions", ai_events)

    lines += [
        "---",
        "",
        "## Notes",
        "",
        "- This is an evidence-based report.",
        "- Conclusions are limited to recorded events.",
        "- Missing evidence means the report cannot infer that activity.",
        "- Manual review is still required before using this as a formal project report.",
        "",
    ]

    return "\n".join(lines)