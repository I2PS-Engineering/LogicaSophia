# Lexia — Approved I2PS Narration Configuration

**Built by I2PS Engineering · LogicaSophia v0.7.0**

Lexia is the **approved I2PS narration workflow** supplied in `SHOPIA V-KIT.zip` / `Lexia_Voice_Kit.zip`. The kit is a reproducible **engine/voice/pronunciation specification**, not evidence of independently trained I2PS voice weights. Preserve the approved original kit, WAV recordings and pronunciation mapping.

| Field | Approved value |
| --- | --- |
| Synthesis runtime | Kokoro v1.0 through `kokoro-onnx==0.6.1` |
| Voice | `af_bella` |
| Language | `en-us` |
| Speed | `1.1` |
| Output | 24 kHz mono WAV |
| Sentence pause | 0.28 seconds |
| Paragraph pause | 0.55 seconds |
| Product names | Approved recorded WAV inserts, not resynthesized |

`I2PS Dual ISA Lab` and `I2PS Dual ISA Lab 4.2 SR` use the two approved `name_*.wav` recordings. Do not synthesize those product names as replacements.

## Model provenance and verification

The two model resources are **downloaded from the Kokoro model release separately**, and their bytes **must** match the approved kit:

- `kokoro-v1.0.onnx`: SHA-256 `7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5`
- `voices-v1.0.bin`: SHA-256 `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`

The initial supplied kit did **not** contain these weights. The v0.7.0 installer fetches and verifies them on Linux; an unavailable resource or failed checksum must stop synthesis. No replacement voice or engine may be selected silently.

## Required narration gate

1. Read the complete user script. Format slides as `SLIDE 01 — TITLE` followed by paragraphs.
2. **Audit** every known pronunciation and flag every unknown technical term, abbreviation, product name or number requiring review.
3. Produce a **short real test WAV** using the approved configuration, including new terms and an approved prerecorded product-name insert where applicable.
4. Obtain explicit user approval of that test, speed and phrasing. Do not render the complete script before approval.
5. Render one approved slide for a final spot check when requested. Any correction should regenerate only the affected sections.
6. After final approval, export per-slide WAVs, combined narration WAV, subtitle SRT, `timing.json` and checksums.

The voice name “Lexia” is **not spoken** unless present in the script.

## Pronunciation examples

- I2PS: “I-two-P-S”; ISA: individually spoken letters.
- FPGA: smoothly spoken letters; RISC-V: “risk five”.
- UART: “you-art”; SHA-256: “shah two fifty-six”.
- Project acronyms and technical brands follow the approved `pronunciations.json` mapping.
- For unlisted terms, ask the user rather than invent pronunciations.

The original script-kit parameters and recorded word inserts remain the source of truth for this voice. **Real audio synthesis on the target Ubuntu i5 has not yet been field-confirmed**, so v0.7.0 does not claim a complete approved narration recording.
