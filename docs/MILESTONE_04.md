# Milestone 4 · Unified GUI + Qwen inference (v0.4.0)

## Delivered

- Approved gold-on-black LogicaSophia artwork displayed via a bundled 512px WebP rendering of the supplied original image; original artwork is not redesigned.
- Standard-library localhost dashboard at port 8766. Task submission, model selection, live state/decision/evidence trace, final answer and audit path.
- Existing original read-only agent remains responsible for all task execution; UI requests cannot invoke a shell or change files.
- Qwen3-1.7B Q4_K_M as the default **replaceable** initial model in USB launcher (SmolLM2 optional for comparison).
- Human-readable comprehensive README separating implemented capabilities from experimental research directions.
- Localhost model backend port 8090; JSON task API; origin and anti-CSRF token enforcement.

## Execution

```bash
bash LogicaSophia_Start_AI.txt
```

The script fetches dependencies and model weights on first run, then opens the UI on `http://127.0.0.1:8766`. It may request sudo for Ubuntu packages. Use `bash LogicaSophia_Start_AI.txt smol` for a comparison model; stop the previous server first.

The GUI workspace is selected at process startup through `--workspace`. Avoid storing audit results inside it. The project remains Linux-first and independent of Atlas Nexus.

## Acceptance tests

- GUI page and approved logo served from localhost, browser origin and task-token checks, oversize rejection, one-task concurrency rule.
- An HTTP-submitted task runs the existing model-agent tool loop (with a **deterministic model stub**) and writes verified audit files. Live model status comes from `/v1/models`.
- Existing file access constraints and offline smoke tests remain intact.
- The actual i5 CPU inference speed, Qwen response-format consistency and semantic answer correctness are **not yet field-qualified**.

## Limits

Version 0.4.0 does not provide general shell/OS autonomy, write tools, full semantic memory, multi-agent collaboration, remote clients or AGI. It is a real, model-backed engineering application with carefully bounded capabilities. Full intelligence ambitions are research milestones, not software feature claims.
