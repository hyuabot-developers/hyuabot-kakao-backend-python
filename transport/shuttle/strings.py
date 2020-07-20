from . import shuttle
import datetime
try:
    from .date import is_semester, is_seasonal
except:
    from date import is_semester, is_seasonal

def make_string(where, destination):
    where_dic = {"shuttleOut":"Shuttlecock_O", "shuttleIn":"Shuttlecock_I", "subway":"Subway", "terminal":"YesulIn", "dorm":"Residence"}
    received_json = shuttle.request(where_dic[where])
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    timetable = received_json[list(received_json.keys())[0]]
    arrival_list = []
    string = ""
    if destination is not None:
        for x in timetable:
            hour, minute = x['time'].split(":")
            hour = int(hour)
            minute = int(minute)
            if x['type'] == destination and (hour > now.hour or (hour == now.hour and minute > now.minute)):
                arrival_list.append(x)
            if len(arrival_list) == 2:
                break
    else:
        for x in timetable:
            hour, minute = x['time'].split(":")
            hour = int(hour)
            minute = int(minute)
            if hour > now.hour or (hour == now.hour and minute > now.minute):
                arrival_list.append(x)
            if len(arrival_list) == 2:
                break
    for x in arrival_list:
        hour, minute = x['time'].split(":")
        time = (int(hour) - now.hour) * 60 + int(minute) - now.minute
        string += f"{hour}시 {minute}분 도착예정 ({time}분 후)\n"
    if string == '':
        string += '도착 예정인 버스가 없습니다.'
    if string[-1] == '\n':
        string = string[:-1]
    return string


def first_last(where):
    where_dic = {"shuttleOut":"Shuttlecock_O", "shuttleIn":"Shuttlecock_I", "subway":"Subway", "terminal":"YesulIn", "dorm":"Residence"}
    received_json = shuttle.request(where_dic[where])
    if where == "shuttleOut":
        stop_list = {"DH" : "한대앞 직행", "DY" : "예술인 직행", "C" : "순환버스"}
    elif where == "shuttleIn":
        stop_list = {"DH" : "기숙사행", "DY" : "기숙사행", "R" : "기숙사행", "NA" : "셔틀콕 종착"}
    elif where == "subway":
        stop_list = {"" : "셔틀콕 직행", "C" : "순환버스"}
    elif where == "terminal":
        stop_list = {"" : "셔틀콕 직행", "C" : "순환버스"}
    elif where == "dorm":
        stop_list = {"DH" : "한대앞 직행", "DY" : "예술인 직행", "C" : "순환버스"}
    timetable = received_json[list(received_json.keys())[0]]
    first, last = timetable[0], timetable[-1]
    string = ""
    hour, minute = first['time'].split(":")
    string += f"첫차: {hour.zfill(2)}:{minute.zfill(2)}({stop_list[first['type']]})\n"
    hour, minute = last['time'].split(":")
    string += f"막차: {hour.zfill(2)}:{minute.zfill(2)}({stop_list[last['type']]})"
    return string

def make2_string(route):
    received_json = shuttle.request2()
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    come_list = ["route1", "route2", "route3", "route4", "route5"]
    go_list = ["routeA", "routeB", "routeC", "routeD"]
    info = received_json[route]
    string = ""
    if route in come_list:
        for x in range(len(info)):
            string += info[x]['time'] +"/"
            string += info[x]['stop'] + '\n'
            stop_hour = int(info[x]['time'].split(':')[0])
            stop_min = int(info[x]['time'].split(':')[1])
            arrival = False
            if stop_hour < now.hour or (stop_hour == now.hour and stop_min < now.minute):
                laststop = x
            if laststop == len(info) - 1:
                arrival = True
        if x == len(info) - 1 and arrival:
            string += "현재 예상 위치: 학교 도착"
        else:
            string += "현재 예상 위치:" + info[laststop]['stop'] +"~" + info[laststop + 1]['stop']
    else:
        for x in info:
            string += x['stop'] + '\n'
        string += "하교 버스 출발 시간은 17시 40분입니다."
    return string