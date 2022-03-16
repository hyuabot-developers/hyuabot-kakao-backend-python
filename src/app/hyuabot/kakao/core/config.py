import os

from pydantic import AnyUrl, BaseSettings, Field


class AppSettings(BaseSettings):
    API_URL: AnyUrl = Field(os.environ.get("API_URL", "http://localhost:8080"))
