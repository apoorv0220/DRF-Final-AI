# Q4 — Edge cases and failures

How the VARYNT design (and the Q2 API implementation) behaves when things go wrong.

## Low / garbage input

- **Detection:** very short messages, nonsense tokens, obvious spam patterns, or repeated characters.
- **Behavior:** classify **cold** (or **warm** if a human might still be there but unclear); reply is **short, polite, and asks one clarifying question** — no demo/pricing promises.
- **Q2 mock:** messages under ~12 chars or trivial tokens lean **cold**; live model follows classification prompt rules.

## Ambiguous leads

- **Detection:** real person but missing timeline, authority, scope, or product fit.
- **Behavior:** prefer **warm** over **hot**; response asks **targeted** questions (timeline, problem, team size) rather than inventing facts.
- **CRM:** tag as “needs qualification” for SDR follow-up.

## Model failure

- **Detection:** provider errors, malformed JSON after repair attempt, internal validation errors.
- **Behavior:** return **502/500** from API with safe detail in dev; in product UI, user sees generic “try again” while server logs correlation id.
- **Fallback:** after retries, send **templated** reply by last known bucket or neutral template + **alert** on-call for Hot leads.

## Timeout / API failure

- **Client timeout:** bounded OpenAI client timeout (Q2: `request_timeout_seconds`, default 45s).
- **Retries:** idempotent job id; exponential backoff for rate limits and transient 5xx; cap attempts.
- **User experience:** async path acknowledges receipt immediately; sync path may return 504 with guidance to retry once.

## Incorrect classification

- **Human override:** CRM field for SDR-corrected bucket; feed corrections into eval set (not auto-trained in MVP).
- **Confidence:** store `confidence` and `signals`; if confidence low, **downgrade** CTA strength in the reply (future rule layer).
- **A/B and monitoring:** track conversion by bucket and override rate (Q5).
