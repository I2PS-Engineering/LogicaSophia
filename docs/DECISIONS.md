# LogicaSophia — Engineering decisions

## LS-001 — Project identity (updated 2026-10-29)

**Accepted:** LogicaSophia, one word, capital L and S, no accent. Python package `logicasophia`.

## LS-002 — Repository placement (updated 2026-10-29)

**Superseded on 2026-10-29:** The project originally lived in `I2PS-Engineering/Atlas_Nexus/LogicaSofia/`. The canonical development repository is now `I2PS-Engineering/LogicaSophia`. The older Atlas copy is historical and must not be updated as part of LogicaSophia development.

## LS-003 — Independent Linux AI software

**Accepted:** AI app operates standalone. Orion Core, Data Core, Phoenix Core and Horizon Core are separate and will be integrated later.

## LS-004 — Model-neutral bootstrap

**Accepted for bootstrap:** A pluggable localhost inference adapter. Do not silently inherit model, hardware or Kubernetes commitments from older Atlas documentation. Benchmark before committing to a first model.

## LS-005 — Truthful readiness

**Accepted:** Without an actual local model backend, the chat API must return 503. Never fabricate model responses or claim production readiness.

## LS-006 — Local networking

**Accepted:** Bind the unauthenticated API to localhost only and reject remote inference-backend URLs. No secrets or weights in Git.

## LS-007 — Milestone 1: Standalone Linux hardware qualification (2026-10-29)

**Accepted:** One non-invasive Python command on any available Linux host, producing a local JSON qualification report. No privilege escalation, software installation, model runtime or Atlas Nexus integration. Device and network identification details must not be included in the report. Hardware fitness cannot be claimed until measured against a selected model and quantization.

## LS-008 — Model and interface policy (2026-10-29)

**Accepted:** Build a standalone gold-on-black LogicaSophia GUI using the user-approved artwork. Use a licensed local Qwen model as the default experimental inference backend while keeping the model interface replaceable. Display real task actions, file observations, verification outcomes and audit records in the GUI.

## LS-009 — Original engineering and accurate project claims (2026-10-29)

**Accepted:** Maintain a complete technical README describing the AI application, implementation, model relationship, safety boundaries and research roadmap. Do not claim foundation model authorship, copy third-party agent code, or represent source-integrity checks as verified reasoning. OpenClaw and public Claude-Code-shaped implementations remain comparative architecture references only.
