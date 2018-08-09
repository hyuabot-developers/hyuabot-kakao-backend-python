try:
    import food_crawl
except:
    from . import food_crawl
from datetime import datetime

def food_main(cafeteria):
    now = datetime.now()
    date_time_string = datetime.today().strftime('%Y-%m-%d')

    if 'erica' in cafeteria:
        campus = 'ERICA'
    else:
        campus = 'Seoul'
    menu_list = []
    received_json = food_crawl.food_request_main(campus, cafeteria)
    menus = received_json['store']['menus']
    if now.hour < 10:
        date_time_string += '의 조식\n'
        for x in menus:
            if x['time'] == 0:
                menu_list += [x]
    elif now.hour <15:
        date_time_string += '의 중식\n'
        for x in menus:
            if x['time'] == 1:
                menu_list += [x]
    else:
        date_time_string += '의 석식\n'
        for x in menus:
            if x['time'] == 2:
                menu_list += [x]
    if menu_list == []:
        date_time_string += '식단이 제공되지 않습니다'
    for x in menu_list:
        if x['name'] != '':
            date_time_string += x['name'] + ' '
        try:
            date_time_string += str(x['price']) + '원\n'
        except:
            pass
        for y in x['description'].split(' '):
            date_time_string += y + '\n'
        date_time_string += '\n'
    if date_time_string[-1] == '\n':
        date_time_string = date_time_string[:-1]
    return date_time_string

def make_string_food(content, campus=1):
    if "학생식당" in content:
        if campus == 1:
            string = food_main('student_erica')
        else:
            string = food_main('student_seoul')
    elif "교직원식당" in content:
        if campus == 1:
            string = food_main('teacher_erica')
        else:
            string = food_main('teacher_seoul')
    elif content == "푸드코트":
        string = food_main('foodcoart_erica')
    elif content == "창업보육센터":
        string = food_main('changbo_erica')
    elif content == "기숙사식당":
        string = food_main('dorm_erica')
    elif content == "사랑방":
        string = food_main('sarang_seoul')
    elif content == "신교직원식당":
        string = food_main('newteacher_seoul')
    elif content == "제1생활관식당":
        string = 'api 제공자의 사정으로 제공되지 않습니다.'
    elif content == "제2생활관식당":
        string = food_main('dorm2_seoul')
    elif content == "행원파크":
        string = food_main('hangwon_seoul')
    return string.strip()

