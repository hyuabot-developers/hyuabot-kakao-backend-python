from fastapi import APIRouter

from app.hyuabot.kakao.library.reading_room import reading_room_router

library_router = APIRouter(prefix="/library")
library_router.include_router(reading_room_router)
