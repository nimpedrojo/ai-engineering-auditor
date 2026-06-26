# AI Engineering Auditor

# Architecture v1.0

---

# Vision

AI Engineering Auditor is not a CLI.

It is not an MCP server.

It is not a VS Code extension.

Those are clients.

AI Engineering Auditor is an engineering platform.

Its purpose is to capture engineering evidence, evaluate AI contribution and generate objective engineering reports.

---

# Architecture Overview

```
                    +-------------------------+
                    |      VS Code Extension  |
                    +-------------------------+

                    +-------------------------+
                    |      GitHub Copilot     |
                    +-------------------------+

                    +-------------------------+
                    |          Codex          |
                    +-------------------------+

                    +-------------------------+
                    |           MCP           |
                    +-------------------------+

                    +-------------------------+
                    |            CLI          |
                    +-------------------------+

                               │
                               ▼

                 ===============================
                 AIEA PUBLIC PYTHON API
                 ===============================

                 Project
                 Activity
                 Event
                 Evidence
                 Metrics
                 Report

                               │
                               ▼

                 ===============================
                    DOMAIN SERVICES
                 ===============================

                 project.py
                 activity.py
                 event.py
                 report.py
                 metrics.py
                 state.py
                 validation.py

                               │
                               ▼

                 ===============================
                      STORAGE LAYER
                 ===============================

                 project.json
                 state.json
                 events.jsonl
                 metrics.json
                 report.md
```

---

# Architectural Principles

## 1. Single Domain

Every client must use the same engineering model.

There is only one Project model.

There is only one Activity model.

There is only one Event model.

---

## 2. Python First

Business logic lives only in Python.

Bash is only a launcher.

MCP is only an adapter.

VS Code Extension is only a client.

---

## 3. Storage Independence

The domain never depends on JSON.

Today:

```
events.jsonl
```

Tomorrow:

```
SQLite
PostgreSQL
Azure SQL
Cloud Storage
```

The API must not change.

---

## 4. Append Only

Engineering evidence is immutable.

Events are never edited.

Reports are regenerated.

---

## 5. Evidence Before Conclusions

Everything starts from evidence.

```
Evidence
    ↓
Events
    ↓
Activities
    ↓
Metrics
    ↓
Reports
```

Reports never create evidence.

---

# Layer Responsibilities

## Clients

Responsible for user interaction.

Examples

CLI

VS Code

Copilot

Codex

MCP

REST API

Never contain engineering logic.

---

## Public API

The official interface.

Everything must be possible through the API.

Examples

```
Project.current()

project.start_activity()

activity.add_finding()

activity.finish()

project.generate_report()
```

---

## Domain

Contains engineering rules.

Examples

Activity lifecycle

Validation

Metrics

AI contribution

Evidence relationships

No UI code.

No terminal code.

No filesystem assumptions.

---

## Storage

Responsible only for persistence.

Current implementation

JSON

Future implementations

SQLite

Cloud

Git

Database

The rest of the system must not notice.

---

# Supported Clients

## CLI

Developer terminal.

---

## GitHub Copilot

Engineering assistant.

---

## Codex

Engineering assistant.

---

## MCP

Tool provider.

---

## VS Code Extension

Automatic evidence collection.

Background observations.

Workspace integration.

---

## REST API

Future.

---

# Event Flow

```
Developer

↓

Copilot / Codex

↓

AIEA API

↓

Activity

↓

Event

↓

Evidence

↓

Storage

↓

Metrics

↓

Report
```

---

# Responsibilities Matrix

| Component         | Responsibility        |
| ----------------- | --------------------- |
| CLI               | Execute commands      |
| MCP               | Expose tools          |
| VS Code Extension | Observe IDE           |
| Copilot           | Engineering reasoning |
| Codex             | Engineering reasoning |
| Python API        | Domain                |
| Storage           | Persistence           |

---

# Non Goals

The platform does not replace Git.

The platform does not replace Jira.

The platform does not replace Azure DevOps.

The platform complements engineering work.

---

# Long-Term Vision

The Auditor becomes the engineering memory of the project.

Every engineering activity leaves objective evidence.

Reports become a consequence of engineering work instead of an additional task.

The platform should be able to answer questions such as:

- Where did AI contribute most?

- Which decisions were AI-assisted?

- Which risks appeared after AI-generated code?

- Which engineering activities required the most human intervention?

- How did engineering productivity evolve over time?

without relying on memory or subjective opinions.

---

# Final Principle

The platform should disappear during engineering work.

The developer should feel assisted, not audited.
