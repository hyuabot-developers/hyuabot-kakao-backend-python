from datetime import datetime

import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao.core.config import AppSettings, korea_standard_time
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

bus_arrival_router = APIRouter(prefix="/arrival")
start_stop_dict = {"10-1": "대우푸르지오6차후문", "707-1": "신안산대", "3102": "새솔고"}


async def fetch_bus_arrival() -> list:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/bus/arrival"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            bus_arrival_list: list = response_json["departureInfoList"]
            return bus_arrival_list


@bus_arrival_router.post("")
async def arrival(_: KakaoRequest) -> ServerResponse:
    bus_arrival_list = await fetch_bus_arrival()
    card_list: list[TextCard] = []

    weekday = datetime.now(tz=korea_standard_time).weekday()
    if weekday < 5:
        weekday_key = "weekdays"
    elif weekday == 6:
        weekday_key = "saturday"
    else:
        weekday_key = "sunday"

    for bus_arrival_item in bus_arrival_list:
        route_name = bus_arrival_item["name"]
        bus_stop_name = bus_arrival_item["busStop"]
        bus_arrival_realtime_list = bus_arrival_item["realtime"]
        bus_arrival_timetable_list = []
        for bus_arrival_timetable_item in bus_arrival_item["timetable"][weekday_key]:
            bus_arrival_time = datetime.strptime(bus_arrival_timetable_item, "%H:%M:%S")\
                .replace(tzinfo=korea_standard_time)
            if bus_arrival_time > datetime.now(tz=korea_standard_time):
                bus_arrival_timetable_list.append(bus_arrival_time)
            if len(bus_arrival_timetable_list) == 3:
                break

        title = f"{route_name} ({bus_stop_name})"
        description = "실시간 도착 정보\n"

        if bus_arrival_realtime_list:
            for bus_arrival_realtime in bus_arrival_realtime_list:
                remained_stop_count = bus_arrival_realtime["location"]
                remained_time = bus_arrival_realtime["remainedTime"]
                remained_seat = bus_arrival_realtime["remainedSeat"]
                description += f"{remained_stop_count}전/ {remained_time}분 후 도착({remained_seat}석)\n"
        else:
            description += "운행 중인 버스가 없습니다.\n"

        description += f"\n시점({start_stop_dict[route_name]}) 츌벌 시간표\n"
        if bus_arrival_timetable_list:
            for bus_arrival_timetable in bus_arrival_timetable_list:
                description += f"{bus_arrival_timetable.strftime('%H시 %M분')}\n"
        else:
            description += "운행이 종료되었습니다\n막차: " \
                           f"{bus_arrival_item['timetable'][weekday_key][-1][:5].replace(':', '시 ')}분\n"
        card_list.append(TextCard(
            title=title, description=description, buttons=[],
        ))

    return create_carousel_response(card_list, [])
