from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from openai import APIStatusError, APITimeoutError, RateLimitError

from varynt_api.config import get_settings
from varynt_api.llm_client import build_llm_client
from varynt_api.pipeline import qualify_lead
from varynt_api.schemas import LeadIn, QualifyResponse

# Load sibling .env for local runs (q02-core-implementation/.env).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="VARYNT Lead Qualification (Q2)", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/v1/qualify",
    response_model=QualifyResponse,
    summary="Classify a lead and generate a first reply (live OpenAI or mock).",
)
def qualify(lead: LeadIn) -> JSONResponse:
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
    get_settings.cache_clear()
    llm = build_llm_client()
    try:
        result = qualify_lead(lead, llm)
    except (APIStatusError, RateLimitError, APITimeoutError) as exc:
        raise HTTPException(status_code=502, detail=f"Upstream LLM error: {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Model output error: {exc}") from exc

    return JSONResponse(
        content=jsonable_encoder(result),
        headers={"X-LLM-Mode": result.llm_mode},
    )
