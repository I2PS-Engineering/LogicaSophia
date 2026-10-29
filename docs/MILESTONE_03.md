# LogicaSophia — Connected Local AI Agent (v0.3.0)

## Goal

One standalone Linux application with a replaceable local foundation model, bounded model-directed file inspection, deny-by-default policy checks, source-evidence revalidation, and durable audit trails. No Atlas Nexus integration or reused code from Claude Code/OpenClaw.

## Implementation

- `logicasophia agent --goal 'Explain hello.py' --workspace fixtures/project_fixture --backend-url http://127.0.0.1:8090` connects to a running local OpenAI-compatible inference server.
- The agent automatically discovers the local model identifier via `/v1/models`.
- A model selects JSON actions (`read_file`, `search_files`, `final`) in a bounded loop. The host validates the actions before execution.
- Workspace reads reject symlink traversal, unsupported paths, large files, and binary content. Shell, edits, installations, and network tools are **not exposed** to model calls.
- The host reopens observed files and checks their hashes after inference. `ACCEPTED` means *the read-only execution completed and cited source bytes were stable*, **not** that the model's interpretation is necessarily true.
- JSONL hash chain, SQLite event database, and outcome.json are written under `~/.local/share/logicasophia/results/<run-id>/` by default.

## First real Linux run

Copy `LogicaSophia_Start_AI.txt` to the Ubuntu machine and run `bash LogicaSophia_Start_AI.txt` from the folder containing it. The script installs missing compiler dependencies with Ubuntu apt, clones/fast-forwards the official LogicaSophia GitHub repo, runs local tests, builds llama.cpp as a replaceable model backend, downloads a **temporary experimental SmolLM2-1.7B-Instruct Q4_K_M** model, and launches an interactive task prompt. Internet is required for first build/model download. The script never downloads or executes the Claude Code leak or a bundled OpenClaw app.

The default model is a small locally hosted research baseline selected to fit the measured 7.1 GiB RAM of the i5-6500T. It is **not** a permanent model decision or claimed LogicaSophia intellectual property. Model selection is replaceable with `LOGICASOPHIA_MODEL_HF` or by pointing `--backend-url` at an independently running OpenAI-compatible local model server.

## Test evidence

- Local deterministic core tests + model-agent integration tests: 29 passed.
- The integration smoke test drives the entire model-to-tool-to-verifier-to-ledger flow with a local **mocked model server** and passes offline trace replay.
- The real GGUF model and actual i5 performance have NOT been exercised in this environment. Model formatting quality and tokens/sec remain unverified and must be measured on the Linux test host.

## Safety and limits

This is research software, not a hardened security sandbox. Model-proposed actions are restricted to read/search. No arbitrary shell execution, host modification, RAG, persistent semantic memory, or multi-host autonomy is enabled. Do not expose the model server or API beyond localhost. Inspect the logs and outcomes before trusting AI-generated conclusions.

## Relationship to references

Claw Code and OpenClaw are architectural comparisons, not imported dependencies; their source code and any proprietary Claude Code leak are not copied here. The execution controller, policy enforcement, verifier and audit record are authored in this project and require independent, comparative evaluation before claiming technical superiority.
