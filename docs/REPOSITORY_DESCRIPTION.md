# LogicaSophia — Project Overview

**Built by I2PS Engineering.**

**Short description:** Standalone Linux AI with local Qwen inference, evidence-governed agent execution, auditable results and a graphical console. Built by I2PS Engineering.

## Product scope

LogicaSophia is a locally deployed engineering AI application. It connects a licensed local language model to an independently implemented task controller. The model proposes bounded JSON decisions; the controller permits only `read_file`, `search_files` and `final` and rejects unapproved operations.

A workspace scope limits which files may be inspected. Approved file observations carry SHA-256 evidence. The host checks observed source files again before reporting an accepted result. The GUI presents the model, task, decision trace, source observations and audit location.

**Verification scope:** Source-byte consistency and trace integrity. The current build does not prove the correctness of a model's interpretation or provide autonomous shell, code-writing or network access.

## Deployment and licensing

The default Linux package uses local Qwen3 inference through an independently licensed inference server. The model and runtime are separate from I2PS-owned application code. The public repository provides technical documentation and the approved identity artwork. The application itself is issued as a proprietary noncommercial package.

**Release:** [0.4.1 Stable Package](RELEASE_0.4.1.md)  
**Documentation:** [README](../README.md)  
**License:** [Noncommercial Binary Use](../LICENSE.md)

Real Qwen inference on the initial Ubuntu i5 qualification host remains to be measured.
