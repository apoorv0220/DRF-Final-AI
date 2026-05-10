# Q3 — Prompts

- [classification_system.md](classification_system.md) — system prompt for **Hot / Warm / Cold** classification (JSON output).
- [response_system.md](response_system.md) — system prompt for **personalized first response** (JSON output).

See [OUTPUT_QUALITY.md](OUTPUT_QUALITY.md) for how we keep outputs **non-generic**, **grounded**, and **context-aware**.

The Q2 API loads these files at runtime via `varynt_api.prompt_loader`.
