# LogicaSophia — Repository Description

**Built by I2PS Engineering.**

**Suggested GitHub About description:** LogicaSophia — standalone Linux AI with local Qwen inference, controlled agent execution, verified file evidence and an auditable GUI. Built by I2PS Engineering.

## What this repository represents

This public repository documents the LogicaSophia application and its noncommercial **package-only distribution**. It is not a source-code release or a claim that I2PS Engineering authored the separately licensed Qwen model weights or llama.cpp runtime.

## How LogicaSophia works

1. A local foundation model receives a user task and a bounded inventory of filenames within the explicitly selected workspace.
2. The model proposes an action. The current application only accepts `read_file`, `search_files` and `final` decisions in a bounded JSON protocol.
3. The original LogicaSophia controller validates requests and executes permitted **read-only** file operations; it does not grant arbitrary shell, installation, network or write access.
4. Observations are recorded with evidence hashes, state transitions and a durable local audit record.
5. A separate integrity check re-reads the observed files to check whether the source bytes changed.
6. The GUI displays the task, available local model, action trace, result and audit location.

**Important:** An accepted file-integrity check does **not** establish that the model understood the file correctly or proved its answer. Real Qwen behavior and performance on the target Ubuntu i5 still require field testing.

## Screenshots and technical claims

Do not use generic AI illustrations as LogicaSophia interface screenshots. The prior simulated task-trace and graphical README views are **not evidence of a real Qwen run**. The new packaged-GUI capture shows an honestly reported offline inference backend and is accompanied by capture-method notes. Real task screenshots must be tied to actual run records.

## Distribution, history and identity

- The current default branch contains documentation, licensing and the original artwork only.
- Older public commits and feature branches may still be reachable. Removing code from `main` does not erase Git history or revoke previously obtained copies.
- The package is proprietary, free for authorized noncommercial use; the public repository remains public.
- Source rights, model weights and third-party runtime licenses remain separate.
- **Built by I2PS Engineering**; no AI company or assistant is identified as software author or co-author.
