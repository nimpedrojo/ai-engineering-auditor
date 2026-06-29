# Rule Engine

## Purpose

The Rule Engine converts Observations into Engineering Actions.

Rules never modify the Core directly.

Rules evaluate observations and return actions.

The Observer executes those actions.

---

# Flow

```text
Observation

↓

Rule

↓

Engineering Action

↓

Core API
```

---

# Rule Interface

Every rule exposes two operations.

```python
matches(observation) -> bool

process(observation) -> list[EngineeringAction]
```

---

# EngineeringAction

Actions describe what should happen.

Examples:

- CreateEvent
- UpdateActivity
- Ignore

Actions contain no execution logic.

---

# Observer

The Observer:

1. Receives an Observation.
2. Finds matching rules.
3. Collects Engineering Actions.
4. Executes them through the Core API.

---

# First Rule

FileSavedRule

Input:

```text
type = file.saved
```

Output:

```text
CreateEvent(
    eventType="FileChanged"
)
```

---

# Future Rules

- CopilotAcceptedRule
- CodexResponseRule
- GitCommitRule
- TerminalCommandRule
- TestExecutedRule
