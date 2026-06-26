# Technical Debt

## TD-001 — Centralize state access

Repeated logic exists in `framework/aiea/project.py` for:

- checking whether `state.json` exists
- loading state from JSON
- writing state back to disk

This should be refactored into a dedicated state abstraction after the first functional version is complete.

Status: Deferred until v1 functional MVP.
