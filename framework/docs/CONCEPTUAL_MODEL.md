# AI Engineering Auditor — Conceptual Model v1.0

## Purpose

AI Engineering Auditor captures evidence about software engineering work and evaluates how AI contributes to that work.

The system does not audit AI in isolation.

It audits engineering activity and measures AI contribution inside that activity.

---

## Core Concept

The central unit is:

```text
Engineering Activity
```

An Engineering Activity represents a meaningful piece of software engineering work.

Examples:

- Analyze legacy persistence
- Design migration strategy
- Implement repository layer
- Refactor authentication flow
- Review generated tests
- Investigate production bug
- Validate migrated data

---

## Domain Model

```text
Project
│
├── Engineering Activity
│   │
│   ├── Events
│   ├── Evidence
│   ├── AI Interactions
│   ├── Human Decisions
│   ├── Artifacts
│   ├── Outcomes
│   └── Metrics Observations
│
└── Reports
```

---

## Project

A Project is the software initiative being audited.

Examples:

- Mac to .NET migration
- API development
- Legacy refactor
- Testing improvement initiative

A Project contains multiple Engineering Activities.

---

## Engineering Activity

An Engineering Activity is the main unit of audit.

It answers:

```text
What engineering work was performed?
```

Each activity should have:

- id
- title
- phase
- objective
- status
- start time
- end time
- related events
- related evidence
- related AI interactions
- outcome

---

## Event

An Event is a recorded fact that happened during an Engineering Activity.

Events are append-only.

Events must not be edited manually.

Examples:

- ActivityStarted
- ActivityCompleted
- AIInteraction
- Finding
- Decision
- Risk
- Issue
- CommitCreated
- TestExecuted
- MilestoneReached

---

## Evidence

Evidence is any observable artifact supporting a conclusion.

Examples:

- source file
- commit
- pull request
- test result
- documentation
- terminal output
- benchmark
- review note

Reports must be based on evidence.

No evidence means no strong conclusion.

---

## AI Interaction

An AI Interaction records meaningful AI contribution during an Engineering Activity.

It captures:

- tool used
- purpose
- result
- accepted / modified / rejected
- human correction required
- risk introduced
- evidence reference

Examples of tools:

- GitHub Copilot
- Codex
- ChatGPT
- Manual baseline

---

## Human Decision

A Human Decision records an engineering choice.

Examples:

- choose SQL Server instead of Realm
- preserve legacy behavior
- reject AI-generated design
- delay optimization
- add characterization tests before migration

Decisions may be supported by AI, but they remain human decisions.

---

## Artifact

An Artifact is a produced or modified project asset.

Examples:

- code file
- test file
- documentation file
- diagram
- migration script
- report

---

## Outcome

An Outcome describes the result of an Engineering Activity.

Examples:

- task completed
- issue clarified
- risk identified
- implementation accepted
- tests added
- migration decision documented
- AI suggestion rejected

---

## Metrics Observation

A Metrics Observation is raw measurable data.

Examples:

- estimated time
- actual time
- review time
- number of AI iterations
- accepted percentage
- modified percentage
- rejected percentage
- files changed
- tests executed

Metrics Observations are not conclusions.

They are inputs for reports and metrics.

---

## Report

A Report is a generated interpretation of recorded evidence.

Reports answer:

- what work was done
- where AI contributed
- where AI failed
- what risks appeared
- what decisions were made
- what evidence supports the conclusions

Reports are derived artifacts.

They are not the source of truth.

---

## Source of Truth Hierarchy

```text
Evidence
↓
Events
↓
Metrics Observations
↓
Reports
```

Reports must never override evidence.

---

## v1.0 Rule

For v1.0, every relevant event should be linked to an Engineering Activity whenever possible.

If an activity is unknown, the event may still be recorded, but it should be marked as unassigned.

---

## Golden Rule

The Auditor does not try to prove that AI is useful.

It records engineering evidence so that usefulness can be evaluated honestly.
