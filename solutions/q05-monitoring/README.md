# Q5 — Monitoring

Practical observability for the lead qualification pipeline (proportionate to MVP → production).

## Logs (structured)

- **Correlation id** per request / job; log `lead_id`, `source`, `llm_mode` (live/mock), **model id**, latency per step (classify vs respond), token usage (if returned), outcome (success, fallback, error class).
- **Never log** full raw messages in production if policy requires redaction — log hashes or truncated excerpts.

## Metrics

- **Traffic:** requests/sec, queue depth (async), worker utilization.
- **Reliability:** error rate by class (4xx/5xx), OpenAI error rate, timeout rate, JSON validation failures.
- **Latency:** p50/p95 end-to-end; per-stage LLM latency.
- **Quality proxies:** distribution of Hot/Warm/Cold; rate of human overrides; spam reports.

## Traces

- Distributed traces spanning API → DB write → LLM calls → CRM sync for debugging slow requests.

## Alerts

- **SLO burn:** p95 latency or error budget thresholds.
- **Provider issues:** spike in 429/5xx from OpenAI.
- **Data quality:** sudden shift in bucket distribution (possible prompt regression or traffic source change).
- **Business:** drop in qualified leads created vs submissions (funnel break).

## Dashboards

- One **operations** dashboard (health, errors, latency) and one **product** dashboard (volumes, buckets, conversion placeholders).

## Tests in CI

- **Mock mode** runs without API keys; smoke test `/health` and `/v1/qualify` with golden inputs.
