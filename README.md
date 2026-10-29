# LogicaSophia

Independent, standalone Linux agentic AI engineering system by I2PS Engineering.

## v0.3.0 — First connected agent

LogicaSophia connects a replaceable localhost foundation model to our original evidence-governed execution controller. It can independently select bounded read/search operations in a workspace, inspect real files and produce an answer. The host validates every tool request, checks source evidence integrity and records an audit trail. It has **no access to arbitrary shell commands or system writes**.

This is original orchestration software. OpenClaw and Claw Code are **architectural references**, not copied source or foundation models. No weights were obtained from the Claude Code source leak.

## First run on Ubuntu (one USB text file)

Download `LogicaSophia_Start_AI.txt`, transfer it to your Linux machine and execute:

```bash
bash LogicaSophia_Start_AI.txt
```

Internet is required on first run. The launcher builds llama.cpp as a replaceable local inference backend and downloads an *experimental* small open-weight model to prove an end-to-end loop on the i5 test host. It runs the tests and the mock-model integration smoke check before opening an interactive prompt.

## Direct CLI (if you already have a local model server)

```bash
PYTHONPATH=src python3 -m logicasophia agent \
  --goal 'Explain hello.py' --workspace fixtures/project_fixture \
  --backend-url http://127.0.0.1:8090
```

Model discovery is automatic. You may use a different local inference runtime/model; there is no hardcoded Qwen dependency. Model interactions are limited by the selected model's ability to emit valid structured JSON.

## Verify and diagnose

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/m2_smoke.py
python3 scripts/m3_smoke.py
```

Each run records `outcome.json`, `trace.jsonl`, and `events.sqlite3`. An `ACCEPTED` read-only run means evidence files remained unchanged, **not** that the model's interpretation has been fact-checked.

Other existing commands are unchanged: `logicasophia inventory`, `logicasophia serve` and `python3 scripts/qualify_linux.py`.

See `docs/MILESTONE_03.md` for implementation details, limits and privacy controls.

**Licensing:** the LogicaSophia project has not yet selected its distribution license. The optional external inference runtime/model have separate licenses; respect their notices.
