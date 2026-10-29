# LogicaSophia

**Built by I2PS Engineering.**  
**Independent AI engineering platform · Linux-first · Proprietary noncommercial package distribution**

![Original approved LogicaSophia identity](assets/identity.jpeg)

LogicaSophia is an independently engineered agentic AI application for **engineering analysis, technical documents, image and speech workflows, and evidence-governed task execution**. It combines an original I2PS task controller with a replaceable inference interface and real file-generation tools. It is designed to grow into a more capable autonomous engineering system without making any external foundation-model vendor the identity of the project.

> **Current release: v0.7.0 — Private Engineering Preview · October 29, 2026.** The packaged analysis and engineering-deliverable paths have passed **79 local automated tests**. Real Qt visual interaction, Kokoro audio synthesis and diffusion-image generation on the designated Ubuntu i5 have **not** been field-verified. This is an engineering preview, not a fully qualified production AI or an independently trained foundation model.

## What makes LogicaSophia different

The central contribution is the **I2PS-controlled engineering workflow**: task routing, explicit authorization, bounded tools, source observations, integrity checks, output manifests, and a readable action record. A user should be able to request a deliverable, see which inputs and methods were used, and inspect the actual output instead of trusting a confident but unsupported claim.

**Model neutrality is a design constraint.** The native default is a limited deterministic analyzer and engineering tool dispatcher. An external language model can be connected deliberately; **Qwen is neither required nor the default architecture**. External weights and runtimes remain separately licensed. LogicaSophia does not claim to have trained a new general-purpose foundation model.

## What the current application can do

| Capability | v0.7.0 implementation | Evidence and limits |
| --- | --- | --- |
| Engineering source inspection | Native AST-based Python inspection and bounded read-only file tools | Tested locally; not general programming intelligence |
| Unified engineering requests | Preview and confirm a proposed analysis, artifact, image, speech or narration task | Deterministic routing, not free-form autonomous multi-step reasoning |
| Measured-data analysis | Read numeric CSV, compute statistics, export actual PNG chart and PDF report | Tested on sample data; results are only as reliable as the input |
| Architecture visualization | Create PNG/PDF diagrams from explicitly supplied modules and connections | Does not invent undisclosed system architecture |
| General image generation | Adapter to a locally configured ComfyUI checkpoint | Needs actual image model and runtime; not field-verified |
| Logo placement | Insert a supplied authentic logo into a generated picture | No replacement/imaginary I2PS logo; visual review still required |
| Text-to-speech | Lexia adapter for approved Kokoro voice | Installed weights and actual voice test still required |
| Narration | Pronunciation audit, short test, approval, slide WAVs, timestamps and subtitle export | Long-form rendering requires human approval and verified model |
| Graphical desktop | Gold/black Qt Studio with **Assistant, Create, Results** | Code integrated; Qt visual field test pending |
| Local audit | Source hashes, task outcomes, evidence traces and export manifests | Source integrity is not proof of answer correctness |

The product can generate **real engineering PNG/PDF files** today under tested local conditions. Its text-to-image and Lexia voice adapters are genuine integrations but **not demonstrations of completed field inference**. The request “a skateboarding cat with the I2PS logo on its shirt” needs a configured image model and the real logo file; it must not return a fabricated preview.

## One task, one controlled workflow

1. You enter an engineering or creative instruction in the **Assistant** panel, or select a specific task under **Create**.
2. The I2PS dispatcher classifies the task against supported operations and shows an inspectable plan, required inputs and missing dependencies.
3. **Execution requires explicit confirmation.** Unavailable models, missing data or missing logos are reported instead of silently substituted.
4. Approved local tools execute using scoped input files and generate outputs outside the read workspace.
5. **Results** exposes real PNG, PDF, WAV, subtitle, JSON, and evidence files as appropriate to the task.

**Example engineering instruction:** `Create an engineering report and chart from measurements.csv`. This reads supplied numeric source data; the example proof is **sample data**, not a claimed benchmark from the user’s hardware.

**Example architecture instruction:** `Architecture: Sensor -> Controller -> Audit`. Only these explicitly supplied components and connections are drawn.

**Example creative instruction:** `Make a picture of a cat skateboarding with the I2PS logo on its shirt`. This requires a real local diffusion checkpoint and the user-provided logo.

**Example narration script:**
~~~text
SLIDE 01 — INTRODUCTION
Welcome to the I2PS Engineering laboratory.

SLIDE 02 — RESULTS
Here are the measurements collected during the experiment.
~~~
The script is audited for pronunciation before any authorized long render.

## Installation and first use

The v0.7.0 engineering package is a **separate, source-free ZIP delivered by I2PS Engineering**, not a source checkout of this public repository. Extract it on an **Ubuntu x86-64** computer. From inside the extracted package directory:

~~~bash
# Installs optional Qt, engineering document, and Lexia dependencies;
# downloads and verifies the approved Kokoro model files.
bash LogicaSophia_Setup_Lexia_And_Studio.txt

# Launch the desktop interface.
bash LogicaSophia_Start_AI.txt qt
~~~

To use the native, no-vendor-required engine in the terminal:

~~~bash
bash LogicaSophia_Start_AI.txt native
~~~

To preview and then authorize a real measured-data deliverable:

~~~bash
bash LogicaSophia_Start_AI.txt work --goal 'Create chart and report from measurements.csv'
bash LogicaSophia_Start_AI.txt work --goal 'Create chart and report from measurements.csv' --confirm
~~~

**No Qwen download is required.** The Qt and voice setup needs external packages and an initial internet connection; substantial resources are downloaded for Kokoro. Full hardware prerequisites and command options are in [Installation](docs/INSTALLATION.md).

## System design

~~~text
                      LOGICASOPHIA · I2PS ENGINEERING
          ┌────────────────────────────────────────────┐
          │  Qt Studio: Assistant · Create · Results   │
          └────────────────────┬───────────────────────┘
                               │ user instruction
                  ┌────────────▼─────────────┐
                  │ Governed task dispatcher │
                  │ plan · check · authorize │
                  └─────┬──────────┬─────────┘
                        │          │ optional explicit
             native tools│          ▼
              ┌──────────▼─────┐ ┌─────────────────────┐
              │ Analysis &     │ │ External local model│
              │ engineering    │ │ (not required)      │
              └─────┬──────────┘ └─────────────────────┘
                    │
        ┌───────────┼──────────────┐
        ▼           ▼              ▼
     PNG / PDF   Image model    Lexia / Kokoro
        └───────────┼──────────────┘
                    ▼
        Files · provenance · hashes · audit records
~~~

All generated work is an **artifact that can be inspected**. The original controller enforces read-only input access on qualified paths and stores results separately. More autonomous code edits, validated execution and long-lived memory remain development targets.

Read the [Architecture](docs/ARCHITECTURE.md), [Features and qualification](docs/CAPABILITIES.md), [Artifact Studio](docs/ARTIFACTS_AND_IMAGES.md), [Lexia voice specification](docs/VOICE_LEXIA.md), and [Security and verification](docs/SECURITY_AND_VERIFICATION.md).

## Visual identity and authorship

**Built by I2PS Engineering.** The original approved **LogicaSophia** gold-on-black JPEG is preserved **byte-for-byte** in [assets/identity.jpeg](assets/identity.jpeg), SHA-256 `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`. No substituted or invented identity artwork.

The I2PS-owned controller, GUI, integration and engineering application are distributed as a **proprietary binary/bytecode package, free only for authorized noncommercial use**, under [LICENSE.md](LICENSE.md). The public repository supplies product documentation, licensing and the approved identity asset; it does not distribute the application’s human-readable source. Publishing a public GitHub repository does **not** make this software OSI open source. Bytecode should not be considered resistant to reverse engineering.

Third-party libraries, inference frameworks and weights retain their independent ownership and licenses. **I2PS Engineering is the application author and maintainer**; neither an external AI model nor an assistant is named as a software co-author.

## Verification and current status

- **79/79 local automated application tests passed**, including 10 unified-dispatcher integration tests.
- The local measured-data example generated a real PNG/PDF pair; PDF pagination was visually checked and corrected.
- ZIP structure and **1,189 package manifest entries** were previously verified during v0.7.0 packaging.
- **Not yet qualified:** Qt desktop on the target host, real Kokoro narration output, a diffusion-generated cat picture, or general engineering reasoning via an independently trained AI model.
- Source and output file hashes prove integrity of recorded bytes, **not** correctness of an AI interpretation, future performance or code execution.

See [v0.7.0 Release Record](docs/RELEASE_0.7.0.md), [Verification](docs/SECURITY_AND_VERIFICATION.md), and [Research Roadmap](docs/ROADMAP.md).

**This public repository remains documentation-first.** The verified v0.7.0 ZIP is distributed separately until an official package release asset is published. Do not clone this repository expecting the application source or a runnable binary.
