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


@router.post("", response_model=CarouselResponse, tags=["bus"])
async def get_bus(_: Payload):
    current_time = datetime.datetime.now(tz=timezone("Asia/Seoul"))
    current_time_str = current_time.strftime("%H:%M")
    transport = AIOHTTPTransport(url=f"{settings.API_URL}/query")
    weekdays = "weekdays"
    if current_time.weekday() == 5:
        weekdays = "saturday"
    elif current_time.weekday() == 6:
        weekdays = "sunday"
    query = gql(
        f"""
            query {{
                bus (start: \"{current_time_str}\", weekdays: \"{weekdays}\") {{
                    id,
                    routes {{
                        info {{ name }}
                        timetable {{ time }}
                        realtime {{ stop, time, seat, lowFloor, updatedAt }}
                    }}
                }}
            }}
        """,
    )
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(query)
        bus = result["bus"]
        convention_center_filter = list(filter(lambda x: x["id"] == 216000379, bus))
        main_gate_filter = list(filter(lambda x: x["id"] == 216000719, bus))
        junction_filter = list(filter(lambda x: x["id"] == 216000070, bus))
        sangnoksu_station_filter = list(filter(lambda x: x["id"] == 216000138, bus))
        convention_center = convention_center_filter[0] if convention_center_filter else None
        main_gate = main_gate_filter[0] if main_gate_filter else None
        junction = junction_filter[0] if junction_filter else None
        sangnoksu_station = sangnoksu_station_filter[0] if sangnoksu_station_filter else None

        if convention_center is None or main_gate is None or junction is None or sangnoksu_station is None:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "textCard",
                                "items": [{
                                    "text": "버스 API 오류",
                                    "description": "버스 정보를 불러오지 못했습니다.",
                                }],
                            },
                        },
                    ],
                },
            }
        try:
            bus_to_sangnoksu_station = list(
                filter(
                    lambda x: x["info"]["name"] == "10-1", convention_center["routes"],
                ),
            )[0]
            bus_from_sangnoksu_station = list(
                filter(
                    lambda x: x["info"]["name"] == "10-1", sangnoksu_station["routes"],
                ),
            )[0]
            bus_3100 = list(filter(lambda x: x["info"]["name"] == "3100", main_gate["routes"]))[0]
            bus_3100n = list(filter(lambda x: x["info"]["name"] == "3100N", main_gate["routes"]))[0]
            bus_3101 = list(filter(lambda x: x["info"]["name"] == "3101", main_gate["routes"]))[0]
            bus_707_1 = list(filter(lambda x: x["info"]["name"] == "707-1", main_gate["routes"]))[0]
            bus_3102 = list(filter(lambda x: x["info"]["name"] == "3102", convention_center["routes"]))[0]
            bus_110 = list(filter(lambda x: x["info"]["name"] == "110", junction["routes"]))[0]
            bus_7070 = list(filter(lambda x: x["info"]["name"] == "7070", junction["routes"]))[0]
            bus_9090 = list(filter(lambda x: x["info"]["name"] == "9090", junction["routes"]))[0]
            bus_suwon = []
            for bus_item in bus_110["realtime"]:
                bus_suwon.append({"name": "110", **bus_item})
            for bus_item in bus_7070["realtime"]:
                bus_suwon.append({"name": "7070", **bus_item})
            for bus_item in bus_9090["realtime"]:
                bus_suwon.append({"name": "9090", **bus_item})
        except IndexError:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "textCard",
                                "items": [{
                                    "text": "버스 API 오류",
                                    "description": "버스 정보를 불러오지 못했습니다.",
                                }],
                            },
                        },
                    ],
                },
            }
        # 학교 → 상록수역 버스
        bus_to_sangnoksu_station_arrival = []
        for realtime_item in bus_to_sangnoksu_station["realtime"]:
            if realtime_item["lowFloor"]:
                bus_to_sangnoksu_station_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상)",
                )
            else:
                bus_to_sangnoksu_station_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착",
                )
        if len(bus_to_sangnoksu_station_arrival) < 3:
            for index, timetable_item in enumerate(bus_to_sangnoksu_station["timetable"]):
                if index >= 3:
                    break
                bus_to_sangnoksu_station_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 상록수역 → 학교 버스
        bus_from_sangnoksu_station_arrival = []
        for realtime_item in bus_from_sangnoksu_station["realtime"]:
            if realtime_item["lowFloor"]:
                bus_from_sangnoksu_station_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상)",
                )
            else:
                bus_from_sangnoksu_station_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착",
                )
        if len(bus_from_sangnoksu_station_arrival) < 3:
            for index, timetable_item in enumerate(bus_from_sangnoksu_station["timetable"]):
                if index >= 3:
                    break
                bus_from_sangnoksu_station_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 3100번 버스
        bus_3100_arrival = []
        for realtime_item in bus_3100["realtime"]:
            if realtime_item["lowFloor"]:
                bus_3100_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상, {realtime_item['seat']}석)",
                )
            else:
                bus_3100_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 ({realtime_item['seat']}석)",
                )
        if len(bus_3100_arrival) < 3:
            for index, timetable_item in enumerate(bus_3100["timetable"]):
                if index >= 3:
                    break
                bus_3100_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 3100N번 버스
        bus_3100n_arrival = []
        for realtime_item in bus_3100n["realtime"]:
            if realtime_item["lowFloor"]:
                bus_3100n_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상, {realtime_item['seat']}석)",
                )
            else:
                bus_3100n_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 ({realtime_item['seat']}석)",
                )
        if len(bus_3100n_arrival) < 3:
            for index, timetable_item in enumerate(bus_3100n["timetable"]):
                if index >= 3:
                    break
                bus_3100n_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 3101번 버스
        bus_3101_arrival = []
        for realtime_item in bus_3101["realtime"]:
            if realtime_item["lowFloor"]:
                bus_3101_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상, {realtime_item['seat']}석)",
                )
            else:
                bus_3101_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 ({realtime_item['seat']}석)",
                )
        if len(bus_3101_arrival) < 3:
            for index, timetable_item in enumerate(bus_3101["timetable"]):
                if index >= 3:
                    break
                bus_3101_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 3102번 버스
        bus_3102_arrival = []
        for realtime_item in bus_3102["realtime"]:
            if realtime_item["lowFloor"]:
                bus_3102_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상, {realtime_item['seat']}석)",
                )
            else:
                bus_3102_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 ({realtime_item['seat']}석)",
                )
        if len(bus_3102_arrival) < 3:
            for index, timetable_item in enumerate(bus_3102["timetable"]):
                if index >= 3:
                    break
                bus_3102_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 707-1번 버스
        bus_707_1_arrival = []
        for realtime_item in bus_707_1["realtime"]:
            if realtime_item["lowFloor"]:
                bus_707_1_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 (저상, {realtime_item['seat']}석)",
                )
            else:
                bus_707_1_arrival.append(
                    f"{int(realtime_item['time'])}분 후 도착 ({realtime_item['seat']}석)",
                )
        if len(bus_707_1_arrival) < 3:
            for index, timetable_item in enumerate(bus_707_1["timetable"]):
                if index >= 3:
                    break
                bus_707_1_arrival.append(
                    f"{timetable_to_str(timetable_item['time'])} 시점 출발",
                )
        # 학교 → 수원역 버스
        bus_suwon_arrival = []
        for realtime_item in sorted(bus_suwon, key=lambda x: x["time"]):
            if realtime_item["lowFloor"]:
                bus_suwon_arrival.append(
                    f"({realtime_item['name']}번) {int(realtime_item['time'])}분 후 도착 (저상)",
                )
            else:
                bus_suwon_arrival.append(
                    f"({realtime_item['name']}번) {int(realtime_item['time'])}분 후 도착",
                )
        intercity_bus_title = "시내버스"
        intercity_bus_description = "10-1번 (학교 → 상록수역)\n"
        if len(bus_to_sangnoksu_station_arrival) > 0:
            if len(bus_to_sangnoksu_station_arrival) > 3:
                intercity_bus_description += "\n".join(bus_to_sangnoksu_station_arrival[:3])
            else:
                intercity_bus_description += "\n".join(bus_to_sangnoksu_station_arrival)
        else:
            intercity_bus_description += "운행 정보 없음"
        intercity_bus_description += "\n\n10-1번 (상록수역 → 학교)\n"
        if len(bus_from_sangnoksu_station_arrival) > 0:
            if len(bus_from_sangnoksu_station_arrival) > 3:
                intercity_bus_description += "\n".join(bus_from_sangnoksu_station_arrival[:3])
            else:
                intercity_bus_description += "\n".join(bus_from_sangnoksu_station_arrival)
        else:
            intercity_bus_description += "운행 정보 없음"

        seoul_bus_title = "강남역 방면 버스"
        seoul_bus_description = "3102번 (학교 → 강남역)\n"
        if len(bus_3102_arrival) > 0:
            if len(bus_3102_arrival) > 3:
                seoul_bus_description += "\n".join(bus_3102_arrival[:3])
            else:
                seoul_bus_description += "\n".join(bus_3102_arrival)
        else:
            seoul_bus_description += "운행 정보 없음"
        seoul_bus_description += "\n\n3100N번 (학교 → 강남역, 심야)\n"
        if len(bus_3100n_arrival) > 0:
            if len(bus_3100n_arrival) > 3:
                seoul_bus_description += "\n".join(bus_3100n_arrival[:3])
            else:
                seoul_bus_description += "\n".join(bus_3100n_arrival)
        else:
            seoul_bus_description += "운행 정보 없음"

        suwon_bus_title = "수원역 방면 버스"
        suwon_bus_description = "707-1번 (정문 → 수원역)\n"
        if len(bus_707_1_arrival) > 0:
            if len(bus_707_1_arrival) > 3:
                suwon_bus_description += "\n".join(bus_707_1_arrival[:3])
            else:
                suwon_bus_description += "\n".join(bus_707_1_arrival)
        else:
            suwon_bus_description += "운행 정보 없음"
        suwon_bus_description += "\n\n기타 (한양대입구 → 수원역)\n"
        if len(bus_suwon_arrival) > 0:
            if len(bus_suwon_arrival) > 3:
                suwon_bus_description += "\n".join(bus_suwon_arrival[:3])
            else:
                suwon_bus_description += "\n".join(bus_suwon_arrival)
        else:
            suwon_bus_description += "운행 정보 없음"

        other_bus_title = "군포, 의왕 방면 버스"
        other_bus_description = "3100번 (학교 → 군포 → 강남역)\n"
        if len(bus_3100_arrival) > 0:
            if len(bus_3100_arrival) > 3:
                other_bus_description += "\n".join(bus_3100_arrival[:3])
            else:
                other_bus_description += "\n".join(bus_3100_arrival)
        else:
            other_bus_description += "운행 정보 없음"
        other_bus_description += "\n\n3101번 (학교 → 의왕 → 강남역)\n"
        if len(bus_3101_arrival) > 0:
            if len(bus_3101_arrival) > 3:
                other_bus_description += "\n".join(bus_3101_arrival[:3])
            else:
                other_bus_description += "\n".join(bus_3101_arrival)
        else:
            other_bus_description += "운행 정보 없음"

        response_card = [
            {
                "title": intercity_bus_title,
                "description": intercity_bus_description,
            },
            {
                "title": seoul_bus_title,
                "description": seoul_bus_description,
            },
            {
                "title": suwon_bus_title,
                "description": suwon_bus_description,
            },
            {
                "title": other_bus_title,
                "description": other_bus_description,
            },
        ]
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "textCard",
                        "items": response_card,
                    },
                },
            ],
        },
    }
