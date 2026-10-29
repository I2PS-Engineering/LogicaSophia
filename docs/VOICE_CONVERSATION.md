# Voice Conversation — LogicaSophia 0.8.2

**Built by I2PS Engineering.**

The Assistant's **speaker icon** (beside the answer) uses the approved Lexia narration kit to read that specific answer aloud. It is not an always-on chatbot voice, and no other voice is substituted when the approved resources are unavailable.

The **microphone icon** (beside the prompt) records a user-initiated short clip with QtMultimedia (16 kHz mono, PCM). The second click ends capture and initiates local transcription through the optional multilingual faster-whisper base model. The transcript appears in the editable task box. The user decides whether to select **Analyze** or **Search online** afterwards.

The spoken recording is **not uploaded to a speech service**. By default it is deleted after successful transcription, while a text transcript, source-audio SHA-256, detected language and a review-required flag are stored for audit. On failure, the recording remains available for troubleshooting.

**First-time setup:** `bash LogicaSophia_Setup_And_Start.txt` installs optional Qt, approved Kokoro and multilingual speech recognition resources. Or run the dedicated `bash LogicaSophia_Setup_Voice_Chat.txt`. This requires Internet during setup, but the audio path itself is local.

**Testing:** 113 local automated tests passed overall, including 9 transcription tests using a controlled model factory. Real microphone access, Qt playback, actual faster-whisper transcription and full Kokoro output remain **unverified on the target Ubuntu host**. The original slide Narration Studio stays unchanged.

The voice-recognition engine is independent of the optional language-model inference interface; no Qwen or other model is required for native engineering work.
