from typing import Any

import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao import AppSettings
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

subway_arrival_router = APIRouter(prefix="/arrival")
minute_to_arrival = {
    "한대앞": 0, "중앙": 2, "고잔": 4, "초지": 6.5, "안산": 9, "신길온천": 12.5, "정왕": 16, "오이도": 19,
    "달월": 21, "월곶": 23, "소래포구": 25, "인천논현": 27, "호구포": 29, "남동인더스파크": 31, "원인재": 33,
    "연수": 35, "송도": 38.5, "인하대": 41, "숭의": 42.5, "신포": 45, "인천": 46.5,
    "상록수": 2, "반월": 6, "대야미": 8.5, "수리산": 11.5, "산본": 13.5, "금정": 18,
    "범계": 21.5, "평촌": 23.5, "인덕원": 26, "정부과천청사": 28, "과천": 30,
    "사리": 2, "야목": 7, "어천": 10, "오목천": 14, "고색": 17, "수원": 21, "매교": 23, "수원시청": 26,
    "매탄권선": 29, "망포": 31.5, "영통": 34, "청명": 36, "상갈": 39, "기흥": 41.5, "신갈": 44, "구성": 46.5,
    "보정": 49, "죽전": 52, "오리": 55.5, "미금": 57.5, "정지": 60, "수내": 62.5, "서현": 64.5, "이매": 66.5
}


@subway_arrival_router.post("")
async def arrival(_: KakaoRequest) -> ServerResponse:
    station_name, subway_arrival_list = await fetch_subway_arrival()
    card_list: list[TextCard] = []

    for subway_arrival_item in subway_arrival_list:
        description = "상행\n"
        title = f"{subway_arrival_item['lineName']}({station_name})"
        if len(subway_arrival_item["realtime"]["up"]) >= 2:
            for item_index, realtime_item in enumerate(subway_arrival_item["realtime"]["up"]):
                description += f"{int(minute_to_arrival[realtime_item['currentStation']])} 분 후 도착" \
                               f"({realtime_item['terminalStation']}행)\n"
                if item_index == 1:
                    break
        elif subway_arrival_item["realtime"]["up"]:
            realtime_item = subway_arrival_item["realtime"]["up"][0]
            description += f"{int(minute_to_arrival[realtime_item['currentStation']])} 분 후 도착" \
                           f"({realtime_item['terminalStation']}행)\n"
        else:
            if len(subway_arrival_item["timetable"]["up"]) >= 2:
                for item_index, timetable_item in enumerate(subway_arrival_item["timetable"]["up"]):
                    description += f"{timetable_item['departureTime'][:5]}" \
                                   f"({timetable_item['terminalStation']}행)\n"
                    if item_index == 1:
                        break
            elif subway_arrival_item["timetable"]["up"]:
                timetable_item = subway_arrival_item["timetable"]["up"][0]
                description += f"{timetable_item['departureTime'][:5]}" \
                               f"({timetable_item['terminalStation']}행)\n"
            else:
                description += "도착 예정인 전철 정보 없음\n"

        description += "\n하행\n"
        if len(subway_arrival_item["realtime"]["down"]) >= 2:
            for item_index, realtime_item in enumerate(subway_arrival_item["realtime"]["down"]):
                description += f"{int(minute_to_arrival[realtime_item['currentStation']])} 분 후 도착" \
                               f"({realtime_item['terminalStation']}행)\n"
                if item_index == 1:
                    break
        elif subway_arrival_item["realtime"]["down"]:
            realtime_item = subway_arrival_item["realtime"]["down"][0]
            description += f"{int(minute_to_arrival[realtime_item['currentStation']])} 분 후 도착" \
                           f"({realtime_item['terminalStation']}행)\n"
        else:
            if len(subway_arrival_item["timetable"]["down"]) >= 2:
                for item_index, timetable_item in enumerate(subway_arrival_item["timetable"]["down"]):
                    description += f"{timetable_item['departureTime'][:5]}" \
                                   f"({timetable_item['terminalStation']}행)\n"
                    if item_index == 1:
                        break
            elif subway_arrival_item["timetable"]["down"]:
                timetable_item = subway_arrival_item["timetable"]["down"][0]
                description += f"{timetable_item['departureTime'][:5]}" \
                               f"({timetable_item['terminalStation']}행)\n"
            else:
                description += "도착 예정인 전철 정보 없음"

        card_list.append(TextCard(
            title=title, description=description, buttons=[],
        ))
    return create_carousel_response(card_list, [])


async def fetch_subway_arrival() -> tuple[Any, list]:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}/api/v1/subway/arrival/erica"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()

            station_name = response_json["stationName"]
            subway_arrival_list: list = response_json["departureList"]
            return station_name, subway_arrival_list
