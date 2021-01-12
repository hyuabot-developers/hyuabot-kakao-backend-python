from transport.subway.get_info import get_subway_info, get_subway_timetable
from transport.shuttle.date import is_semester
from kakao.common.sender import *

import time


def make_answer_subway() -> dict:
    _, is_weekend = is_semester()
    is_weekend = True if is_weekend == 'weekend' else False
    line_main = get_subway_info()
    line_sub = get_subway_timetable(is_weekend)
    if line_main:
        result = '4호선(한대앞역)\n'
        if line_main['up']:
            arrival_item = line_main['up'][0]
            end_station, pos, remained_time, status = list(arrival_item.values())
            if '전역' in status:
                result += f'{end_station}행 {status} {int(remained_time)}분 후 도착\n'
            else:
                result += f'{end_station}행 {pos} {int(remained_time)}분 후 도착\n'
        else:
            result += '당고개 방면 열차가 없습니다\n'
        if line_main['down']:
            arrival_item = line_main['down'][0]
            end_station, pos, remained_time, status = list(arrival_item.values())
            if '전역' in status:
                result += f'{end_station}행 {status} {int(remained_time)}분 후 도착\n'
            else:
                result += f'{end_station}행 {pos} {int(remained_time)}분 후 도착\n\n'
        else:
            result += '오이도 방면 열차가 없습니다\n'
        result += '\n수인선(한대앞역)\n'
        if line_sub['up']:
            end_station, arrival_time = line_sub['up'][0]['endStn'], line_sub['up'][0]['time']
            result += f'{end_station}행 {arrival_time.strftime("%H시 %M분")} 도착\n'
        else:
            result += '인천 방면 열차가 없습니다\n'
        if line_sub['down']:
            end_station, arrival_time = line_sub['down'][0]['endStn'], line_sub['down'][0]['time']
            result += f'{end_station}행 {arrival_time.strftime("%H시 %M분")} 도착\n'
        else:
            result += '왕십리/수원 방면 열차가 없습니다\n'
    else:
        result = "지하철 실시간 API 서버로부터 잘못된 응답을 수신하였습니다.\n잠시 후 다시 시도해주십시오."
    response = insert_text(result.strip())

    return response
