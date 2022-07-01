from typing import Any

import aiohttp as aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao import AppSettings
from app.hyuabot.kakao.core.create_response import create_carousel_response
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse, TextCard

subway_arrival_router = APIRouter(prefix="/arrival")
minute_to_arrival = {'당고개': 95.5, '상계': 93.5, '노원': 91.5,
                     '창동': 89.5, '쌍문': 87.0, '수유': 84.5, '미아': 82.5,
                     '미아사거리': 80.0, '길음': 77.5, '성신여대입구': 75.0, '한성대입구': 73.0, '혜화': 71.0,
                     '동대문': 68.5, '동대문역사문화공원': 67.0, '충무로': 64.5, '명동': 63.0, '회현': 61.5,
                     '서울': 59.5, '숙대입구': 57.5, '삼각지': 55.5, '신용산': 54.0, '이촌': 51.5,
                     '동작': 48.0, '총신대입구(이수)': 45.0, '사당': 43.0, '남태령': 40.5, '선바위': 37.5,
                     '경마공원': 35.5, '대공원': 33.5, '과천': 31.5, '정부과천청사': 29.5, '인덕원': 26.0,
                     '평촌': 23.5, '범계': 21.5, '금정': 18.0, '산본': 13.5, '수리산': 11.5, '대야미': 8.0,
                     '반월': 5.5, '상록수': 2.0, '한대앞': 0.0, '중앙': 2.5, '고잔': 4.5, '초지': 7.0,
                     '안산': 9.5, '신길온천': 13.0, '정왕': 16.0, '오이도': 19.0, '신포': 47.0, '숭의': 44.5,
                     '인하대': 42.0, '송도': 39.5, '연수': 36.0, '원인재': 34.0, '남동인더스파크': 32.0,
                     '호구포': 30.0, '인천논현': 28.0, '소래포구': 26.0, '월곶': 24.0, '달월': 21.5,
                     '사리': 3.5, '야목': 8.5, '어천': 11.5, '오목천': 16.0, '고색': 18.5, '수원': 22.5,
                     '매교': 25.0, '수원시청': 27.5, '매탄권선': 30.5, '망포': 33.0, '영통': 35.5,
                     '청명': 37.5, '상갈': 41.0, '기흥': 43.5, '신갈': 46.0, '구성': 48.5, '보정': 51.0,
                     '죽전': 54.0, '오리': 57.5, '미금': 59.5, '정자': 62.0, '수내': 64.5, '서현': 66.5,
                     '이매': 68.5, '야탑': 71.0, '모란': 74.0, '태평': 76.0, '가천대': 78.0, '복정': 81.0,
                     '수서': 85.0, '대모산입구': 89.0, '개포동': 90.5, '구룡': 92.5, '도곡': 94.0,
                     '한티': 95.5, '선릉': 97.5, '선정릉': 99.5, '강남구청': 101.0, '로데오': 103.5,
                     '서울숲': 105.5, '왕십리': 109.0, '청량리': 118.0}


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
