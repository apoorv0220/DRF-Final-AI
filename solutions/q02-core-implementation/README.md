# Q2 — Core implementation (API + AI pipeline)

This folder contains a **minimal FastAPI service** that implements the **input → classify → respond** slice of VARYNT.

## Pinned model

- **Provider:** OpenAI Chat Completions  
- **Model id (hardcoded):** `gpt-4o-mini`  
- **Credential:** `OPENAI_API_KEY` only (never commit real values)

Changing the model requires a **code change** so request parameters (e.g. `max_completion_tokens`) stay valid.

## LLM modes

| Mode | When |
|------|------|
| **live** | `OPENAI_API_KEY` is non-empty **and** `LLM_MODE` is not `mock` **and** `MOCK_LLM` is not `1` |
| **mock** | No key / empty key, **or** `LLM_MODE=mock`, **or** `MOCK_LLM=1` |

Responses include header `X-LLM-Mode: live | mock`.

## Setup

```powershell
cd "G:\Projects\DRF Final AI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy solutions\q02-core-implementation\.env.example solutions\q02-core-implementation\.env
# Edit .env: add OPENAI_API_KEY for live mode
```

## Run

```powershell
cd "G:\Projects\DRF Final AI"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "G:\Projects\DRF Final AI\solutions\q02-core-implementation"
uvicorn varynt_api.main:app --reload --host 0.0.0.0 --port 8000
```

Or from repo root with explicit app path:

```powershell
cd "G:\Projects\DRF Final AI\solutions\q02-core-implementation"
$env:PYTHONPATH = (Get-Location).Path
..\..\.venv\Scripts\uvicorn.exe varynt_api.main:app --reload --host 0.0.0.0 --port 8000
```

(Adjust `.venv` path if your venv lives elsewhere.)

## Try it

```powershell
curl -X POST http://127.0.0.1:8000/v1/qualify `
  -H "Content-Type: application/json" `
  -d "{\"source\":\"chat\",\"message\":\"We're evaluating vendors for 500 seats next quarter; can you share enterprise pricing?\",\"email\":\"alex@example.com\",\"company\":\"Contoso\"}"
```

Prompts loaded at runtime from [../q03-prompts/](../q03-prompts/).
