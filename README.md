# LogicaSophia

**BUILT BY I2PS ENGINEERING**  
**Independent AI engineering platform · Internet-connected research · Linux-first · Proprietary noncommercial package**

![Original approved LogicaSophia artwork](assets/identity.jpeg)

LogicaSophia is an I2PS Engineering application for **engineering analysis, online research, real PNG/PDF deliverables, creative image workflows, and approved speech/narration**. The system uses an original evidence-governed task controller and replaceable inference interfaces.

> **Current engineering release: 0.8.1 — Connected Engineering Preview · October 29, 2026.**  
> 104 local tests passed; packaged CLI, consent controls and PDF export checked. Online provider tests used mocked HTTP, so live search on the designated Ubuntu i5 is not yet field-qualified. Qt window operation, actual diffusion image generation and Kokoro audio remain pending field validation. This is not a production-ready general autonomous AI or newly trained foundation model.

## Internet connection and intelligence

**LogicaSophia is not restricted to offline mode.** It can send an approved research query to real Internet services, retrieve cited sources and generate a documented PDF. It can also run native engineering tools locally when online access is unnecessary.

The model-independent controller currently routes `Research ...` and `Search web for ...` to a real network adapter. **Wikipedia and Crossref** provide public references without an API key. **Brave Search** provides optional broad-index search when the user explicitly configures `LOGICASOPHIA_BRAVE_API_KEY`. The query is sent only after authorization; failed services are disclosed, not replaced with invented results. The report contains actual provider metadata, source links and timestamps rather than AI-generated guesses.

**Model neutrality:** Qwen is neither the project's foundation nor a mandatory default. The native engine handles deterministic work, while external inference models can be deliberately configured. A trained general-purpose I2PS foundation model and unrestricted autonomous browsing are not yet implemented.

## Engineering features

| Capability | Included engineering pathway | Qualification |
| --- | --- | --- |
| Online research | Network search of Wikipedia/Crossref; optional Brave; `sources.json`, `research.md`, cited PDF and hashes | Request/response and output integration tests; live host test pending |
| Source inspection | Scoped file reads and limited native Python AST/numeric analysis | Local automated tests |
| Engineering PNG/PDF | CSV measurements to chart, numeric statistics and PDF; structured architecture diagrams | Real artifact generation tested on sample inputs |
| Document studio | Paginated source-grounded PDF briefs from approved Markdown/text | Automated PDF and source-hash tests |
| Qt desktop | **Assistant / Create / Results**, workspace selector, Web search, artifact forms | Code integrated; desktop visual test pending |
| Creative images | Local ComfyUI adapter; user-uploaded authentic I2PS shirt logo | Image checkpoint/real generation not yet qualified |
| Lexia speech | Approved Kokoro v1.0 / `af_bella` / `en-us` / speed 1.1 | Kit/audit validated; synthesis pending real model download |
| Slide narration | Pronunciation audit, human approval, scene WAVs, subtitles and timing manifest | Gate tested; long-form audio pending |
| Source/output evidence | Hashes, task record, user approval and traceable output directory | Integrity does not prove factual correctness |

**Example image request:** “Make a picture of a cat skateboarding wearing a shirt with the authentic I2PS logo.” The real I2PS logo and a working image-generation checkpoint must be supplied. The LogicaSophia identity artwork is **not** silently substituted for the corporate shirt logo.

## Deployment

The public repository is a **documentation and identity repository**, not an application source checkout. Get the approved `LogicaSophia_0.8.1_Connected_Engineering_Package.zip` from I2PS Engineering and extract it on x86-64 Linux.

Run the included commands from its extracted folder:

```bash
# No network request: inspect installed components
bash LogicaSophia_Start_AI.txt doctor

# User-authorized Internet research and real cited PDF export
bash LogicaSophia_Start_AI.txt research --query 'RISC-V pipeline architecture' --confirm-network

# Preview first, then approve the requested operation
bash LogicaSophia_Start_AI.txt work --goal 'Research thermal design of compact server enclosures'
bash LogicaSophia_Start_AI.txt work --goal 'Research thermal design of compact server enclosures' --confirm

# CSV-based actual chart and PDF output
bash LogicaSophia_Start_AI.txt work --goal 'Create chart and report from measurements.csv' --confirm

# Install optional desktop and approved Lexia dependencies, then open Qt
bash LogicaSophia_Setup_And_Start.txt
bash LogicaSophia_Start_AI.txt qt
```

**Bundled:** CPython 3.13, I2PS compiled application, NumPy, Pillow, ReportLab, SoundFile, original artwork and Lexia approved kit assets, plus a standard-library HTTPS research client.

**Additional first-time dependencies:** PySide6/Qt, Kokoro ONNX and checksum-verified Kokoro v1.0 model files. Creative image generation requires a separate configured diffusion checkpoint and runtime; a broad-web Brave Search token is optional. A source-free bytecode package is not immune to reverse engineering.

For procedures and provenance see [Installation](docs/INSTALLATION.md), [Internet Research](docs/ONLINE_RESEARCH.md), [Capabilities](docs/CAPABILITIES.md), [Architecture](docs/ARCHITECTURE.md), [Voice / Lexia](docs/VOICE_LEXIA.md) and [Security & Verification](docs/SECURITY_AND_VERIFICATION.md).

## Architecture

```text
         LogicaSophia Qt Studio · I2PS Engineering
          Assistant  ·  Create  ·  Results
                         |
            Governed task dispatcher
            plan · validate · approve
                 /          \
        Native tools       Online tools
        AST / CSV          HTTPS research
        PNG / PDF          cited metadata
                 \          /
                  Source evidence
                  SHA-256 / audit
                         |
           Optional explicit model adapters
           Text inference · Image · Lexia
```

The application records **what was actually read or generated**. File-integrity checks do not establish semantic correctness; externally retrieved snippets and article metadata are not fact-checked conclusions. The controller does not silently authorize general code execution or unrestricted access to online accounts.

## Identity and license

**Built by I2PS Engineering.** The approved 1254 × 1254 original LogicaSophia JPEG is committed at [assets/identity.jpeg](assets/identity.jpeg), SHA-256 `03cb470f5d16dea18cd8991d5fcb4419383ad58d07375e7e7f781ccf93a67d39`, unchanged. The authorship belongs to I2PS Engineering, not to an outside AI assistant or model provider.

The I2PS application uses [proprietary noncommercial package licensing](LICENSE.md). Source files are not distributed in the current public branch or package. Third-party models, runtimes, search services and libraries retain their own licenses and terms. This is **not OSI open source**.

**Engineering release details:** [v0.8.1](docs/RELEASE_0.8.1.md). Hardware-specific live web, Qt, Kokoro and diffusion checks remain open before a full public stable qualification.
