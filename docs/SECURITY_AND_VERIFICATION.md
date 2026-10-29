# Security, Integrity and Verification

**Built by I2PS Engineering · Engineering Preview v0.7.0**

## What is verified

The host-side controller checks allowed operations, permitted paths, bounded inputs and basic evidence integrity. Read observations identify source files and SHA-256 digests. File-generation operations record the resulting filenames and output hashes. Per-run records allow independent inspection of actual input/output bytes and task status.

For agent analysis, artifacts can include `outcome.json`, hash-linked `trace.jsonl`, and `events.sqlite3`. File-generating workflows also create a workbench manifest.

**An accepted source-integrity verdict is not proof of model reasoning, mathematical correctness, image quality, legal compliance or production readiness.**

## Workflow controls

- Model/tool boundary: a generated model command does not have authority to run an arbitrary shell process.
- Workspace boundary: scoped file reads; generated deliverables are outside the authorized input workspace.
- User gate: the unified dispatcher refuses execution without explicit confirmation.
- External services: optional local model and ComfyUI endpoints should not be exposed to untrusted networks.
- Voice gate: failed Kokoro checksum, unknown pronunciation or missing user approval prevents final narration.
- Logo authenticity: corporate artwork is supplied by the user; never synthesize a falsely branded replacement.

## Test evidence

The v0.7.0 private engineering suite recorded **79 successful local automated tests**. Integration tests exercised task routing and confirmed real file outputs from example inputs. PDF layout was visually inspected and corrected. ZIP/package integrity and its manifest were also checked.

**What those tests do not show:** the PySide6 window working on the physical Ubuntu i5, Kokoro synthesizing a voice clip there, ComfyUI drawing a real image, semantic correctness of arbitrary engineering advice, or unbounded autonomous agent behavior.

## Privacy and package policy

The default public repository is documentation and approved visual identity. I2PS application source is not shipped on the current public branch. The separate packaged product contains compiled Python bytecode and is subject to a proprietary noncommercial binary-use license. Bytecode can be reverse-engineered; source non-distribution is not absolute secrecy.

Git histories, mirrors and previously downloaded copies cannot be made unavailable merely by updating a README or deleting current files. The license covers only I2PS-owned material, not independently licensed third-party runtimes and weights.

The package is an **engineering preview**, and its reliability, security and output interpretation must be qualified on real field tasks before a production label is justified.
