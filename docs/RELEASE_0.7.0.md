# LogicaSophia v0.7.0 — Private Engineering Studio

**Built by I2PS Engineering.**  
**Release date:** October 29, 2026  
**Status:** Engineering Preview — **not** a production stable AI release.

## Delivery

Binary/package-only Ubuntu x86-64 archive supplied separately by I2PS Engineering:
`LogicaSophia_0.7.0_Private_Engineering_Studio.zip`

**SHA-256:** `b9ef54e36d9f3ecc569d5be66978955fcbf8d24e9986351db93b596d1e8f62cf`

**Important:** The ZIP is not included in this public repository; this document does not represent that a GitHub Release asset has already been published.

The package includes the I2PS application in bytecode form, a bundled CPython runtime, approved original artwork, command wrappers and license notices. The separate Kokoro model files and user-selected image checkpoints are not bundled. Proprietary I2PS source is not publicly distributed.

## Implemented changes relative to the earlier application baseline

- Unified model-neutral engineering task dispatcher with explicit preview/confirm.
- Native source analysis without a mandatory foundation model.
- Real engineering CSV chart PNG/PDF export and architecture diagram export.
- Qt Studio with Assistant, Create and Results areas.
- Adapter for real local ComfyUI image generation and authentic corporate logo.
- Lexia voice/narration workflow, pronunciation audit and user approval gates.
- Audit manifests for generated output files, original visual identity preserved.

## Validation scope

**79 local automated tests** passed at build time, including ten task-workbench integration tests. A real measured-data example generated output files; PDF page layout was reviewed and fixed. ZIP integrity and **1,189 manifest entries** were checked.

**Not yet demonstrated:** real Qt UI testing on the target Ubuntu i5, real Kokoro audio generation, text-to-image with a loaded checkpoint, and general-purpose reasoning performance. A production stability claim would be premature.

### Installation

~~~bash
bash LogicaSophia_Setup_Lexia_And_Studio.txt
bash LogicaSophia_Start_AI.txt qt
~~~

Native model-free mode:
~~~bash
bash LogicaSophia_Start_AI.txt native
~~~

See [Installation](INSTALLATION.md) and [Capabilities](CAPABILITIES.md).
