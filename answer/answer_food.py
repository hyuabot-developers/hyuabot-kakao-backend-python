from common.config import korea_timezone
from food.menu import CafeteriaSeoul, CafeteriaERICA, get_recipe

from kakao.common.sender import *

from datetime import datetime


def make_answer_food_menu(user_answer=''):
    now = datetime.now(tz=korea_timezone)
    cafeterias = {
        "학생식당": CafeteriaERICA.student_erica,
        "창의인재원식당": CafeteriaERICA.dorm_erica,
        "교직원식당": CafeteriaERICA.teacher_erica,
        "창업보육센터": CafeteriaERICA.changbo_erica,
        "푸드코트": CafeteriaERICA.food_court_erica
    }

    cafeteria = cafeterias[user_answer]
    recipe = get_recipe(cafeteria)
    string = f'{recipe["time"].strip()}\n'

    is_working = False
    for key in recipe.keys():
        if key in ['조식', '중식', '석식', '중식/석식', '분식']:
            is_working = True
            break

    if not is_working:
        string += '오늘 식당은 운영하지 않습니다.'
        response = insert_text(string.strip())
        return response

    both_lunch_dinner = False
    if '중식/석식' in recipe.keys():
        menus = recipe['중식/석식']
        for x in menus:
            string += x["menu"] + "\n"
            string += x["price"] + "\n"
            string += '\n'
        if string[-1] == '\n':
            string = string[:-1]
        both_lunch_dinner = True

    if '분식' in recipe.keys():
        menus = recipe['분식']
        for x in menus:
            string += x["menu"] + "\n"
            string += x["price"] + "\n"
            string += '\n'
        if string[-1] == '\n':
            string = string[:-1]

    if not both_lunch_dinner:
        if now.hour < 10:
            if "조식" in recipe.keys():
                string += "조식\n"
                menus = recipe["조식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]
        elif now.hour < 14:
            string += "중식\n"
            menus = recipe["중식"]
        elif now.hour < 19:
            if "석식" in recipe.keys():
                string += "석식\n"
                menus = recipe["석식"]
            else:
                string += "중식\n"
                menus = recipe["중식"]
        else:
            menus = [{"info": "미운영 시간입니다."}]
            string = "식당 운영시간이 아닙니다."
    # 식단이 없을 때
    if not menus:
        string = '식단이 제공되지 않습니다'
    if "info" not in menus[0].keys():
        for x in menus:
            string += x["menu"] + "\n"
            string += x["price"] + "\n"
            string += '\n'
        if string[-1] == '\n':
            string = string[:-1]
    rest_list = ['학생식당', '교직원식당', '창의인재원식당', '창업보육센터', '푸드코트']
    response = insert_text(string.strip())
    block_id = '5eaa9b11cdbc3a00015a23fb'
    for restaurant in rest_list:
        reply = make_reply(restaurant, f"{restaurant}의 식단입니다.", block_id)
        response = insert_replies(response, reply)

    return response
