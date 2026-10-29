# LogicaSophia 0.4.1 Stable Code Baseline — Package Only

**Built by I2PS Engineering.**

October 29, 2026. Binary/package distribution; no human-readable LogicaSophia source in the package. Local tests: 40/40 passed. Packaged Python 3.13 x86-64 runtime + compiled application bytecode; actual target Ubuntu 26.10 field test and Qwen inference are pending.

Original user-approved 1254x1254 JPEG SHA-256: `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`.

## Distribution

Use the authorized I2PS-issued `LogicaSophia_0.4.1_Stable_Ubuntu_amd64_Package.zip`. After extracting, execute `bash LogicaSophia_Start_AI.txt` from its directory. First launch downloads separately licensed llama.cpp and Qwen and requires Internet access and appropriate local build tools. The repository's original source-based launcher is retired.

Package SHA-256: `b9988090fd25e2d4e3f56a7393e8a866d676e7b162d32434086c6f8061a23690`.

## Verification limits

- 40 local automated tests passed before packaging.
- Bundle starts and serves its GUI locally in a controlled smoke test; the original artwork hash matches.
- GUI snapshots showing task execution use a **simulated local model**, not genuine Qwen inference.
- The runtime package uses bytecode, which does not prevent reverse engineering.
- Historical source commits remain in GitHub; changing repository visibility is required to prevent casual public browsing of that history.

## License and attribution

I2PS-owned application package: proprietary, free for authorized noncommercial use only. See [LICENSE.md](../LICENSE.md) and [COPYRIGHT.md](../COPYRIGHT.md). No AI provider credited as software author or co-author. Third-party model weights and inference runtime retain their own licenses.
