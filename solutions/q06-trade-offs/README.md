# Q6 — Trade-offs

Design choices for the VARYNT MVP vs a fuller enterprise build.

## Sync pipeline first (Q2) vs async everywhere

- **Chosen:** synchronous **classify → respond** in one API for clarity and fast demos.
- **Trade-off:** under burst traffic, tail latency and OpenAI rate limits hurt more than with queued workers; production adds a queue (Q1).

## Single pinned OpenAI model

- **Chosen:** `gpt-4o-mini` hardcoded with fixed Chat Completions parameters.
- **Trade-off:** no per-tenant model selection without code changes; avoids parameter mismatch bugs across model generations.

## LLM-centric classification vs hybrid rules

- **Chosen:** LLM-first classifier with conservative prompt rules.
- **Trade-off:** higher variable cost and occasional inconsistency vs a rules engine; rules can be added later for obvious spam.

## JSON-only outputs

- **Chosen:** `response_format: json_object` + Pydantic validation.
- **Trade-off:** stricter failures when the model drifts; mitigated by retries/repair prompts and templates.

## Minimal CRM / DB in Q2

- **Chosen:** Q2 omits persistence to keep scope small.
- **Trade-off:** no audit trail or SDR workflow in the demo API; architecture (Q1) specifies where DB/CRM fit.

## Mock mode default without API key

- **Chosen:** safe local/CI runs with deterministic stub logic.
- **Trade-off:** mock behavior does not reflect model quality — must run **live** for realistic evals.

## Personalization depth

- **Chosen:** one-turn personalized reply using lead text + classification only.
- **Trade-off:** no RAG over docs/pricing; reduces hallucination risk but limits depth — explicit allowlisted snippets would be the next step.
