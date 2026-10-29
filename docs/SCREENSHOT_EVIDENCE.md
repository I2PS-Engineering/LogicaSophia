# LogicaSophia — GUI Screenshot Evidence Policy

**Built by I2PS Engineering.**

The former four-image preview set is **deprecated as release evidence**. Generic AI illustrations are never LogicaSophia UI screenshots. Simulated-model events are not actual Qwen execution, and stylized README graphics are not captures of a real GitHub README page.

## Verified packaged GUI offline capture

- Original application: LogicaSophia v0.4.1 ZIP package, with bundled HTML, CSS and approved JPEG.
- Public presentation preview: [Offline packaged GUI render](../assets/gui-offline-package-render.png). The same preview is included in the corrected release package.
- Browser: headless Chromium using unchanged packaged HTML/CSS/JPEG. Direct localhost browser navigation was blocked in the capture environment, so styles and byte-identical image data were embedded into the document used for the capture. **This is a documented render/reconstruction of the offline interface, not a direct navigation screenshot.**
- Model state: obtained from the running packaged `GET /api/status` endpoint. It returned `backend_ready: false`; the screenshot says **Backend offline** and **No loaded model**.
- No Qwen computation or successful model-directed task is claimed from this capture.
- Original approved artwork SHA-256: `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

The prior simulated task and stylized README screenshots are excluded from the corrected package. The current README links only to the offline package-asset render. The package contains `Capture_Actual_GUI_Screenshot.txt` to capture the real interface on the user's Linux host.

## Future real Qwen snapshots

A screenshot can only be labeled as actual Qwen execution when it is linked to the model identifier, Linux host test, real `outcome.json`, and source-evidence trace. Captures must preserve their actual text and measurements. A UI screenshot is presentation evidence, not proof of reasoning correctness.

For the full product details, see the [README](../README.md). For the repository architecture, see [Repository Description](REPOSITORY_DESCRIPTION.md).

## File integrity

- Public GUI render SHA-256: `35fb369465219df88ed28ce9eb3fb763e8d8f75b8b008f43a196d1ab7e759739` (Git blob `df8ff0e167e91df5a70c3b2f8b2d18d20360db84`).
- Updated documentation-only package SHA-256: `44813299e13eb418931d2bffce12e52e3e2ba9f41537e4b21de0294a1616c15a`.
- Approved artwork SHA-256: `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

**Provenance limitation:** This browser rendering is based on exact package assets and observed offline API state, but was not obtained by direct Chromium navigation to the local server. It is not evidence of a Qwen execution.

## Capture an actual GUI screenshot on the target Ubuntu host

The **final** v0.4.1 ZIP contains `Capture_Actual_GUI_Screenshot.txt`. After the packaged application starts and the local GUI responds on `127.0.0.1:8766`, run `bash Capture_Actual_GUI_Screenshot.txt` in the extracted package folder. With Chromium or Chrome installed, this makes a genuine on-machine browser PNG, saves the actual `GET /api/status` JSON, and writes a SHA-256 capture record in the user's home folder. Capture metadata identifies the backend state; it does not fabricate a model response. A claim about a Qwen task also requires its `outcome.json` and `trace.jsonl` evidence. If no suitable browser is available, the helper exits with a clear instruction to capture the GUI manually; it does not substitute a synthetic image.
