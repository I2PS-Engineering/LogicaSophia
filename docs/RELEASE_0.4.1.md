# LogicaSophia 0.4.1 — Stable Package

**Built by I2PS Engineering.**

**Release date:** October 29, 2026  
**Platform:** Ubuntu Linux x86-64 (target host: Intel Core i5-6500T, 7.1 GiB RAM)  
**Distribution:** Binary/package only, proprietary I2PS application; authorized noncommercial use under [LICENSE.md](../LICENSE.md).

## Package

**Filename:** `LogicaSophia_0.4.1_Stable_Package_Final.zip`

**SHA-256:** `2111395cda9ee111f94aba6c2c95871348e5766f8c812d8ef91b39e46ef682ac`

Unpack the official I2PS-issued archive and run `bash LogicaSophia_Start_AI.txt` from its extracted folder. An internet connection is needed for the initial external llama.cpp build and Qwen model download. The local GUI is at `http://127.0.0.1:8766` and the local model service uses port `8090`. The default Qwen3-1.7B Q4_K_M selection is replaceable.

The package includes compiled I2PS application bytecode, a Python 3.13 runtime, the original approved artwork, documentation, integrity manifest and `Capture_Actual_GUI_Screenshot.txt`. It does not include proprietary I2PS `.py` application source. Bytecode should not be considered resistant to reverse engineering.

## Verified functionality and boundaries

- **40/40 local application and GUI tests passed** with a controlled model stub.
- Packaged app starts locally and responds to GUI HTTP requests.
- The approved artwork was preserved byte-for-byte (SHA-256 `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`).
- Model-directed read-only `read_file` and `search_files` tools are enforced by a bounded host-side controller.
- Traces and evidence are recorded in `outcome.json`, `trace.jsonl` and `events.sqlite3`. Acceptance validates source-file integrity, not semantic correctness.
- Package ZIP and 738 integrity-manifest entries passed consistency checks.
- A real Qwen task, CPU throughput, answer accuracy and GUI capture on the target Ubuntu i5 **have not yet been field-tested**.

## Capture a real GUI session

Start the app and run `bash Capture_Actual_GUI_Screenshot.txt` from the extracted package folder on the Ubuntu host. The helper saves a browser image, API status and checksum record. See [GUI capture requirements](SCREENSHOT_EVIDENCE.md). A Qwen execution claim additionally requires the matching real task trace and outcome.

## Ownership

The LogicaSophia application and original engineering components are **built by I2PS Engineering**. Qwen weights and the llama.cpp inference runtime are external dependencies governed by their own terms. See [Copyright](../COPYRIGHT.md) and [License](../LICENSE.md).
