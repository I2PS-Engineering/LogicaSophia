# Features

**LogicaSophia 0.8.2 · Built by I2PS Engineering**

| Feature | Function | Requirements |
| --- | --- | --- |
| Assistant | Governed task planning, scoped source inspection, evidence and result display | Core package |
| Internet research | Wikipedia/Crossref source retrieval, optional Brave indexed search, cited PDF report | Network permission; Brave API key optional |
| Engineering charts | Numeric CSV analysis, PNG charts and PDF reports | Authorized source data |
| Architecture diagrams | PNG/PDF drawings from specified components and links | Structured design input |
| PDF documents | Source-based PDF briefs from approved Markdown/text | Source document or supplied text |
| Creative images | Model-backed image generation, optionally with an authentic supplied logo | ComfyUI and a compatible model/checkpoint |
| Voice input | Microphone capture, editable transcription, explicit send | Qt microphone access and locally installed multilingual STT |
| Answer playback | Speaker control beside responses, approved Lexia voice | Kokoro runtime and verified voice files; audio output |
| Narration | Script audit, pronunciation approval, scene WAV files, subtitles and timings | Approved Lexia profile, model files, script approval |
| Results | Generated files and source/output hash records | Core package |

The three desktop areas are **Assistant**, **Create**, and **Results**. Text-to-speech for ordinary answers and microphone input belong to the Assistant conversation, while long-form narration remains in Create.

## Capability boundaries

The local I2PS controller handles specified operations; it is **not a newly trained foundation language model** and does not yet offer unrestricted autonomous code changes, arbitrary shell execution, or verified interpretation of all internet content.

Hardware-dependent features such as Qt audio, image inference, speech recognition and speech playback require setup and acceptance on the user's machine. An unavailable model is a dependency failure, not a successful media-generation result.

For operating instructions, see [Getting started](GETTING_STARTED.md).
