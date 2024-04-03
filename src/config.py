from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    SITE_DOMAIN: str
    ENVIRONMENT: Environment = Environment.PRODUCTION
    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    API_URL: str
    APP_VERSION: str = "1.0.0"


settings = Config()
app_configs: dict[str, Any] = {
    "title": "HYUabot Kakao API",
    "version": settings.APP_VERSION,
}

if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = "/api/v1"

if not settings.ENVIRONMENT.is_debug:
    app_configs["docs_url"] = None
    app_configs["redoc_url"] = None
    app_configs["openapi_url"] = None
