"""Centralized configuration for the SEO optimizer service."""
import os
from dataclasses import dataclass   
from functools import lru_cache #for caching settings
from pathlib import Path

from dotenv import load_dotenv


#the project root and load .env explicitly
ROOT_DIR = Path(__file__).resolve().parents[2]
DOTENV_PATH = ROOT_DIR / ".env"
load_dotenv(DOTENV_PATH)


@dataclass(frozen=True)  #make settings immutable 
                        #immutable settings prevent accidental changes at runtime
class Settings:
    github_models_token: str | None = os.getenv("GITHUB_MODELS_TOKEN")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "10"))
    user_agent: str = os.getenv("USER_AGENT", "SEO-Optimizer/1.0")


@lru_cache(maxsize=1)  #maxsize=1 to cache a single instance
def get_settings() -> Settings:
    """return memoized settings instance.
    using a cached instance keeps configuration lookup cheap across requests.
    """

    return Settings()
