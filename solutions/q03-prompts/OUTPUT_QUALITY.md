# Output quality — not generic, not hallucinated, context-aware

## Not generic

- **Structured outputs:** Both steps request **JSON only** with a fixed schema, which reduces rambling and template-y filler.
- **Prompt constraints:** The response prompt sets length bounds and requires **one** concrete next step tied to the lead text.
- **Classification gates tone:** Hot leads get a more direct CTA; cold/garbage gets a polite, lightweight reply (handled in code + Q4), avoiding “enterprise polish” on junk.

## Not hallucinated (grounding)

- **Explicit anti-fabrication rules** in prompts: no features, pricing, certifications, or integrations unless supplied in the lead payload.
- **Validation:** Pydantic validates model JSON for classification; the reply step must include a non-empty `message` string or the API errors (live path).
- **Pinned model + parameters:** A single OpenAI model (`gpt-4o-mini`) and fixed Chat Completions parameters reduce surprise API behavior while we tune prompts.

## Context-aware

- The user payload includes **source** (`form` vs `chat`), **message**, and optional **email / company / name** so the model can mirror what the lead actually said.
- The response step receives the **classification JSON** so the next step matches **hot vs warm vs cold** (e.g., stronger scheduling ask only when justified).

## Operational note

For production, add offline **golden-set regression tests** on prompts (expected JSON shape + rubric scoring) and optional **human review** for edge buckets.
