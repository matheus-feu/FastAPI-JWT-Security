from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(getenv(".env"))


class Settings(BaseSettings):
    """Configurações do projeto"""
    # Base
    app_version: str
    app_v1_prefix: str
    debug: bool
    project_name: str
    project_description: str

    # Database
    postgres_uri: str

    # Security
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """O uso @lru_cache() permite evitar a leitura repetida do arquivo dotenv para cada solicitação,
    enquanto permite que você o substitua durante o teste."""
    return Settings()


settings: Settings = get_settings()
