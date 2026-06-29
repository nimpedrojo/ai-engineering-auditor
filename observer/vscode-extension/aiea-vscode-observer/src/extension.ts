import * as vscode from "vscode";
import * as fs from "fs";
import * as path from "path";

function workspaceRoot(): string | undefined {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
}

function eventsFile(root: string): string {
  return path.join(root, "docs", "ai-auditor", "events.jsonl");
}

function nextEventId(file: string): string {
  if (!fs.existsSync(file)) {
    return "EVT-000001";
  }

  const count = fs
    .readFileSync(file, "utf8")
    .split(/\r?\n/)
    .filter((line: string) => line.trim().length > 0).length;

  return `EVT-${String(count + 1).padStart(6, "0")}`;
}

function utcNow(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function appendFileChangedEvent(
  root: string,
  savedFile: string,
  languageId: string,
): void {
  const file = eventsFile(root);

  if (!fs.existsSync(file)) {
    return;
  }

  const relative = path.relative(root, savedFile);

  if (relative.startsWith(path.join("docs", "ai-auditor"))) {
    return;
  }

  const event = {
    eventId: nextEventId(file),
    timestamp: utcNow(),
    schemaVersion: "1.0.0",
    eventType: "FileChanged",
    phase: "Discovery",
    tool: "VSCode",
    title: `File saved: ${relative}`,
    description: "A file was saved in VS Code.",
    metadata: {
      file: relative,
      languageId,
    },
  };

  fs.appendFileSync(file, JSON.stringify(event) + "\n", "utf8");
}

export function activate(context: vscode.ExtensionContext) {
  const root = workspaceRoot();

  if (!root) {
    return;
  }

  if (!fs.existsSync(eventsFile(root))) {
    vscode.window.showInformationMessage("AIEA Observer: run aiea-init first.");
    return;
  }

  vscode.window.showInformationMessage("AIEA Observer active.");

  const disposable = vscode.workspace.onDidSaveTextDocument((document) => {
    if (document.uri.scheme !== "file") {
      return;
    }

    appendFileChangedEvent(root, document.uri.fsPath, document.languageId);
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
