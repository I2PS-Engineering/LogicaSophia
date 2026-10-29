# Getting started

**LogicaSophia 0.8.2 · Built by I2PS Engineering**

## Requirements

- Linux x86-64 with a graphical desktop for Qt Studio.
- Network access for optional component installation and online research.
- A microphone and speaker for voice interaction.
- Additional memory, compute, and storage for speech and image models; requirements depend on the models selected.

The supplied package includes its own Python runtime and core numeric, plotting, PDF, and audio-file libraries. Optional Qt, Kokoro, and speech-recognition components are installed during first-time setup. A ComfyUI installation and diffusion checkpoint are configured separately.

## Start the application

Get the official \`LogicaSophia_0.8.2_Voice_Conversation_Package.zip\` from I2PS Engineering. Extract it. In a terminal opened in the extracted package directory, run:

\`\`\`bash
bash LogicaSophia_Setup_And_Start.txt
bash LogicaSophia_Start_AI.txt qt
\`\`\`

The application opens as a **Qt desktop window**, not a remote website or login portal. Select a project workspace with **Choose folder**. Access Assistant, Create, and Results from the main tabs.

## Check components

\`\`\`bash
bash LogicaSophia_Start_AI.txt doctor
\`\`\`

For microphone transcription setup only:

\`\`\`bash
bash LogicaSophia_Setup_Voice_Chat.txt
\`\`\`

The initial setup downloads the optional speech-recognition engine and multilingual model. Captured speech is transcribed locally. If the model cannot be installed, voice input remains unavailable until the issue is corrected; the rest of the application can still be used.

## Use voice in Assistant

1. Select the **microphone** near the message input to begin recording, then select it again to stop.
2. Review or correct the transcription.
3. Submit the resulting text using the ordinary task action.
4. Select the **speaker** beside an assistant answer to hear the approved Lexia voice, and select again to stop playback.

For long-form production, choose **Narration** in Create instead. See [Voice and narration](VOICE.md).

## Engineering and internet research

Preview a supported task:

\`\`\`bash
bash LogicaSophia_Start_AI.txt work --goal "Create chart and report from measurements.csv"
\`\`\`

Approve a reviewed task:

\`\`\`bash
bash LogicaSophia_Start_AI.txt work --goal "Create chart and report from measurements.csv" --confirm
\`\`\`

Research online with explicit authorization:

\`\`\`bash
bash LogicaSophia_Start_AI.txt research --query "RISC-V instruction pipeline" --confirm-network
\`\`\`

Wikipedia and Crossref need no search API key. For optional Brave Search, configure \`LOGICASOPHIA_BRAVE_API_KEY\` in the process environment; never add credentials to files committed to GitHub.

## Distribution

This public GitHub repository provides documentation and the original visual identity. Obtain the application package through an authorized I2PS Engineering channel; no executable download is hosted in this repository. The current release is intended for evaluation and noncommercial use, not unrestricted service hosting.
