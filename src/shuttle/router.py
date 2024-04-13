import datetime

from fastapi import APIRouter
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pytz import timezone

from config import settings
from schema.payload import Payload
from schema.response import CarouselResponse
from utils import calculate_remaining_minutes

router = APIRouter()


@router.post("", response_model=CarouselResponse, tags=["shuttle"])
async def get_shuttle(_: Payload):
    current_time = datetime.datetime.now(tz=timezone("Asia/Seoul")).time()
    current_time_str = current_time.strftime("%H:%M")
    transport = AIOHTTPTransport(url=f"{settings.API_URL}/query")
    query = gql(
        f"""
            query {{
                shuttle (start: \"{current_time_str}\") {{
                    timetable {{ tag, route, time, stop }}
            }}
        }}
        """,
    )
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(query)
        timetable = result["shuttle"]["timetable"]
        dormitory_out_station = list(
            filter(
                lambda x: (
                    x["stop"] == "dormitory_o" and (x["tag"] == "DH" or x["tag"] == "DJ" or x["tag"] == "C")
                ), timetable,
            ),
        )
        dormitory_out_terminal = list(
            filter(
                lambda x: (
                    x["stop"] == "dormitory_o" and (x["tag"] == "DY" or x["tag"] == "C")
                ), timetable,
            ),
        )
        dormitory_out_jungang_station = list(
            filter(
                lambda x: (
                    x["stop"] == "dormitory_o" and x["tag"] == "DJ"
                ), timetable,
            ),
        )
        shuttlecock_out_station = list(
            filter(
                lambda x: (
                    x["stop"] == "shuttlecock_o" and (x["tag"] == "DH" or x["tag"] == "DJ" or x["tag"] == "C")
                ), timetable,
            ),
        )
        shuttlecock_out_terminal = list(
            filter(
                lambda x: (
                    x["stop"] == "shuttlecock_o" and (x["tag"] == "DY" or x["tag"] == "C")
                ), timetable,
            ),
        )
        shuttlecock_out_jungang_station = list(
            filter(
                lambda x: (
                    x["stop"] == "shuttlecock_o" and x["tag"] == "DJ"
                ), timetable,
            ),
        )
        station_to_campus = list(filter(lambda x: x["stop"] == "station", timetable))
        station_to_terminal = list(filter(lambda x: x["stop"] == "station" and x["tag"] == "C", timetable))
        station_to_jungang = list(filter(lambda x: x["stop"] == "station" and x["tag"] == "DJ", timetable))
        terminal_to_campus = list(filter(lambda x: x["stop"] == "terminal", timetable))
        jungang_to_campus = list(filter(lambda x: x["stop"] == "jungang_stn", timetable))
        shuttlecock_in_dormitory = list(
            filter(
                lambda x: (
                    x["stop"] == "shuttlecock_i" and str(x["route"]).endswith("D")
                ), timetable,
            ),
        )

        # 기숙사 출발 카드
        dormitory_out_card_title = "기숙사"
        dormitory_out_card_contents = "한대앞 행\n"
        if len(dormitory_out_station) > 0:
            for index, shuttle in enumerate(dormitory_out_station):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                dormitory_out_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            dormitory_out_card_contents += "운행 종료\n"

        dormitory_out_card_contents += "\n예술인 행\n"
        if len(dormitory_out_terminal) > 0:
            for index, shuttle in enumerate(dormitory_out_terminal):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                tag = "직행" if shuttle["tag"] == "DY" else "순환"
                dormitory_out_card_contents += f"{tag} {departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            dormitory_out_card_contents += "운행 종료\n"

        dormitory_out_card_contents += "\n중앙역 행\n"
        if len(dormitory_out_jungang_station) > 0:
            for index, shuttle in enumerate(dormitory_out_jungang_station):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                dormitory_out_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            dormitory_out_card_contents += "운행 종료\n"

        # 셔틀콕 출발 카드
        shuttlecock_out_card_title = "셔틀콕"
        shuttlecock_out_card_contents = "한대앞 행\n"
        if len(shuttlecock_out_station) > 0:
            for index, shuttle in enumerate(shuttlecock_out_station):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                shuttlecock_out_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            shuttlecock_out_card_contents += "운행 종료\n"

        shuttlecock_out_card_contents += "\n예술인 행\n"
        if len(shuttlecock_out_terminal) > 0:
            for index, shuttle in enumerate(shuttlecock_out_terminal):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                tag = "직행" if shuttle["tag"] == "DY" else "순환"
                shuttlecock_out_card_contents += (f"{tag} "
                                                  f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n")
        else:
            shuttlecock_out_card_contents += "운행 종료\n"

        shuttlecock_out_card_contents += "\n중앙역 행\n"
        if len(shuttlecock_out_jungang_station) > 0:
            for index, shuttle in enumerate(shuttlecock_out_jungang_station):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                shuttlecock_out_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            shuttlecock_out_card_contents += "운행 종료\n"

        # 한대앞 출발 카드
        station_to_campus_card_title = "한대앞"
        station_to_campus_card_contents = "캠퍼스 행\n"
        if len(station_to_campus) > 0:
            for index, shuttle in enumerate(station_to_campus):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                station_to_campus_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            station_to_campus_card_contents += "운행 종료\n"

        station_to_campus_card_contents += "\n터미널 행\n"
        if len(station_to_terminal) > 0:
            for index, shuttle in enumerate(station_to_terminal):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                station_to_campus_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            station_to_campus_card_contents += "운행 종료\n"

        station_to_campus_card_contents += "\n중앙역 행\n"
        if len(station_to_jungang) > 0:
            for index, shuttle in enumerate(station_to_jungang):
                if index > 1:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                station_to_campus_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            station_to_campus_card_contents += "운행 종료\n"

        # 터미널 출발 카드
        terminal_to_campus_card_title = "터미널"
        terminal_to_campus_card_contents = "캠퍼스 행\n"
        if len(terminal_to_campus) > 0:
            for index, shuttle in enumerate(terminal_to_campus):
                if index > 5:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                terminal_to_campus_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            terminal_to_campus_card_contents += "운행 종료\n"

        # 중앙역 출발 카드
        jungang_to_campus_card_title = "중앙역"
        jungang_to_campus_card_contents = "캠퍼스 행\n"
        if len(jungang_to_campus) > 0:
            for index, shuttle in enumerate(jungang_to_campus):
                if index > 5:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                jungang_to_campus_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            jungang_to_campus_card_contents += "운행 종료\n"

        # 셔틀콕 건너편 출발 카드
        shuttlecock_in_card_title = "셔틀콕 건너편"
        shuttlecock_in_card_contents = "기숙사 행\n"
        if len(shuttlecock_in_dormitory) > 0:
            for index, shuttle in enumerate(shuttlecock_in_dormitory):
                if index > 5:
                    break
                departure_time = datetime.datetime.strptime(shuttle["time"], "%H:%M:%S").time()
                remaining_time = calculate_remaining_minutes(departure_time, current_time)
                shuttlecock_in_card_contents += f"{departure_time.strftime('%H:%M')} 출발 ({remaining_time}분 후)\n"
        else:
            shuttlecock_in_card_contents += "운행 종료\n"

        dormitory_out_card = {
            "title": dormitory_out_card_title,
            "description": dormitory_out_card_contents.strip(),
        }
        shuttlecock_out_card = {
            "title": shuttlecock_out_card_title,
            "description": shuttlecock_out_card_contents.strip(),
        }
        station_to_campus_card = {
            "title": station_to_campus_card_title,
            "description": station_to_campus_card_contents.strip(),
        }
        terminal_to_campus_card = {
            "title": terminal_to_campus_card_title,
            "description": terminal_to_campus_card_contents.strip(),
        }
        jungang_to_campus_card = {
            "title": jungang_to_campus_card_title,
            "description": jungang_to_campus_card_contents.strip(),
        }
        shuttlecock_in_card = {
            "title": shuttlecock_in_card_title,
            "description": shuttlecock_in_card_contents.strip(),
        }
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
                            "items": [
                                dormitory_out_card,
                                shuttlecock_out_card,
                                station_to_campus_card,
                                terminal_to_campus_card,
                                jungang_to_campus_card,
                                shuttlecock_in_card,
                            ],
                        },
                    },
                ],
            },
        }
