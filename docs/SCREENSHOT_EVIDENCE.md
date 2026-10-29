# LogicaSophia — GUI Capture and Evidence

**Built by I2PS Engineering.**

## Authentic application screenshots

The official GUI uses the original approved gold-on-black JPEG artwork, SHA-256 `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

The issued v0.4.1 package contains `Capture_Actual_GUI_Screenshot.txt`. After starting the application on Ubuntu, run:

```bash
bash Capture_Actual_GUI_Screenshot.txt
```

The helper uses an installed Chromium/Chrome browser to capture the **actual running GUI** at `http://127.0.0.1:8766`. It also saves the genuine `GET /api/status` response and file checksums. It has been syntax-checked; a successful screenshot from the target i5 machine has not yet been reported.

## Evidence required for inference results

A screenshot must be labeled with its observed runtime and model state. A claim that Qwen completed a task requires the corresponding real `outcome.json`, `trace.jsonl`, model identifier and actual Ubuntu host test. The GUI's file-hash acceptance demonstrates evidence stability, **not** the factual correctness of an AI answer.

The repository does not use decorative or reconstructed dashboards as evidence of actual Qwen execution.
