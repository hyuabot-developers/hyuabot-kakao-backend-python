import requests
from datetime import datetime
from . import date


def request():
    now = datetime.now()
    if date.is_semester(now.month, now.day):
        dir1 = "/semester"
    else:
        dir1 = "/vacation"
    if now.weekday() == 6:
        dir2 = "/sat.json"
    elif now.weekday() == 7:
        dir2 = "/sun.json"
    else:
        dir2 = "/week.json"
    link = 'https://nayunhwan.github.io/ShuttlecockAPI'+dir1+dir2
    response = requests.get(link)
    return response.json()


request()