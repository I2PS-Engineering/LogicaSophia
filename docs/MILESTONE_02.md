# Milestone 2 — Evidence-Governed Execution, Phase A

Status: first independently authored deterministic prototype. No LLM, no inference, no automated patching, no shell execution.

## What is implemented

- Strict v1 task contract with at most eight steps and eight independent file-content checks.
- Deny-by-default policy allowing only `read_file` and `search_files` if the task separately grants the tool.
- Path boundary validation, no-follow file opens, maximum 64 KiB per file, and bounded search.
- State machine with explicit terminal ACCEPTED / FAILED / UNCERTAIN outcomes.
- Independent verifier reopens each observed file and checks content + digest consistency.
- JSONL event hash chain, SQLite event archive and offline replay.
- Read-only fixture task, tests and a one-command Linux script.

## Run from the repository root

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/m2_smoke.py
```

The smoke command creates `results/<trace_id>/outcome.json`, `trace.jsonl`, and `events.sqlite3` and immediately replays the trace without running tools again.

## Limits and security boundary

This is **not** an OS-level sandbox or a secure multiuser service. It performs no shell execution, patch application, network requests, dependency installation or writes to the inspected workspace. CLI explicitly writes only the local results directory. The process runs with its invoker's ordinary filesystem read privileges. Inference, autonomous planning, advanced memory, approval workflows, replay-based resumption and controlled code editing remain future stages. The hash chain detects accidental/casual tampering but does not authenticate against an attacker who can rewrite the complete result directory.

## Acceptance

- Pass all core tests for acceptance, denial, missing evidence, file mutation, traversal, symlinks and trace corruption.
- A real Linux machine can execute the fixture and create trace + outcome.
- No inference performance or claimed autonomous intelligence is inferred from these tests.
