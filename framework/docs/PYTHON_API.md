# AI Engineering Auditor

# Python API v1.0

---

# Design Principles

The Python API is the canonical interface of AI Engineering Auditor.

All clients use this API:

- CLI
- MCP Server
- VS Code Extension
- Tests
- Future REST API

The API must expose engineering concepts.

It must never expose implementation details such as JSON files.

---

# Entry Point

```python
from aiea import Project

project = Project.current()
```

There is always one current project.

---

# Project

Represents the current engineering project.

## Factory

```python
Project.current()
```

Returns the current project.

Raises an exception if the project is not initialized.

---

## Initialization

```python
Project.initialize()
```

Creates the AI Engineering Auditor structure.

Equivalent to:

```text
aiea-init
```

---

## Status

```python
project.status()
```

Returns

```python
ProjectStatus
```

Example

```python
status.current_phase
status.current_activity
status.total_events
```

---

## Activities

Start

```python
activity = project.start_activity(
    title="Analyze Realm persistence",
    phase="Discovery"
)
```

Current

```python
activity = project.current_activity()
```

Finish

```python
activity.finish()
```

Cancel

```python
activity.cancel()
```

List

```python
project.activities()
```

---

# EngineeringActivity

Represents one engineering activity.

Properties

```python
activity.id
activity.title
activity.phase
activity.status
activity.started_at
activity.finished_at
```

---

# Engineering Events

Generic event

```python
activity.add_event(...)
```

Convenience helpers

```python
activity.add_finding(...)

activity.add_decision(...)

activity.add_issue(...)

activity.add_risk(...)

activity.add_milestone(...)
```

---

# AI

Register AI interaction

```python
activity.add_ai_interaction(
    tool="Copilot",
    purpose="Implementation",
    accepted=True,
    result="Accepted"
)
```

Possible tools

- Copilot
- Codex
- ChatGPT
- Manual

---

# Engineering Evidence

Register evidence

```python
activity.add_evidence(
    type="Commit",
    reference="7f9d12c"
)
```

Examples

- Commit

- Pull Request

- File

- Screenshot

- Benchmark

- Test Result

---

# Metrics

Current metrics

```python
metrics = project.metrics()
```

Examples

```python
metrics.total_events

metrics.ai_interactions

metrics.activities

metrics.findings

metrics.decisions

metrics.risks

metrics.issues
```

---

# Reports

Generate

```python
project.generate_report()
```

Returns

```python
Report
```

---

# Validation

```python
project.validate()
```

Checks

- schema

- events

- consistency

- activities

Returns

```python
ValidationResult
```

---

# Export

Markdown

```python
project.export_markdown()
```

JSON

```python
project.export_json()
```

Future

PDF

HTML

Dashboard

---

# Exceptions

```python
ProjectNotInitialized

NoActiveActivity

ActivityAlreadyRunning

InvalidEvent

ValidationError
```

---

# Internal Rule

Public API must never expose:

- events.jsonl

- state.json

- project.json

- metrics.json

- report.md

These are implementation details.

---

# Golden Rule

The API speaks the language of engineering.

The storage layer speaks the language of files.
