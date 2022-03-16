__version__ = "1.0.0-alpha1"

from fastapi import FastAPI

from app.hyuabot.kakao.core.config import AppSettings
from app.hyuabot.kakao.shuttle import shuttle_router


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()
    app.extra["settings"] = app_settings

    app.include_router(shuttle_router)
    return app
