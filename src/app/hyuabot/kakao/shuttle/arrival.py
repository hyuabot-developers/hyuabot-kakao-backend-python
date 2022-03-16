import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao import AppSettings
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

shuttle_arrival_router = APIRouter(prefix="/arrival")
heading_dict = {"DH": "직행", "DY": "직행", "C": "순환"}


@shuttle_arrival_router.post("")
async def arrival(_: KakaoRequest) -> ServerResponse:
    shuttle_arrival_list = await fetch_shuttle_arrival()
    card_list: list[TextCard] = []

    for shuttle_arrival_item in shuttle_arrival_list:
        title = shuttle_arrival_item["stopName"]
        description = ""
        if title in ["기숙사", "셔틀콕"]:
            description = "한대앞 방면\n"
            if len(shuttle_arrival_item["busForStation"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForStation"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."

            description += "예술인 방면\n"
            if len(shuttle_arrival_item["busForTerminal"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForTerminal"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."
        elif title == "한대앞":
            description = "셔틀콕/기숙사 방면\n"
            if len(shuttle_arrival_item["busForStation"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForStation"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."

            description += "예술인 방면\n"
            if len(shuttle_arrival_item["busForTerminal"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForTerminal"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."
        elif title == "예술인":
            description = "셔틀콕/기숙사 방면\n"
            if len(shuttle_arrival_item["busForTerminal"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForTerminal"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."
        elif title == "셔틀콕 건너편":
            description = "기숙사 방면\n"
            if len(shuttle_arrival_item["busForTerminal"]) > 0:
                for shuttle_index, shuttle_item in enumerate(shuttle_arrival_item["busForTerminal"]):
                    description += f"{shuttle_item['time']} ({heading_dict[shuttle_item['type']]})\n"
                    if shuttle_index >= 1:
                        break
            else:
                description += "도착 예정인 셔틀이 없습니다."
        card_list.append(TextCard(
            title=title, description=description, buttons=[],
        ))
    return create_carousel_response(card_list)


async def fetch_shuttle_arrival() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/shuttle/arrival"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            shuttle_arrival_list: list = response_json["arrivalList"]
            return shuttle_arrival_list
