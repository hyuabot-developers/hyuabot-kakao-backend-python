import os
from datetime import timezone, timedelta

from pydantic import BaseSettings, Field


korea_standard_time = timezone(timedelta(hours=9))


class AppSettings(BaseSettings):
    API_HOST: str = Field(os.environ.get("API_HOST", "localhost"))
    API_PORT: int = Field(os.environ.get("API_PORT", 8080))
