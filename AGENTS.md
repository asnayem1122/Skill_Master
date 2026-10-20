# Skill Master — Agent Guidelines & Execution Guardrails

This repository is the single source of truth for 70+ modular AI agent skills linked globally to Google Antigravity via an NTFS Directory Junction (`~/.gemini/config/skills`).

---

## 📜 Core Governance Commandments

1. **Never Duplicate Skills**: Merge overlapping capabilities into existing master skills rather than creating splinter directories (e.g. Impeccable $\to$ `frontend-design`, Karpathy $\to$ `ponytail`).
2. **Positive Updates Only**: Every modification must add value (sharper triggers, deeper checklists, structural remedies). Never degrade or bloat existing skills.
3. **Tracking Ledger Synchronization**: Every skill modification or addition must be logged in [`Catalog.md`](Catalog.md) and [`README.md`](README.md).
4. **Validation Gate**: All skills must pass validation via `node skills-cli.js installed` with `[OK] SKILL.md`.

---

## ⚙️ Windows CLI & Subprocess Execution Guardrails

When executing terminal commands in Windows environments (PowerShell / Antigravity subprocesses):

### 1. Mandatory Non-Interactive Flags (`--yes` / `-y`)
- Never run bare `npx`, `pnpm dlx`, or `bunx` that can trigger interactive installation prompts (`Need to install ... (y/n)`).
- Subprocesses lack an interactive TTY; the process will hang indefinitely waiting for standard input.
- **Always specify**:
  ```powershell
  npx --yes tsx <target>
  pnpm dlx --yes <target>
  ```

### 2. The Scratch Script Pattern (No Complex `-e "..."` One-Liners)
- On Windows, PowerShell parses quotes, semicolons (`;`), and curly braces (`{ ... }`) differently than POSIX shells.
- Passing multi-line or import-heavy TypeScript/JavaScript via inline `-e " import { ... } ... "` strings causes silent failures, quote mangling, or infinite stdin loops.
- **The Golden Rule**: Write a temporary scratch script file (e.g. in `scratch/test.ts` or `.tmp_test.ts`) and execute it cleanly:
  ```powershell
  npx --yes tsx .tmp_test.ts
  ```
- Remove the temporary file when execution finishes.

### 3. Active Background Task Lifecycle & Triage
- If a command drops into the background and reports `Empty log` or hangs:
  1. Call `manage_task(Action: "status", TaskId: "<id>")` to inspect real-time logs.
  2. If the task is frozen waiting for stdin or locked in a quote loop, **kill it immediately**:
     ```json
     manage_task({"Action": "kill", "TaskId": "<id>"})
     ```
  3. Never leave orphaned zombie tasks running in the workspace holding file locks or ports.
- Use realistic `WaitMsBeforeAsync` durations (8000–10000 ms) for commands that compile, bundle, or run tests so they execute synchronously.
