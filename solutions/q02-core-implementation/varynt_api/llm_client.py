from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Literal

from openai import APIStatusError, APITimeoutError, OpenAI, RateLimitError

from varynt_api.config import OPENAI_CHAT_MODEL, get_settings
from varynt_api.schemas import ClassificationResult, ResponseResult


class LLMClient(ABC):
    mode: Literal["live", "mock"]

    @abstractmethod
    def classify(self, system: str, user: str) -> ClassificationResult: ...

    @abstractmethod
    def generate_reply(self, system: str, user: str) -> ResponseResult: ...


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("Model did not return parseable JSON.")
    return json.loads(match.group(0))


class OpenAILLMClient(LLMClient):
    mode: Literal["live", "mock"] = "live"

    def __init__(self) -> None:
        settings = get_settings()
        self._client = OpenAI(
            api_key=settings.openai_api_key.strip(),
            timeout=settings.request_timeout_seconds,
        )

    def _chat_json(self, system: str, user: str, max_completion_tokens: int) -> dict[str, Any]:
        completion = self._client.chat.completions.create(
            model=OPENAI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_completion_tokens=max_completion_tokens,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        content = completion.choices[0].message.content or ""
        return _extract_json_object(content)

    def classify(self, system: str, user: str) -> ClassificationResult:
        data = self._chat_json(system, user, max_completion_tokens=400)
        return ClassificationResult.model_validate(data)

    def generate_reply(self, system: str, user: str) -> ResponseResult:
        data = self._chat_json(system, user, max_completion_tokens=700)
        message = data.get("message")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Model JSON missing non-empty 'message' string.")
        subject = data.get("subject_line")
        subject_line = subject.strip() if isinstance(subject, str) and subject.strip() else None
        return ResponseResult(message=message.strip(), subject_line=subject_line)


class MockLLMClient(LLMClient):
    mode: Literal["live", "mock"] = "mock"

    def classify(self, system: str, user: str) -> ClassificationResult:
        text = user.lower()
        if any(k in text for k in ("enterprise", "pricing", "500 seats", "procurement", "po", "contract")):
            bucket = "hot"
            confidence = 0.78
            signals = ["explicit buying intent", "scale / enterprise language"]
        elif len(text.strip()) < 12 or text in ("test", "asdf", "hi"):
            bucket = "cold"
            confidence = 0.55
            signals = ["low information content"]
        else:
            bucket = "warm"
            confidence = 0.62
            signals = ["some interest but needs clarification"]
        return ClassificationResult(
            bucket=bucket,  # type: ignore[arg-type]
            confidence=confidence,
            signals=signals,
            reasoning="Heuristic mock classifier (no API call).",
        )

    def generate_reply(self, system: str, user: str) -> ResponseResult:
        return ResponseResult(
            message=(
                "Thanks for reaching out - I'd love to help. "
                "To point you to the right next step, what timeline are you working on, "
                "and what problem you're trying to solve first?"
            ),
            subject_line=None,
        )


def build_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.use_mock_llm:
        return MockLLMClient()
    return OpenAILLMClient()


__all__ = [
    "LLMClient",
    "OpenAILLMClient",
    "MockLLMClient",
    "build_llm_client",
    "APIStatusError",
    "APITimeoutError",
    "RateLimitError",
]
