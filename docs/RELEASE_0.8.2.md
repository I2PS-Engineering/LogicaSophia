# Release 0.8.2

**LogicaSophia — Built by I2PS Engineering**  
**October 29, 2026 · Linux x86-64**

**Official application archive:** \`LogicaSophia_0.8.2_Voice_Conversation_Package.zip\`  
**SHA-256:** \`c6835ff6387fff0aaff032a0a763127d4fd8fc5fa6cdaff61fa8dc498ab3ba50\`

This repository provides public product documentation and the approved original identity; the proprietary application ZIP is distributed separately through I2PS Engineering.

## Release highlights

- Conversation-level **speaker** control for reading an assistant answer aloud through Lexia, with stop playback.
- Conversation-level **microphone** control that records and transcribes into an editable input without automatically sending the request.
- Internet research with source links, PDF output, and explicit network authorization.
- Engineering PNG/PDF reports, charts, architecture diagrams, and source-grounded briefs.
- Optional model-backed image creation and separate scene narration.
- Qt Studio organized into Assistant, Create and Results.

## Dependencies and availability

The core package includes its runtime, native controller and document-generation libraries. Qt, Kokoro voice assets and multilingual speech recognition require optional first-time installation. Creative image inference requires a configured ComfyUI checkpoint. A specific language-model vendor is not mandatory.

Core application and workflow tests have passed. Hardware-dependent Qt interaction, microphone transcription, approved-voice synthesis, and diffusion-image output require validation on the destination machine. This version should not be represented as independently trained general AI or an unrestricted autonomous system.

**Terms:** [Noncommercial Binary Use License](../LICENSE.md) · [Third-party notices](../THIRD_PARTY_NOTICES.md).
