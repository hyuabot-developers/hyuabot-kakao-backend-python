import datetime

from fastapi import APIRouter
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pytz import timezone

from config import settings
from schema.payload import Payload
from schema.response import CarouselResponse

router = APIRouter()


@router.post("", response_model=CarouselResponse, tags=["subway"])
async def get_cafeteria(_: Payload):
    now = datetime.datetime.now(tz=timezone("Asia/Seoul"))
    today_str = now.strftime("%Y-%m-%d")
    type_ = "중식"
    if now.hour < 10:
        type_ = "조식"
    elif now.hour >= 14:
        type_ = "석식"
    transport = AIOHTTPTransport(url=f"{settings.API_URL}/query")
    query = gql(
        f"""
            query {{
                menu (date: \"{today_str}\", campusId: 2, type_: \"{type_}\") {{
                    id, name,
                    menu {{ menu, price }}
                }}
            }}
        """,
    )
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(query)
        cafeteria_list = result["menu"]
        cards = []
        for cafeteria in cafeteria_list:
            title = f"{cafeteria['name']} ({type_})"
            description = ""
            if len(cafeteria["menu"]) == 0:
                description = "오늘은 메뉴가 없어요!"
            for menu in cafeteria["menu"]:
                price = menu["price"] if str(menu["price"]).endswith("원") else f"{menu['price']}원"
                description += f"{menu['menu']}\n{price}\n"
            cards.append({
                "title": title,
                "description": description,
            })
    return {
        "version": "2.0",
        "template": {
            "quickReplies": [
                {
                    "label": "휴아봇 앱 설치",
                    "action": "block",
                    "messageText": "휴아봇 앱 설치",
                    "blockId": "6077ca2de2039a2ba38c755f",
                    "extra": {},
                },
            ],
            "outputs": [
                {
                    "carousel": {
                        "type": "textCard",
                        "items": cards,
                    },
                },
            ],
        },
    }
