from enum import Enum
import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring

from utils import *

class Cafeteria(Enum):
    student_seoul_1 = "1"
    teacher_seoul_1 = "2"
    sarang_seoul = "3"
    teacher_seoul_2 = "4"
    student_seoul_2 = "5"
    dorm_seoul_1 = "6"
    dorm_seoul_2 = "7"
    hangwon_seoul = "8"
    teacher_erica = "11"
    student_erica = "12"
    dorm_erica = "13"
    foodcoart_erica = "14"
    changbo_erica = "15"


def get_recipe(cafeteria : Cafeteria, url="https://www.hanyang.ac.kr/web/www/re"):
    ret = {}
    ret["restaurant"] = cafeteria.name

    inboxes = CSSSelector("div.in-box")
    h4 = CSSSelector("h4")  # 조식, 중식, 석식
    h3 = CSSSelector("h3")  # menu
    li = CSSSelector("li")
    price = CSSSelector("p.price")
    # get
    try:
        res = requests.get(f"{url}{cafeteria.value}")
    except requests.exceptions.RequestException as _:
        ret["restaurant"] = "-1"
        return ret

    tree = fromstring(res.text)
    for inbox in inboxes(tree):
        title = h4(inbox)[0].text_content()
        ret[title] = []
        for l in li(inbox):
            menu = h3(l)[0].text_content().replace("\t", "").replace("\r\n", "")
            p = price(l)[0].text_content()
            ret[title].append({"menu": menu, "price": p})

    return ret
