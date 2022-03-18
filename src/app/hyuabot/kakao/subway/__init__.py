from fastapi import APIRouter

from app.hyuabot.kakao.subway.arrival import subway_arrival_router

subway_router = APIRouter(prefix="/subway")
subway_router.include_router(subway_arrival_router)
