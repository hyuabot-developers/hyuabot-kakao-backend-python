import requests
try:
    from .date import is_semester, is_seasonal
except:
    from date import is_semester, is_seasonal
import datetime, json, os
from workalendar.asia import SouthKorea

holiday = [(5, 15)]
def request(stopName):
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    cal = SouthKorea()
    # 학기중일 때
    if is_semester(now.month, now.day):
        dir1 = "/semester"
        # 주말
        if now.weekday() in [5, 6] or not cal.is_working_day(now) or (now.month, now.day) in holiday:
            dir2 = "/weekend"
            file_ext = "_weekend.json"
        # 평일
        else:
            dir2 = "/week"
            file_ext = "_week.json"
    elif is_seasonal(now.month, now.day):
        dir1 = "/vacation_session"
        if now.weekday() in [5, 6] or not cal.is_working_day(now):
            dir2 = "/weekend"
            file_ext = "_weekend.json"
        # 평일일 때
        else:
            dir2 = "/week"
            file_ext = "_week.json"
    else:
        # 방학일 때
        dir1 = "/vacation"
        # 토요일일 때
        if now.weekday() in [5, 6] or not cal.is_working_day(now):
            dir2 = "/weekend"
            file_ext = "_weekend.json"
        # 평일일 때
        else:
            dir2 = "/week"
            file_ext = "_week.json"
    # 셔틀콕 api 로 요청보냄
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/timetable' + dir1 + dir2 + "/" + stopName + file_ext) as json_file:
            json_data = json.load(json_file)
            return json_data
    except:
        link = 'https://raw.githubusercontent.com/jil8885/hyuabot-mainline/master/hyuabot/transport/shuttle/API/timetable/' + dir1 + dir2 + "/" + stopName + file_ext
        response = requests.get(link)
    return response.json()

def request2():
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    cal = SouthKorea()
    # 학기중일 때
    if is_semester(now.month, now.day) and now.weekday() not in [5, 6] and cal.is_working_day(now):
    # 셔틀콕 api 로 요청보냄
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + '/timetable/semester/schoolbus.json') as json_file:
                json_data = json.load(json_file)
                return json_data
        except:
            link = 'https://raw.githubusercontent.com/jil8885/ShuttlecockAPI/master/semester/schoolbus.json'
            response = requests.get(link)
            return response.json()
