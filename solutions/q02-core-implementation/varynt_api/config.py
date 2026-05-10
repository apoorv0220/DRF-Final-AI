from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

# Pinned in code (not env): changing this requires validating Chat Completions parameters.
OPENAI_CHAT_MODEL = "gpt-4o-mini"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    llm_mode: str = ""
    mock_llm: str = ""

    request_timeout_seconds: float = 45.0

    @property
    def use_mock_llm(self) -> bool:
        if self.llm_mode.strip().lower() == "mock":
            return True
        if self.mock_llm.strip() == "1":
            return True
        if not (self.openai_api_key or "").strip():
            return True
        return False


@lru_cache
def get_settings() -> Settings:
    return Settings()
