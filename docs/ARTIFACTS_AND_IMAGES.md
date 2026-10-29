# Engineering Artifacts and Image Studio

**Built by I2PS Engineering · v0.7.0**

## File-producing workflow

A user request passes through `plan_instruction`, which returns the target tool, expected inputs and missing prerequisites. **Nothing is generated until explicit execution confirmation.** Actual outputs are created in a new run directory and receive a SHA-256 evidence manifest.

## Numeric data → chart and report

- Input: user-authorized CSV with at least two validated numeric columns.
- Operations: parse the actual data, identify usable columns, compute summary statistics and draw the corresponding trend.
- Outputs: `engineering.png`, `report.pdf` and a source/output manifest.
- Verification: source-file SHA-256, file-format checks and review of page layout.
- Integrity limit: the software can correctly summarize **incorrect input measurements**. No benchmark has been performed merely because a chart exists.

The demonstrated 13-row sample is synthetic instructional input. The final A4 example was visually checked for clipping/overlap.

## Structured architecture → PNG/PDF

Supply explicit nodes and arrows in the instruction or a structured JSON diagram specification. The implementation bounds nodes and edges and refuses to manufacture unnamed hardware or network relationships. Rendered labels should match user-defined architecture.

## General text-to-image

The image workflow is a genuine adapter to **local ComfyUI**, not an image-generator built into the native analysis engine. Generation requires: a live local ComfyUI instance, a compatible diffusion checkpoint selected by filename, usable hardware and a well-defined prompt. The returned image is decoded, validated and written to a real PNG.

For a request such as “A cat skateboarding with the I2PS logo on its shirt,” the exact company logo must be supplied. Logo positioning requires visual inspection and approval. The LogicaSophia product identity artwork is **not interchangeable** with the I2PS company logo.

No pre-rendered mockup, manually drawn example or borrowed artwork may be labeled as a successfully generated model output.

## Reporting and audit

Engineering exports have task parameters, identified source data, output filenames, and SHA-256 digests recorded. The evidence proves which bytes entered and left a task, not the correctness of inferred engineering conclusions.

Current limitation: real ComfyUI image inference was **not** exercised on the user's Ubuntu i5 during v0.7.0 local tests. A production-grade visual design/report validator and broad engineering reasoning remain separate work.
