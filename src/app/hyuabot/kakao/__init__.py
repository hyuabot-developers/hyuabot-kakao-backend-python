__version__ = "1.0.0-alpha1"

from fastapi import FastAPI

from app.hyuabot.kakao.bus import bus_router
from app.hyuabot.kakao.core.config import AppSettings
from app.hyuabot.kakao.shuttle import shuttle_router
from app.hyuabot.kakao.subway import subway_router


def create_app(app_settings: AppSettings) -> FastAPI:
    app = FastAPI()
    app.extra["settings"] = app_settings

    app.include_router(shuttle_router)
    app.include_router(bus_router)
    app.include_router(subway_router)
    return app
