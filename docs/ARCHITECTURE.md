# Architecture

**LogicaSophia 0.8.2 · Built by I2PS Engineering**

LogicaSophia is built around an **I2PS-developed task controller**, not around one mandatory language-model provider.

\`\`\`text
       User instruction / voice transcript
                      |
             Qt conversation UI
           Assistant / Create / Results
                      |
                Task planner
          scope · permission · preview
                      |
             Authorized execution
       /--------------+---------------\
  Native analysis  Online research  Optional models
  CSV/AST/PNG/PDF  cited sources    images/speech/text
       \--------------+---------------/
                      |
                Output records
         files · source links · SHA-256
\`\`\`

## Responsibilities

**Desktop interface:** the Qt application organizes conversations, project workspaces, media controls, creation tasks, and output files. Recording and transcription require an explicit user interaction.

**Controller:** a bounded native task router previews operations and enforces applicable user confirmation and workspace restrictions before file-producing or internet operations. The current controller supports constrained deterministic tasks, not arbitrary command execution.

**Tool adapters:** local Python inspection, numeric processing, PDF/PNG generation, HTTPS source retrieval, optional image inference through ComfyUI, and speech synthesis/recognition through separately installed runtimes.

**Evidence:** output locations, source references, hashes, and status are recorded for audit. Integrity records do not by themselves validate factual or engineering correctness.

## Interfaces and deployment

The current end-user interface is a **Qt desktop program for Linux x86-64**. Online research is a permitted capability within that application; this does **not** mean the Qt window has a remote browser login. Internet queries are sent only after user authorization.

Approved branding is the original LogicaSophia artwork at [identity.jpeg](../assets/identity.jpeg). The official I2PS logo used in generated branded imagery is a separate user-supplied asset.
