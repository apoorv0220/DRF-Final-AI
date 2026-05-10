from __future__ import annotations

import json

from varynt_api.llm_client import LLMClient
from varynt_api.prompt_loader import load_prompt
from varynt_api.schemas import LeadIn, QualifyResponse


def _classification_user_payload(lead: LeadIn) -> str:
    payload = {
        "source": lead.source,
        "message": lead.message,
        "email": lead.email,
        "company": lead.company,
        "name": lead.name,
    }
    return "Classify this lead. Lead JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=2)


def _response_user_payload(lead: LeadIn, classification: dict) -> str:
    payload = {
        "lead": {
            "source": lead.source,
            "message": lead.message,
            "email": lead.email,
            "company": lead.company,
            "name": lead.name,
        },
        "classification": classification,
    }
    return "Write the first reply. Context JSON:\n" + json.dumps(payload, ensure_ascii=False, indent=2)


def qualify_lead(lead: LeadIn, llm: LLMClient) -> QualifyResponse:
    classification_system = load_prompt("q03-prompts/classification_system.md")
    response_system = load_prompt("q03-prompts/response_system.md")

    classification = llm.classify(
        classification_system,
        _classification_user_payload(lead),
    )
    classification_dump = classification.model_dump()

    response = llm.generate_reply(
        response_system,
        _response_user_payload(lead, classification_dump),
    )

    return QualifyResponse(
        classification=classification,
        response=response,
        llm_mode=llm.mode,
    )
