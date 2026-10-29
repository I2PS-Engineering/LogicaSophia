# LogicaSophia — GUI Screenshot Evidence Policy

**Built by I2PS Engineering.**

The former four-image preview set is **deprecated as release evidence**. Generic AI illustrations are never LogicaSophia UI screenshots. Simulated-model events are not actual Qwen execution, and stylized README graphics are not captures of a real GitHub README page.

## Verified packaged GUI offline capture

- Original application: LogicaSophia v0.4.1 ZIP package, with bundled HTML, CSS and approved JPEG.
- Verified artifact: `LogicaSophia_v0.4.1_Actual_Package_GUI_Offline.png` (supplied separately with the release evidence bundle).
- Browser: headless Chromium using unchanged packaged HTML/CSS/JPEG. Direct localhost browser navigation was blocked in the capture environment, so styles and byte-identical image data were embedded into the document used for the capture.
- Model state: obtained from the running packaged `GET /api/status` endpoint. It returned `backend_ready: false`; the screenshot says **Backend offline** and **No loaded model**.
- No Qwen computation or successful model-directed task is claimed from this capture.
- Original approved artwork SHA-256: `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

## Future real Qwen snapshots

A screenshot can only be labeled as actual Qwen execution when it is linked to the model identifier, Linux host test, real `outcome.json`, and source-evidence trace. Captures must preserve their actual text and measurements. A UI screenshot is presentation evidence, not proof of reasoning correctness.

For the full product details, see the [README](../README.md). For the repository architecture, see [Repository Description](REPOSITORY_DESCRIPTION.md).
