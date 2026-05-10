from typing import Literal

from pydantic import BaseModel, Field


class LeadIn(BaseModel):
    source: Literal["form", "chat"] = Field(description="Where the lead came from.")
    message: str = Field(min_length=1, description="Free-text lead message or form notes.")
    email: str | None = None
    company: str | None = None
    name: str | None = None


class ClassificationResult(BaseModel):
    bucket: Literal["hot", "warm", "cold"]
    confidence: float = Field(ge=0.0, le=1.0)
    signals: list[str] = Field(default_factory=list)
    reasoning: str = ""


class ResponseResult(BaseModel):
    message: str
    subject_line: str | None = None


class QualifyResponse(BaseModel):
    classification: ClassificationResult
    response: ResponseResult
    llm_mode: Literal["live", "mock"]
