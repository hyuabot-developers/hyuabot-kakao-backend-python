import os

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    API_HOST: str = Field(os.environ.get("API_HOST", "localhost"))
    API_PORT: int = Field(os.environ.get("API_PORT", 8080))
