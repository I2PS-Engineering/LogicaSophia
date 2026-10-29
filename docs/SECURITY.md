# Security and data handling

**LogicaSophia 0.8.2 · Built by I2PS Engineering**

## User authorization

Task previews distinguish an instruction from permission to execute it. Operations involving file output or external network requests must be explicitly confirmed. Do not submit confidential credentials, private keys, or sensitive documents as search queries.

## Workspace and output boundaries

The controller limits file access to the authorized workspace for supported operations and stores generated results separately. Uploaded project inputs and research sources are not equivalent to trusted instructions.

## Internet research

Wikipedia and Crossref metadata, or optionally Brave Search results, are obtained over HTTPS using the query authorized by the user. Such content can be inaccurate or incomplete. Provider credentials, when used, are supplied in the environment rather than written into reports or this public repository.

## Speech and models

Microphone capture is initiated explicitly. The speech recognizer runs locally after optional model installation, and the transcript is shown before submission. Voice synthesis uses the approved Lexia configuration. Optional model downloads and configured providers retain their own terms.

## Engineering evidence

Source citations, file hashes, and export logs document what the system accessed or generated. They do not prove a calculation, externally retrieved assertion, model answer, or generated image is correct. Review important outputs independently.

## Product availability

Some audio, desktop, and image capabilities require OS-level permissions, installed runtimes, and compatible hardware. Report missing components rather than showing simulated outputs as completed tasks. This application is not a hardened public multi-tenant service.
