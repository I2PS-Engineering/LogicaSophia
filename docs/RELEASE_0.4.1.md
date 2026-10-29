# LogicaSophia 0.4.1 Stable Code Baseline — Package Only

**Built by I2PS Engineering.**

October 29, 2026. Binary/package distribution; no human-readable LogicaSophia source in the package. Local tests: 40/40 passed. Packaged Python 3.13 x86-64 runtime + compiled application bytecode; actual target Ubuntu 26.10 field test and Qwen inference are pending.

Original user-approved 1254x1254 JPEG SHA-256: `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

## Distribution

Use the authorized I2PS-issued `LogicaSophia_0.4.1_Stable_Package_Final.zip`. After extracting, execute `bash LogicaSophia_Start_AI.txt` from its directory. First launch downloads separately licensed llama.cpp and Qwen and requires Internet access and appropriate local build tools. The repository's original source-based launcher is retired.

Current documentation-corrected package SHA-256: `2111395cda9ee111f94aba6c2c95871348e5766f8c812d8ef91b39e46ef682ac`. Previous evidence-corrected ZIP SHA-256: `11537f58e87405bb1b100f41fbc1ee0ff50b54786017efe7db8be9d150c250b1`.

## Verification limits

- 40 local automated tests passed before packaging.
- Bundle starts and serves its GUI locally in a controlled smoke test; the original artwork hash matches.
- The previous preview collection has been removed from this corrected package. It showed simulated-model task events and stylized README renders. A separate honest offline-state GUI capture comes from packaged HTML/CSS/JPEG, with the model state measured from the actual running package. See [Screenshot Evidence](SCREENSHOT_EVIDENCE.md). No actual Qwen run is claimed.
- The runtime package uses bytecode, which does not prevent reverse engineering.
- The repository remains public by owner choice. Historical source commits and development branches may still be accessible. Deleting source from `main` does not conceal history or revoke earlier copies. No history rewrite has been attempted.

## License and attribution

I2PS-owned application package: proprietary, free for authorized noncommercial use only. See [LICENSE.md](../LICENSE.md) and [COPYRIGHT.md](../COPYRIGHT.md). No AI provider credited as software author or co-author. Third-party model weights and inference runtime retain their own licenses.

## Documentation and snapshot correction (same v0.4.1 application code)

The corrected package removes misleading demonstration snapshots, retains the unchanged application binaries and approved JPEG, and adds one explicitly labeled offline presentation render plus a Linux on-host screenshot capture helper. Internal package SHA-256 manifest and ZIP archive were regenerated and verified. No Qwen field result is represented as measured. No historical commits or dates were rewritten.

## Documentation cleanup (application unchanged)

The public GUI render is now committed as an actual PNG and verified against its SHA-256; it is labeled as a browser render of packaged GUI assets in an offline model state, not direct live navigation. The corrected ZIP contains one offline image, not the retired simulated-task and stylized README set. Package metadata and checksums were regenerated; all 19 bundled LogicaSophia application files match the previous packaging baseline byte-for-byte. The original artwork is unchanged. Qwen field inference remains unverified.

## Package-documentation finalization (2026-10-29)

The final ZIP includes `Capture_Actual_GUI_Screenshot.txt`, the previously missing on-machine screenshot helper. The tool captures the actual local GUI in installed Chromium/Chrome and saves an accompanying application status JSON and SHA-256 capture record. Its Bash syntax has been checked; browser operation on the target Ubuntu i5 remains to be validated. Source-free application bytecode and the approved original JPEG were unchanged by this packaging revision. The one included screenshot is an **offline presentation render**, not evidence of Qwen inference. Package integrity and 738 SHA-256 entries were verified.
