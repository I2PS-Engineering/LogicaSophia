# LogicaSophia

**Built by I2PS Engineering.**  
*An independent, model-flexible engineering assistant for Linux.*

![LogicaSophia — original approved identity](assets/identity.jpeg)

LogicaSophia brings together engineering analysis, internet research, technical document creation, image workflows, and voice interaction in one desktop application. Its I2PS-developed controller coordinates permitted operations and keeps a trace of inputs, generated files, and results.

**Version 0.8.2** · Linux x86-64 · Proprietary package · Free for authorized noncommercial use

## Explore, create, and communicate

| Workspace | What you can do |
| --- | --- |
| **Assistant** | Enter engineering requests, inspect results and evidence, search online, and work by voice. |
| **Create** | Build charts, architecture diagrams, PNG and PDF reports, source-based documents, images, and narrated material. |
| **Results** | Locate generated files, citations, output records, and source/output checksums. |

### Voice built into the conversation

- **Speaker icon on an answer:** click to hear that response read aloud with the approved **Lexia** voice; click again to stop.
- **Microphone icon on the message composer:** click to record, click again to finish, and review the editable transcript before submitting it. Speech is **not sent automatically**.
- **Narration Studio:** separately produce approved voiceovers, slide-by-slide audio, subtitles, and timing data.

The microphone uses an optional locally installed speech-recognition model. The first installation downloads its components; recordings are processed locally, not sent to an external speech-recognition API.

### Internet research

LogicaSophia is **internet-capable**. With the user's authorization, it can search Wikipedia and Crossref for sources, and optionally use Brave Search with a user-configured API key. It can export linked references and a research PDF. Local engineering tools can also work without network access. Search results are source material, not independently verified facts.

### Engineering and media output

LogicaSophia can create real **PNG charts and diagrams**, **PDF reports and briefs** from user-provided data or text, and auditable output files. The image-generation workflow connects to an explicitly configured diffusion system; for a branded image, the **actual supplied I2PS logo** is required. A configured model/checkpoint is needed to generate creative images.

**Model flexibility:** A third-party language model is optional; none is required for built-in deterministic tools. LogicaSophia's current controller is not an independently trained general-purpose language model.

## Install and open

Obtain the official **LogicaSophia 0.8.2** application archive from I2PS Engineering:

\`LogicaSophia_0.8.2_Voice_Conversation_Package.zip\`

The application is distributed separately as a package. **This public repository contains product documentation and original artwork, not the application source or a direct binary download.**

On a Linux x86-64 desktop, extract the ZIP and open a terminal in the extracted directory:

\`\`\`bash
# Install optional desktop and speech components (first use requires internet)
bash LogicaSophia_Setup_And_Start.txt

# Open the desktop application
bash LogicaSophia_Start_AI.txt qt
\`\`\`

Other entry points:

\`\`\`bash
bash LogicaSophia_Start_AI.txt doctor
bash LogicaSophia_Start_AI.txt research --query "RISC-V instruction pipeline" --confirm-network
bash LogicaSophia_Start_AI.txt work --goal "Create chart and report from measurements.csv"
\`\`\`

For input files, use the authorized workspace. The work command can preview a task before approval. See [Getting started](docs/GETTING_STARTED.md) for configuration and optional components.

## Technical overview

\`\`\`text
                LogicaSophia desktop
             Assistant · Create · Results
                         |
             I2PS task controller
            plan · authorize · execute
                 /             \
       Native engineering      Online research
       file / CSV / PNG / PDF   sources and references
                 \             /
                 Audited outputs
                files · links · hashes
                         |
                Optional adapters
             image · speech · language
\`\`\`

A file hash documents integrity, **not** the scientific correctness of an engineering conclusion. Some advanced capabilities require installed models and device-specific validation before use. See [Features and requirements](docs/FEATURES.md), [Architecture](docs/ARCHITECTURE.md), and [Security](docs/SECURITY.md).

## Documentation

[Getting started](docs/GETTING_STARTED.md) · [Features](docs/FEATURES.md) · [Voice and narration](docs/VOICE.md) · [Architecture](docs/ARCHITECTURE.md) · [Version 0.8.2](docs/RELEASE_0.8.2.md)

## Ownership and licensing

**Built by I2PS Engineering.** The original LogicaSophia identity artwork is retained without alteration. I2PS-owned software is made available under the [Noncommercial Binary Use License](LICENSE.md). This is **not an open-source software license**. Third-party inference engines, libraries, models, and online services retain their own ownership and terms; see [Third-party notices](THIRD_PARTY_NOTICES.md) and [Copyright](COPYRIGHT.md).
