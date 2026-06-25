#!/bin/bash

set -e

AUDITOR_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEMPLATE_DIR="$AUDITOR_ROOT/framework/templates/project-instance"
TARGET_DIR="docs/ai-auditor"

echo "Initializing AI Engineering Auditor..."

if [ -d "$TARGET_DIR" ]; then
  echo "AI Engineering Auditor already exists at $TARGET_DIR"
  exit 0
fi

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Template directory not found: $TEMPLATE_DIR"
  exit 1
fi

mkdir -p "$TARGET_DIR"
cp -R "$TEMPLATE_DIR"/. "$TARGET_DIR"/

NOW="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
REPO_NAME="$(basename "$(pwd)")"

# Simple placeholder replacement
sed -i.bak "s/\"createdAt\": \"\"/\"createdAt\": \"$NOW\"/" "$TARGET_DIR/project.json"
sed -i.bak "s/\"updatedAt\": \"\"/\"updatedAt\": \"$NOW\"/" "$TARGET_DIR/state.json"
sed -i.bak "s/\"name\": \"\"/\"name\": \"$REPO_NAME\"/" "$TARGET_DIR/project.json"
sed -i.bak "s/\"projectId\": \"\"/\"projectId\": \"$REPO_NAME\"/" "$TARGET_DIR/project.json"
sed -i.bak "s/\"repository\": \"\"/\"repository\": \"$REPO_NAME\"/" "$TARGET_DIR/project.json"

rm "$TARGET_DIR"/*.bak 2>/dev/null || true

echo "AI Engineering Auditor initialized at $TARGET_DIR"