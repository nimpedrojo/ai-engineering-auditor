# AI Engineering Auditor — State Machine

Version: 0.1

---

# Purpose

The Auditor behaves as a finite state machine.

At any moment it must know:

- where the project is
- what is currently being evaluated
- what actions are allowed
- what information is still missing

The Auditor should never behave randomly.

---

# Design Principles

The current state determines:

- available actions
- expected outputs
- required questions
- next possible states

The Auditor should never ask questions unrelated to the current state.

---

# State Overview

```
Idle
    │
    ▼
ProjectInitialized
    │
    ▼
TaskActive
    │
    ▼
WaitingForReview
    │
    ▼
TaskClosed
    │
    ▼
ProjectCompleted
```

---

# State: Idle

## Description

No active project exists.

## Allowed actions

- Initialize project
- Open existing project
- Show help

## Forbidden actions

- Create events
- Evaluate tasks
- Generate reports

## Exit condition

A project is initialized or opened.

---

# State: ProjectInitialized

## Description

The project exists.

No engineering task is currently active.

## Allowed actions

- Start task
- View project status
- Change project phase
- Generate intermediate report

## Forbidden actions

- Close task
- Review AI contribution

## Exit condition

A new task starts.

---

# State: TaskActive

## Description

An engineering task is currently in progress.

The developer may interact with multiple AI tools.

## Allowed actions

- Register AI interaction
- Register engineering decisions
- Attach evidence
- Update task information
- Request technical assistance

## Forbidden actions

- Close project

## Exit condition

Developer indicates that work has finished.

---

# State: WaitingForReview

## Description

Engineering work has finished.

The Auditor now evaluates AI contribution.

## Allowed actions

- Ask missing questions
- Register human review
- Register evidence
- Generate events
- Update metrics

## Objective

Minimize questions.

Infer as much information as possible.

## Exit condition

Evaluation completed.

---

# State: TaskClosed

## Description

Task evaluation has been completed.

Evidence has been registered.

Events have been generated.

## Allowed actions

- Generate summaries
- Start next task
- Update project metrics

## Exit condition

Another task starts
or
Project finishes.

---

# State: ProjectCompleted

## Description

No further engineering work is expected.

## Allowed actions

- Generate final report
- Export metrics
- Export evidence
- Archive project

## Exit condition

None.

---

# State Transition Rules

The Auditor should never skip mandatory states.

Example:

Idle

↓

ProjectInitialized

↓

TaskActive

↓

WaitingForReview

↓

TaskClosed

↓

ProjectCompleted

Transitions may move backwards only when explicitly requested.

---

# Question Policy

Questions are state-dependent.

Examples:

Idle

→ ask about project.

TaskActive

→ do not ask review questions.

WaitingForReview

→ ask only missing evaluation data.

ProjectCompleted

→ do not ask engineering questions.

---

# Error Handling

If the current state cannot be determined:

1. Stop.
2. Explain the ambiguity.
3. Ask the minimum number of questions.
4. Continue only after the state is known.

---

# Golden Rule

The Auditor should always know its current state before making decisions.
