from copy import deepcopy

import aiohttp
from fastapi import APIRouter

from app.hyuabot.kakao.core.config import AppSettings
from app.hyuabot.kakao.core.create_response import create_basic_card_response
from app.hyuabot.kakao.core.parse_input import parse_user_utterance
from app.hyuabot.kakao.scheme.request import KakaoRequest
from app.hyuabot.kakao.scheme.response import ServerResponse

from .arrival import heading_dict, quick_replies

shuttle_stop_router = APIRouter(prefix="/stop")
shuttle_stop_dict = {"기숙사": "Dormitory", "셔틀콕": "Shuttlecock_O", "한대앞역": "Station",
                     "예술인A": "Terminal", "셔틀콕 건너편": "Shuttlecock_I"}


async def fetch_shuttle_timetable(shuttle_stop_id: str) -> tuple[str, list, list]:
    app_settings = AppSettings()
    url = f"http://{app_settings.API_HOST}:{app_settings.API_PORT}" \
          f"/api/v1/shuttle/arrival/{shuttle_stop_id}/timetable"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            shuttle_stop_name = response_json["stopName"]
            shuttle_for_station = response_json["busForStation"]
            shuttle_for_terminal = response_json["busForTerminal"]
            return shuttle_stop_name, shuttle_for_station, shuttle_for_terminal


@shuttle_stop_router.post("")
async def arrival(user_input: KakaoRequest) -> ServerResponse:
    shuttle_stop = parse_user_utterance(user_input)[2:].strip()

    shuttle_stop_name, shuttle_for_station, shuttle_for_terminal = \
        await fetch_shuttle_timetable(shuttle_stop_dict[shuttle_stop])

    title = shuttle_stop_name
    description = ""
    item_to_remove = -1

    if shuttle_stop == "기숙사":
        item_to_remove = 0
        description += "위치: 행복관 옆 축구장 앞\n"

        description += "\n한대앞 방면\n"
        description += f"첫차: {shuttle_for_station[0]['time']}" \
                       f"({heading_dict[shuttle_for_station[0]['type']]})\n"
        description += f"막차: {shuttle_for_station[-1]['time']}" \
                       f"({heading_dict[shuttle_for_station[-1]['type']]})\n"

        description += "\n예술인 방면\n"
        description += f"첫차: {shuttle_for_terminal[0]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[0]['type']]})\n"
        description += f"막차: {shuttle_for_terminal[-1]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[-1]['type']]})"
    elif shuttle_stop == "셔틀콕":
        item_to_remove = 1
        description += "위치: 제2과학기술관 건너편\n"

        description += "\n한대앞 방면\n"
        description += f"첫차: {shuttle_for_station[0]['time']}" \
                       f"({heading_dict[shuttle_for_station[0]['type']]})\n"
        description += f"막차: {shuttle_for_station[-1]['time']}" \
                       f"({heading_dict[shuttle_for_station[-1]['type']]})\n"

        description += "\n예술인 방면\n"
        description += f"첫차: {shuttle_for_terminal[0]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[0]['type']]})\n"
        description += f"막차: {shuttle_for_terminal[-1]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[-1]['type']]})"
    elif shuttle_stop == "한대앞역":
        item_to_remove = 2
        description += "위치: 한대앞역 2번 출구에서 좌측 전방\n"

        description += "\n셔틀콕/기숙사 방면\n"
        description += f"첫차: {shuttle_for_station[0]['time']}" \
                       f"({heading_dict[shuttle_for_station[0]['type']]})\n"
        description += f"막차: {shuttle_for_station[-1]['time']}" \
                       f"({heading_dict[shuttle_for_station[-1]['type']]})\n"

        description += "\n예술인 방면\n"
        description += f"첫차: {shuttle_for_terminal[0]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[0]['type']]})\n"
        description += f"막차: {shuttle_for_terminal[-1]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[-1]['type']]})"
    elif shuttle_stop == "예술인A":
        item_to_remove = 3
        description += "위치: 안산파크푸르지오 정류장(17471)\n"

        description += "\n셔틀콕/기숙사 방면\n"
        description += f"첫차: {shuttle_for_terminal[0]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[0]['type']]})\n"
        description += f"막차: {shuttle_for_terminal[-1]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[-1]['type']]})"
    elif shuttle_stop == "셔틀콕 건너편":
        item_to_remove = 4
        description += "위치: 제2과학기술관 앞\n"

        description += "\n기숙사 방면\n"
        description += f"첫차: {shuttle_for_terminal[0]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[0]['type']]})\n"
        description += f"막차: {shuttle_for_terminal[-1]['time']}" \
                       f"({heading_dict[shuttle_for_terminal[-1]['type']]})"
    quick_replies_list = deepcopy(quick_replies)
    quick_replies_list.remove(quick_replies[item_to_remove])
    return create_basic_card_response(title, description, [], quick_replies_list)
