import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao import AppSettings
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard, QuickReply

shuttle_arrival_router = APIRouter(prefix="/arrival")
heading_dict = {"DH": "직행", "DY": "직행", "C": "순환"}
quick_replies = [
    QuickReply(action="block", label="🏘️ 기숙사", messageText="🏘️ 기숙사",
               blockId="5ebf702e7a9c4b000105fb25"),
    QuickReply(action="block", label="🏫 셔틀콕", messageText="🏫 셔틀콕",
               blockId="5ebf702e7a9c4b000105fb25"),
    QuickReply(action="block", label="🚆 한대앞역", messageText="🚆 한대앞역",
               blockId="5ebf702e7a9c4b000105fb25"),
    QuickReply(action="block", label="🚍 예술인A", messageText="🚍 예술인A",
               blockId="5ebf702e7a9c4b000105fb25"),
    QuickReply(action="block", label="🏫 셔틀콕 건너편", messageText="🏫 셔틀콕 건너편",
               blockId="5ebf702e7a9c4b000105fb25"),
]

def create_shuttle_arrival_string(shuttle_arrival_list: list) -> str:
    description = ""
    if len(shuttle_arrival_list) >= 0:
        for shuttle_index, shuttle_item in enumerate(shuttle_arrival_list):
            hour, minute = shuttle_item["time"].split(":")
            description += f"{hour}시 {minute}분({heading_dict[shuttle_item['type']]})\n"
            if shuttle_index >= 3:
                break
        return description.strip()
    else:
        return "도착 예정인 셔틀이 없습니다."


@shuttle_arrival_router.post("")
async def arrival(_: KakaoRequest) -> ServerResponse:
    shuttle_arrival_list = await fetch_shuttle_arrival()
    card_list: list[TextCard] = []

    for shuttle_arrival_item in shuttle_arrival_list:
        title = shuttle_arrival_item["stopName"]
        description = ""
        if title in ["기숙사", "셔틀콕"]:
            description = "한대앞 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForStation"])
            description += "\n\n예술인 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForTerminal"])
        elif title == "한대앞":
            description = "셔틀콕/기숙사 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForStation"])
            description += "\n\n예술인 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForTerminal"])
        elif title == "예술인A":
            description = "셔틀콕/기숙사 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForTerminal"])
        elif title == "셔틀콕 건너편":
            description = "\n\n기숙사 방면\n"
            description += create_shuttle_arrival_string(shuttle_arrival_item["busForTerminal"])

        card_list.append(TextCard(
            title=title, description=description, buttons=[],
        ))

    return create_carousel_response(card_list, quick_replies)


async def fetch_shuttle_arrival() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/shuttle/arrival"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            shuttle_arrival_list: list = response_json["arrivalList"]
            return shuttle_arrival_list
