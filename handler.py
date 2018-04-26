from food.food_main import make_string_food
import sqlite3


button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
seoul_cafeteria_list = ["학생식당", "교직원식당", "사랑방", "신교직원식당", "제1생활관식당",  "제2생활관식당", "행원파크", "처음으로"]
erica_cafeteria_list =  ["학생식당", "교직원식당", "푸드코트", "창업보육센터", "기숙사식당", "처음으로"]


def handler(content, campus = 1):
    global button_list, seoul_cafeteria_list, erica_cafeteria_list
    if content == "학식":
        string = "식단을 알고 싶은 식당을 선택해주세요."
        if campus == 1:
            button_list = erica_cafeteria_list
        else:
            button_list = seoul_cafeteria_list
    elif content in seoul_cafeteria_list[:-1] or content in erica_cafeteria_list[:-1]:
        string = make_string_food(content, campus)
    elif content == "교통":
        if campus == 1:
            string = '원하시는 서비스를 선택해주세요.'
            button_list = ['버스', '지하철', '셔틀버스','처음으로']
        else:
            string = '한양대역(2호선) 도착정보입니다.'
            button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
    elif content == "처음으로":
        button_list =   ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
        string = "처음으로 돌아갑니다."
    else:
        string = content
    return string, button_list