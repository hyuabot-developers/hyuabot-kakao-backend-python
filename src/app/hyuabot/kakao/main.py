__version__ = "1.0.0-alpha1"

from fastapi import FastAPI

from app.hyuabot.api.core.config import AppSettings


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()
    app.extra["settings"] = app_settings
    return app
