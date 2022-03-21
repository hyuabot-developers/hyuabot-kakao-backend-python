from datetime import datetime

import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao.core.config import AppSettings, korea_standard_time
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

reading_room_router = APIRouter(prefix="/room", tags=["Reading room by campus"])


async def fetch_reading_room_list() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/library/erica"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            return response_json


@reading_room_router.post("")
async def campus(_: KakaoRequest) -> ServerResponse:
    reading_room_list = sorted(await fetch_reading_room_list(), key=lambda x: x["name"])
    card_list: list[TextCard] = []

    for reading_room_item in reading_room_list:
        reading_room_name: str = reading_room_item["name"]
        reading_room_active: bool = reading_room_item["isActive"]
        reading_room_total: int = reading_room_item["total"]
        reading_room_total_active: int = reading_room_item["activeTotal"]
        reading_room_occupied: int = reading_room_item["occupied"]
        reading_room_available: int = reading_room_item["available"]

        title = reading_room_name
        if reading_room_active:
            title += "/사용 가능"
        else:
            title += "/사용 불가"

        description = f"전체 죄석: {reading_room_total}석\n"
        description += f"전체 죄석(사용 가능): {reading_room_total_active}석\n"
        description += f"사용 중: {reading_room_occupied}석\n"
        description += f"예약 가능: {reading_room_available}석\n"

        card_list.append(TextCard(
            title=title, description=description.strip(), buttons=[],
        ))

    return create_carousel_response(card_list, [])
