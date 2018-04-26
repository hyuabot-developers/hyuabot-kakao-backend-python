from . import shuttle
from datetime import datetime


def make_string(where, destination):
    received_json = shuttle.request()
    now = datetime.now()
    timetable = received_json[where]
    arrival_list = []
    type_list = {'cycle': '순환버스', 'toSubway': '한대앞역', 'toTerminal': '예술인A'}
    string = ''
    pos = 0
    if destination is not None:
        for x in timetable:
            if x['type'] == destination and (int(x['time'].split(':')[0]) > now.hour or (int(x['time'].split(':')[0]) == now.hour and int(x['time'].split(':')[1]) > now.minute)):
                arrival_list.append(x)
    else:
        for x in timetable:
            if int(x['time'].split(':')[0]) > now.hour or (int(x['time'].split(':')[0]) == now.hour and int(x['time'].split(':')[1]) > now.minute):
                arrival_list.append(x)
    for x in arrival_list:
        if pos < 2:
            string += type_list[x['type']] + ' ' + x['time'] + ' 도착예정\n'
            pos += 1
    if string == '':
        string += '도착 예정인 버스가 없습니다.'
    if string[-1] == '\n':
        string = string[:-1]
    return string