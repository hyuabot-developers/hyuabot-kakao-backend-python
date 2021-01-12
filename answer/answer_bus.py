from kakao.common.sender import *
from transport.bus.get_arrival_info import get_bus_info, get_bus_timetable
import datetime


def make_answer_bus_info():
    realtime_info = get_bus_info()
    now = datetime.datetime.now()
    if not (realtime_info['3102'] and realtime_info['10-1']):
        timetable = get_bus_timetable(weekdays=int(now.weekday()))
    string = ""
    string += '3102번(한양대게스트하우스)\n'
    if realtime_info['3102']:
        arrival_info = realtime_info['3102'][0]
        string += f"{arrival_info['location']} 전/{arrival_info['time']}분 후 도착({arrival_info['seat']}석)\n"
    elif timetable['3102']:
        arrival_info = timetable['3102'][0]
        string += f"송산그린시티 {arrival_info['time'].strftime('%H시 %M분')} 출발 예정\n"
    else:
        string += '도착 예정인 버스가 없습니다\n'

    string += '\n10-1번(한양대게스트하우스)\n'
    if realtime_info['10-1']:
        arrival_info = realtime_info['10-1'][0]
        string += f"{arrival_info['location']} 전/{arrival_info['time']}분 후 도착\n"
    elif timetable['10-1']:
        arrival_info = timetable['10-1'][0]
        string += f"푸르지오6차후문 {arrival_info['time'].strftime('%H시 %M분')} 출발 예정\n"
    else:
        string += '도착 예정인 버스가 없습니다\n'

    string += '\n707-1번(한양대정문)\n'
    if realtime_info['707-1']:
        arrival_info = realtime_info['707-1'][0]
        string += f"{arrival_info['location']} 전/{arrival_info['time']}분 후 도착({arrival_info['seat']}석)\n"
    else:
        string += '도착 예정인 버스가 없습니다\n'
    response = insert_text(string.strip())
    return response
