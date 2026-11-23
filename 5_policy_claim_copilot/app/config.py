import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Async Multimodal Policy & Claim Copilot"
    DEBUG: bool = True

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_URL: str = "http://localhost:6333"
    POLICY_COLLECTION_NAME: str = "policy_clauses"

    # Redis
    REDIS_URL: str = "redis://localhost:6381/0"

    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27018"
    MONGODB_DB_NAME: str = "claim_copilot"

    # API Keys
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
