# AIEA Observer

The Observer captures engineering activity automatically and converts it into AIEA events.

The Observer is not the Core.

The Core records evidence.

The Observer detects activity.

## Responsibilities

- Detect engineering activity.
- Normalize observations.
- Send evidence to AIEA Core.
- Avoid interrupting the developer.

## Non responsibilities

- It does not generate reports.
- It does not own the domain model.
- It does not replace the CLI.
- It does not store evidence directly.

## Architecture

Observer Core receives observations.

Adapters detect activity from tools.

Initial adapters:

- VS Code
- Git
- Terminal
- Copilot
- Codex

## First milestone

Detect a saved file in VS Code and register a `FileChanged` event through AIEA Core.
