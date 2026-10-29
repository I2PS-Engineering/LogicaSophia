# Voice and narration

**LogicaSophia 0.8.2 · Built by I2PS Engineering**

## Conversation controls

**Speaker:** The small speaker icon beside an assistant's actual answer reads that answer aloud. Clicking it again stops playback. Playback uses the approved **Lexia** voice and does not replace it with an unapproved voice.

**Microphone:** The icon near the task composer starts a local recording; a second click stops it. Speech recognition places the transcript in the editable input field. Nothing is sent automatically. Voice input is optional and needs Qt audio access and a separately installed multilingual speech-recognition model.

Captured audio is handled locally. A successful transcription removes the temporary recording while retaining a text transcript and evidence hash. Audio permissions are controlled by the operating system.

## Approved Lexia specification

| Setting | Value |
| --- | --- |
| Synthesis engine | Kokoro v1.0 via \`kokoro-onnx==0.6.1\` |
| Approved voice | \`af_bella\` |
| Language | \`en-us\` |
| Speed | 1.1 |
| WAV output | 24 kHz mono |
| Sentence pause | 0.28 seconds |
| Paragraph pause | 0.55 seconds |

Two explicitly approved **I2PS Dual ISA Lab** product-name recordings are inserted from their original WAV files rather than resynthesized. Pronunciation overrides must be reviewed before long renders.

Kokoro downloads are accepted only when their SHA-256 values match:

- \`kokoro-v1.0.onnx\` — \`7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5\`
- \`voices-v1.0.bin\` — \`bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d\`

## Narration Studio

The dedicated narration workflow reads a scene/slide script, audits terminology, produces a short pronunciation test for approval, and only then proceeds to long narration. It exports scene audio, a timing record and subtitles. Changing one scene should not require an unrelated script to be rerecorded.

This is a separate production function from the one-click speaker on assistant answers.

The audio engine, microphone recording, and transcription backends depend on working system audio devices and the installed optional models.
