# LogicaSophia

**Repository description:** LogicaSophia is a standalone Linux AI engineering system combining locally hosted Qwen-compatible inference, an original evidence-governed agent controller, scoped read-only tools, independently checked file evidence, durable audit records and a graphical console. **Built by I2PS Engineering.**

For how the AI works and what this public package-only repository does, see [Repository Description](docs/REPOSITORY_DESCRIPTION.md).

**Built by I2PS Engineering.**  
Independent, local-first AI engineering system. Proprietary package distribution; free for authorized noncommercial use.

> **Release · 0.4.1 Stable Code Baseline (October 29, 2026) — Package only**  
> A working application foundation with a genuine local-model interface, an evidence-governed agent controller, a browser-based GUI, and an explicit Qwen model deployment option. Agent/GUI behavior is covered by local automated tests; **real Qwen inference performance and tool-use reliability on the intended Ubuntu i5 have not yet been field-verified.** LogicaSophia is an AI *application* built around independently obtained foundation models. It is not a newly trained foundation model or a claim of artificial general intelligence.

![Approved LogicaSophia original gold identity](assets/identity.jpeg)

**Visual identity:** `assets/identity.jpeg` is the exact, original user-approved artwork (SHA-256 `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`), served unmodified. No substitutions, recoloring, recompression or replacement artwork without explicit authorization.

## 1. What LogicaSophia is

LogicaSophia is a standalone Linux-first **agentic AI engineering application**. It combines a replaceable language-model inference backend with our own execution-control software. The model interprets an engineering instruction and proposes the next step. LogicaSophia's host-side controller decides whether that step is authorized, carries it out using narrowly defined tools, obtains evidence, and independently checks whether the observed source data remained intact. It then makes the result available through a graphical user interface and persistent audit records.

Our research objective is **evidence-governed machine assistance**: reduce the gap between *a model claiming that it performed a task* and *an engineering system showing observable evidence that an action happened*. This is a design hypothesis requiring benchmark comparisons, not a proven superiority claim.

The project is **not** a reskin of another assistant. OpenClaw and Claude-Code-shaped public agent frameworks are technical references for design comparisons. Their agent implementations, and any leaked proprietary source, are **not bundled or represented as I2PS Engineering code**. The local foundation model, inference runtime, and their licenses are independently identifiable components.

## 2. What the AI actually does today

The 0.4.1 package supports the following locally controlled workflow:

1. Start a locally hosted, licensed foundation model using an OpenAI-compatible inference server (the launcher defaults to **Qwen3-1.7B Q4_K_M**, CPU mode, to match our initial 7.1 GiB RAM Linux qualification host).
2. Open the **LogicaSophia GUI** on `http://127.0.0.1:8766`. It displays the approved gold identity, backend status, model selector, workspace, task prompt, execution trace and result.
3. Submit a bounded **engineering task**, such as explaining a function or examining a project file.
4. The model first receives the authorized task and a manifest of visible **filenames** in the selected workspace. It must **request file content** through an allowed tool to read source bytes.
5. The host validates the request and executes only the `read_file` and `search_files` tools inside the configured workspace.
6. The agent appends bounded model decisions, tool observations and hashes to a trace; a deterministic verifier checks observed file bytes for changes after the run.
7. The GUI shows the model's final answer, tool actions, verification status and on-disk audit directory.

**A successful source-integrity check does not prove the AI's reasoning is correct.** For example, a model may read a file correctly and still misunderstand it. The GUI distinguishes this limitation explicitly. We plan subsequent task-specific factual and behavioral verification.

### Current capabilities at a glance

| Area | Working in v0.4.1 | Not yet implemented / not field-verified |
| --- | --- | --- |
| Inference | OpenAI-compatible **local** backend selection and connection | Real Qwen throughput/tool adherence on target i5 not yet verified |
| Foundation models | Qwen3-1.7B **installation choice**; alternate SmolLM2 launcher choice | Training/hosting our own base weights, or large model fleet |
| Agent loop | Model-directed file reading, searching, final answer, bounded steps | Writes, shell tools, web actions, multiple cooperating agents |
| Policy | Read-only allowlist, path/size/format checks, no arbitrary command execution | General sandbox for untrusted programs and plugins |
| Verification | File content hashes, source consistency, replayable audit chain | Semantic truth, mathematical correctness or code behavior proof |
| GUI | Branded localhost dashboard, local model discovery, live task states and evidence | Remote clients, accounts, voice, mobile applications |
| Memory | Durable task audit ledger on disk | Cross-session semantic memory and retrieval-based knowledge |
| Distributed compute | None required | Multi-node workloads, failover, GPU scheduling |

## 3. System architecture

```text
                        LogicaSophia · LOCAL LINUX HOST
     ┌───────────────────────────────────────────────────────────────┐
     │ Approved identity · gold-on-black browser UI (127.0.0.1:8766)│
     │ Workspace context · model status · task input · trace · result│
     └──────────────────────────────┬────────────────────────────────┘
                                    │ local task API
                                    ▼
     ┌───────────────────────────────────────────────────────────────┐
     │            Original LogicaSophia agent controller             │
     │ State machine · goal validation · bounded model decision loop │
     │        deny-by-default tool policy · task supervision         │
     └─────────────┬────────────────────────────────┬────────────────┘
                   │                                │
          allowed observations                local model calls
                   │                                │
                   ▼                                ▼
     ┌────────────────────────┐    ┌─────────────────────────────────┐
     │ Scoped, read-only tools│    │ OpenAI-compatible local model API│
     │ file read · text search│    │ http://127.0.0.1:8090           │
     │ path & symlink checks  │    │ llama.cpp · Qwen / other model   │
     └───────────┬────────────┘    └─────────────────────────────────┘
                 │
                 ▼
     ┌───────────────────────────────────────────────────────────────┐
     │          Independent evidence and verification layer         │
     │ SHA-256 file evidence · source consistency · trace replay     │
     │ JSON outcome · hash-linked JSONL events · SQLite audit       │
     └───────────────────────────────────────────────────────────────┘
```

**Separation of responsibilities:** the foundation model proposes a possible step; the Python host validates it. Tools never execute directly because the model wrote a command. Untrusted file contents are passed as task *data*, not high-priority instructions. The audit layer records concrete actions and outcomes instead of trusting fluent model responses.

### Runtime and model ownership

- **LogicaSophia code:** controller, task state machine, policy, filesystem observations, evidence verifier, local GUI, backend connector, audit ledger and tests.
- **External inference runtime:** `llama.cpp`, obtained separately from `ggml-org/llama.cpp`. It does not become I2PS Engineering intellectual property by being used as a dependency.
- **External foundation models:** Qwen3 GGUF or an alternative selectable licensed open-weight model. We do **not** claim the foundation model weights were authored by us.
- **Reference research:** OpenClaw and public agent harnesses may inform comparative studies; no proprietary leaked code is bundled.

## 4. One-file Ubuntu deployment: model + GUI + agent

**Target qualification machine:** Intel Core i5-6500T (4 cores / 4 threads), Ubuntu 26.10, approximately 7.1 GiB usable RAM, Intel HD 530 and ~211 GiB free disk. These are one test host's measurements, **not** hardcoded requirements for LogicaSophia.

Extract the I2PS-issued binary package on the Linux machine, open a terminal in the extracted folder, and run the included launch script:

```bash
bash LogicaSophia_Start_AI.txt
```

The launcher uses the bundled precompiled LogicaSophia application and Python runtime, performs an intentional one-time Ubuntu `apt` setup (with your authorization), and builds the independently licensed local inference backend and downloads **Qwen3-1.7B GGUF Q4_K_M** if not cached. It then starts the model on **127.0.0.1:8090** and opens the LogicaSophia UI on **127.0.0.1:8766**.

The model download needs internet on first use. All inference remains on the local machine afterward. The launcher uses a conservative four CPU threads and does not perform GPU offloading. It does not install or connect Atlas Nexus.

**Alternative comparison model**, chosen explicitly rather than silently:

```bash
bash LogicaSophia_Start_AI.txt smol
```

The default is `qwen`. **If a model server is already running on port 8090**, the launcher reuses that server and does not replace its loaded model. Exit the previous server to switch models.

### Direct commands after installation

```bash
cd /path/to/extracted/LogicaSophia_0.4.1_Stable_Ubuntu_amd64
bash LogicaSophia_Run.txt gui --workspace "$PWD/workspace" \
  --backend-url http://127.0.0.1:8090
```

For a real project, explicitly select **the workspace you authorize**:

```bash
bash LogicaSophia_Run.txt gui --workspace /path/to/your/project \
  --backend-url http://127.0.0.1:8090
```

The GUI keeps this workspace fixed for the session; it does not enumerate the rest of the host. Results are written **outside** the workspace. Do not point this early research build at sensitive repositories or secrets.

### First engineering test

The bundled `workspace/hello.py` contains:

```python
def add(a, b):
    return a + b
```

Use this exact prompt in the GUI:

> Read hello.py. What does add(7, 5) return? Show the source statement that supports your answer.

A plausible correct interpretation is **12**, supported by the line `return a + b`. More important than the answer: verify that the GUI trace shows a `read_file` operation before the final answer and that its evidence is accepted. If the model gives the right answer without reading, it must not be reported as evidence-grounded. If it returns invalid structured actions, the run should fail rather than invent success.

## 5. Verification, telemetry and auditability

Runs are saved to `~/.local/share/logicasophia/results/<run-id>/`:

- `outcome.json` — user task, model identifier, final state, model calls, answer, source evidence, elapsed time, verification scope.
- `trace.jsonl` — hash-linked append-only event sequence for replay and tamper detection.
- `events.sqlite3` — durable local task event ledger.

States include RECEIVED, VALIDATED, PLANNED, POLICY_CHECKED, EXECUTING, OBSERVING, VERIFYING, ACCEPTED, FAILED, and UNCERTAIN. A missing file, unsupported tool, malformed model response or changed evidence should not be treated as completed verified work.

The current result label **ACCEPTED** means the *source-integrity preconditions* were met. It is **not a claim** that the final answer is fully fact-checked, that new code compiled, or that a task was accomplished outside the read-only workspace.

## 6. Security and privacy boundaries

- Both the UI and model backend default to **loopback only** (`127.0.0.1`). No public deployment or LAN binding is enabled.
- GUI task POST requests need a per-process local token and reject cross-origin requests; HTML is served with restrictive browser security headers.
- The model may request only `read_file`, `search_files`, or a final answer. The host validates file paths and rejects traversal and symlink following at the read boundary.
- The agent limits tool steps, query lengths, visible manifest entries and file content sizes. Local file bytes may be sent to the **configured localhost model** and are not uploaded by LogicaSophia.
- Task output and trace contents are stored locally; restrict OS filesystem permissions yourself and review records before sharing.
- The application is **research software**, not a formally audited sandbox. Do not expose it to untrusted users or treat it as a hardened multi-tenant service.

## 7. Proposed original research and development roadmap

The future of LogicaSophia extends beyond a chatbot. These are **planned research directions**, not delivered features:

1. **Semantic verification:** testable claim-to-evidence links, deterministic checks for code and arithmetic, and calibrated uncertainty reporting.
2. **Human-authorized write operations:** patches prepared as diffs, review/approval gates, isolated execution, regression tests and precise rollback evidence.
3. **Persistent knowledge:** curated memory with provenance, retrieval, TTL/revocation and explicit separation of observed facts from suggestions.
4. **Longer autonomous workflows:** goal decomposition, subtask dependencies, bounded recovery, confidence tracking and measurable completion criteria.
5. **Multimodal interaction:** voice recognition and speech output after the text workflow is reproducibly qualified.
6. **Hardware-aware distribution:** remote Linux worker discovery, workload arbitration and live measurements; later, interface with Atlas Nexus components while keeping LogicaSophia standalone.
7. **Controlled research comparisons:** same task suites and same model against conventional agents; measure reliability, correct evidence use, latency, memory, CPU utilization, energy use and failure modes.

These experiments are how we establish **our own engineering contributions**, not by claiming ownership of the underlying model or third-party software.

## 8. Package testing and validation

The official x86-64 Linux package includes compiled I2PS application bytecode and a CPython 3.13 runtime. **It does not distribute I2PS `.py` source.** Bytecode is not inherently resistant to reverse engineering. The package is locally smoke-tested; the target Ubuntu 26.10 machine and real Qwen inference have not been validated.

The internal engineering test suite passed 40 local tests, using a simulated model for agent and GUI integrations. The packaged application entrypoint and GUI HTTP endpoints were separately tested, and the served original artwork matches the approved SHA-256. These tests do **not** prove Qwen reasoning quality on the i5.

Unit and GUI integration tests use a **simulated local model server**. A green test run confirms code-level contracts, not the language reasoning quality of Qwen. First-machine qualification requires a genuinely loaded model, at least one observed file read, an accepted audit replay and manual review of answer correctness.

The issued package includes this complete technical README, binary-use license, authorship notice, machine-checkable SHA-256 manifest, and GUI/README snapshots. Internal proprietary source and development files are not part of the package.

## 9. GUI and README snapshots

**Screenshot accuracy:** The earlier four-image collection is deprecated as release evidence. Those views included simulated task execution and stylized README renders; they are not evidence of actual Qwen inference or a live GitHub README screenshot. The current verified preview shows the packaged UI with its model backend **offline** and preserves the original approved artwork. Real Qwen screenshots require actual field execution plus corresponding audit records. See [Screenshot Evidence](docs/SCREENSHOT_EVIDENCE.md).

## 10. Product boundaries and licensing

**I2PS Engineering** maintains this LogicaSophia application and its original controller/GUI implementation. The external inference runtime and selected models have **their own copyright and licensing terms**, which must remain intact. The I2PS-owned application is distributed only as a **proprietary package**, free for permitted noncommercial use under [LICENSE.md](LICENSE.md), with authorship and third-party notices in [COPYRIGHT.md](COPYRIGHT.md). **No I2PS source code is included in the current public branch or the issued package.** Earlier public Git history remains accessible unless repository visibility is changed; deleting current files does not erase historical commits. Commercial exploitation requires separate written permission. This is **not OSI open source**.

This project is created independently for engineering research and progressive autonomous AI development. It makes **no ownership claim** over leaked source, public model weights, or third-party architectures, and it claims no proven performance advantage until the measurements and tests support one.
