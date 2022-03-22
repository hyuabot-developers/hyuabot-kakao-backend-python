from datetime import datetime

import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao.core.config import AppSettings, korea_standard_time
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard, QuickReply

food_campus_router = APIRouter(prefix="/campus", tags=["Restaurant menu by campus"])
quick_replies = [
    QuickReply(action="block", label="학생식당", messageText="학생식당",
               blockId="5cc3f00d384c5508fceec588"),
    QuickReply(action="block", label="교직원식당", messageText="교직원식당",
               blockId="5cc3f00d384c5508fceec588"),
    QuickReply(action="block", label="창의인재원식당", messageText="창의인재원식당",
               blockId="5cc3f00d384c5508fceec588"),
    QuickReply(action="block", label="푸드코트", messageText="푸드코트",
               blockId="5cc3f00d384c5508fceec588"),
    QuickReply(action="block", label="창업보육센터", messageText="창업보육센터",
               blockId="5cc3f00d384c5508fceec588"),
]


async def fetch_menu_list_by_campus() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/food/campus/erica"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            return response_json["restaurantList"]


@food_campus_router.post("")
async def campus(_: KakaoRequest) -> ServerResponse:
    restaurant_list = sorted(await fetch_menu_list_by_campus(), key=lambda x: x["name"])
    card_list: list[TextCard] = []
    now = datetime.now(tz=korea_standard_time)

    for restaurant_item in restaurant_list:
        restaurant_name: str = restaurant_item["name"]
        restaurant_menu_list: dict = restaurant_item["menuList"]

        if list(restaurant_menu_list.keys()):
            restaurant_key = "중식"
            if now.hour < 9 and restaurant_menu_list.keys():
                restaurant_key = "조식"
            elif now.hour >= 14 and restaurant_menu_list.keys():
                restaurant_key = "석식"
            if restaurant_key not in restaurant_menu_list.keys():
                restaurant_key = list(restaurant_menu_list.keys())[0]

            title = f"{restaurant_name}({restaurant_key})"
            description = ""
            for menu_item in restaurant_menu_list[restaurant_key]:
                description += f"{menu_item['menu']}\n"
                description += f"가격 - {menu_item['price']}\n"
        else:
            title = restaurant_name
            description = "제공되는 메뉴 없음"

        card_list.append(TextCard(
            title=title, description=description.strip(), buttons=[]
        ))

    return create_carousel_response(card_list, quick_replies)
