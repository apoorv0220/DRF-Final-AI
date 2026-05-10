# VARYNT — AI lead qualification (solutions repo)

This repository is organized by **section (Q1–Q6)** with code, docs.

| Section | Topic | Location |
|---------|--------|----------|
| **Q1** | Architecture (input → LLM → storage → queue → fallbacks) | [solutions/q01-architecture/ARCHITECTURE.md](solutions/q01-architecture/ARCHITECTURE.md) |
| **Q2** | Core implementation: **FastAPI** + **classify → respond** pipeline | [solutions/q02-core-implementation/](solutions/q02-core-implementation/) |
| **Q3** | Classification + response prompts; output quality | [solutions/q03-prompts/](solutions/q03-prompts/) |
| **Q4** | Edge cases & failures | [solutions/q04-edge-cases-failures/README.md](solutions/q04-edge-cases-failures/README.md) |
| **Q5** | Monitoring | [solutions/q05-monitoring/README.md](solutions/q05-monitoring/README.md) |
| **Q6** | Trade-offs | [solutions/q06-trade-offs/README.md](solutions/q06-trade-offs/README.md) |

## Quick run (Q2 API)

```powershell
cd "G:\Projects\DRF Final AI"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy solutions\q02-core-implementation\.env.example solutions\q02-core-implementation\.env
cd solutions\q02-core-implementation
$env:PYTHONPATH = (Get-Location).Path
uvicorn varynt_api.main:app --reload --host 127.0.0.1 --port 8000
```

- **Live OpenAI:** set `OPENAI_API_KEY` in `solutions/q02-core-implementation/.env` (model pinned to `gpt-4o-mini` in code).
- **Mock:** leave the key empty, or set `LLM_MODE=mock` or `MOCK_LLM=1`. Response header: `X-LLM-Mode`.

Example request:

```powershell
curl -X POST http://127.0.0.1:8000/v1/qualify -H "Content-Type: application/json" -d "{\"source\":\"chat\",\"message\":\"We need enterprise pricing for 500 seats next quarter.\",\"company\":\"Contoso\"}"
```
## Loom Video
- [Watch an overview of the solutions](https://www.loom.com/share/e1ebc51fd7ac4dd1ac23efea3b58c2ee)