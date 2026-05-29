from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY:str
    PINECONE_INDEX_NAME:str
    PINECONE_API_KEY:str
    PINECONE_HOST:str
    SUPABASE_URL:str
    SUPABASE_KEY:str
    GITHUB_BASE_URL:str
    STREAM_DELAY:str
    # Health-check keep-alive (dummy Supabase user row id)
    DUMMY_HEALTH_CHECK_BOT_ID:str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()  # type: ignore