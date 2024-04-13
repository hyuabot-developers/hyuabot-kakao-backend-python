import datetime

from fastapi import APIRouter
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from pytz import timezone

from config import settings
from schema.payload import Payload
from schema.response import CarouselResponse

router = APIRouter()


def timetable_to_str(timetable: str) -> str:
    return timetable[:2] + "시 " + timetable[3:5] + "분"


def calculate_remaining_minutes(remaining_minutes: float, updated_at_str: str, now: datetime.datetime) -> float:
    updated_at = datetime.datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S%z")
    remaining_time = (remaining_minutes * 60) - (now - updated_at).total_seconds()
    return remaining_minutes if remaining_time > 0 else -1


def calculate_bigger_than_realtime(remaining_minutes: float, departure_time_str: str) -> bool:
    departure_time = timezone("Asia/Seoul").localize(
        datetime.datetime.combine(
            datetime.date.today(),
            datetime.datetime.strptime(departure_time_str, "%H:%M:%S").time(),
        ),
    )
    now = datetime.datetime.now(tz=timezone("Asia/Seoul"))
    return (departure_time - now).total_seconds() < (remaining_minutes + 3) * 60


@router.post("", response_model=CarouselResponse, tags=["subway"])
async def get_subway(_: Payload):
    current_time = datetime.datetime.now(tz=timezone("Asia/Seoul"))
    current_time_str = current_time.strftime("%H:%M")
    transport = AIOHTTPTransport(url=f"{settings.API_URL}/query")
    query = gql(
        f"""
            query {{
                subway (
                    id_: ["K251", "K449"],
                    start: "{current_time_str}",
                    weekdays: {str(current_time.weekday() < 5).lower()}
                ) {{
                    id,
                    realtime {{
                        up {{ location, stop, time, terminal {{ name }}, updatedAt }},
                        down {{ location, stop, time, terminal {{ name }}, updatedAt }},
                    }},
                    timetable {{
                        up {{ terminal {{ name }}, time }},
                        down {{ terminal {{ name }}, time }}
                    }}
                }}
            }}
        """,
    )
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(query)
        subway = result["subway"]
        line_yellow = list(filter(lambda x: x["id"] == "K251", subway))[0]
        line_blue = list(filter(lambda x: x["id"] == "K449", subway))[0]

        line_blue_up_arrival = []
        now = datetime.datetime.now(tz=timezone("Asia/Seoul"))
        for up in line_blue["realtime"]["up"]:
            remaining_minutes = calculate_remaining_minutes(up["time"], up["updatedAt"], now)
            if remaining_minutes < 0:
                continue
            line_blue_up_arrival.append(
                f"({up['terminal']['name']}) "
                f"{int(remaining_minutes)}분 후 도착 - {up['location']}",
            )
        for up in line_blue["timetable"]["up"]:
            if len(line_blue["realtime"]["up"]) > 0:
                if calculate_bigger_than_realtime(
                    calculate_remaining_minutes(
                        line_blue["realtime"]["up"][-1]["time"],
                        line_blue["realtime"]["up"][-1]["updatedAt"],
                        now,
                    ),
                    up["time"],
                ):
                    continue
            line_blue_up_arrival.append(f"({up['terminal']['name']}) {timetable_to_str(up['time'])} 출발")

        line_blue_down_arrival = []
        for down in line_blue["realtime"]["down"]:
            remaining_minutes = calculate_remaining_minutes(down["time"], down["updatedAt"], now)
            if remaining_minutes < 0:
                continue
            line_blue_down_arrival.append(
                f"({down['terminal']['name']}) "
                f"{int(remaining_minutes)}분 후 도착 - {down['location']}",
            )
        for down in line_blue["timetable"]["down"]:
            if len(line_blue["realtime"]["down"]) > 0:
                if calculate_bigger_than_realtime(
                    calculate_remaining_minutes(
                        line_blue["realtime"]["down"][-1]["time"],
                        line_blue["realtime"]["down"][-1]["updatedAt"],
                        now,
                    ),
                    down["time"],
                ):
                    continue
            line_blue_down_arrival.append(f"({down['terminal']['name']}) {timetable_to_str(down['time'])} 출발")

        line_yellow_up_arrival = []
        for up in line_yellow["realtime"]["up"]:
            remaining_minutes = calculate_remaining_minutes(up["time"], up["updatedAt"], now)
            if remaining_minutes < 0:
                continue
            line_yellow_up_arrival.append(
                f"({up['terminal']['name']}) "
                f"{int(remaining_minutes)}분 후 도착 - {up['location']}",
            )
        for up in line_yellow["timetable"]["up"]:
            if len(line_yellow["realtime"]["up"]) > 0:
                if calculate_bigger_than_realtime(
                    calculate_remaining_minutes(
                        line_yellow["realtime"]["up"][-1]["time"],
                        line_yellow["realtime"]["up"][-1]["updatedAt"],
                        now,
                    ),
                    up["time"],
                ):
                    continue
            line_yellow_up_arrival.append(f"({up['terminal']['name']}) {timetable_to_str(up['time'])} 출발")

        line_yellow_down_arrival = []
        for down in line_yellow["realtime"]["down"]:
            remaining_minutes = calculate_remaining_minutes(down["time"], down["updatedAt"], now)
            if remaining_minutes < 0:
                continue
            line_yellow_down_arrival.append(
                f"({down['terminal']['name']}) "
                f"{int(remaining_minutes)}분 후 도착 - {down['location']}",
            )
        for down in line_yellow["timetable"]["down"]:
            if len(line_yellow["realtime"]["down"]) > 0:
                if calculate_bigger_than_realtime(
                    calculate_remaining_minutes(
                        line_yellow["realtime"]["down"][-1]["time"],
                        line_yellow["realtime"]["down"][-1]["updatedAt"],
                        now,
                    ),
                    down["time"],
                ):
                    continue
            line_yellow_down_arrival.append(f"({down['terminal']['name']}) {timetable_to_str(down['time'])} 출발")
        line_blue_up_arrival = line_blue_up_arrival[:3] if len(line_blue_up_arrival) > 3 else line_blue_up_arrival
        line_blue_down_arrival = (
            line_blue_down_arrival[:3] if len(line_blue_down_arrival) > 3 else line_blue_down_arrival
        )
        line_yellow_up_arrival = (
            line_yellow_up_arrival[:3] if len(line_yellow_up_arrival) > 3 else line_yellow_up_arrival
        )
        line_yellow_down_arrival = (
            line_yellow_down_arrival[:3] if len(line_yellow_down_arrival) > 3 else line_yellow_down_arrival
        )

        line_blue_title = "한대앞역 (4호선)"
        line_blue_description = "서울 방면\n"
        line_blue_description += "\n".join(line_blue_up_arrival) if len(line_blue_up_arrival) > 0 else "운행 정보 없음"
        line_blue_description += "\n\n"
        line_blue_description += "오이도 방면\n"
        line_blue_description += "\n".join(line_blue_down_arrival) if len(line_blue_down_arrival) > 0 else "운행 정보 없음"

        line_yellow_title = "한대앞역 (수인분당선)"
        line_yellow_description = "수원 방면\n"
        line_yellow_description += "\n".join(line_yellow_up_arrival) if len(line_yellow_up_arrival) > 0 else "운행 정보 없음"
        line_yellow_description += "\n\n"
        line_yellow_description += "인천 방면\n"
        line_yellow_description += (
            "\n".join(line_yellow_down_arrival) if len(line_yellow_down_arrival) > 0 else "운행 정보 없음"
        )
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
                            {
                                "title": line_blue_title,
                                "description": line_blue_description.strip(),
                            },
                            {
                                "title": line_yellow_title,
                                "description": line_yellow_description.strip(),
                            },
                        ],
                    },
                },
            ],
        },
    }
