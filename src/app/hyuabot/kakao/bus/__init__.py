from fastapi import APIRouter

from app.hyuabot.kakao.bus.arrival import bus_arrival_router

bus_router = APIRouter(prefix="/bus")
bus_router.include_router(bus_arrival_router, tags=["bus arrival"])
