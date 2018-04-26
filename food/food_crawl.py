from bs4 import BeautifulSoup
import requests, os
from datetime import datetime

#밥대생의 open api를 경유한 학식 크롤링
def food_request(campus_id, cafeteria_id):
    bob_api = str(os.getenv('bob'))
    link = "https://bablabs.com/openapi/v1"
    header = {'Accesstoken': bob_api}
    param = {'date': datetime.today().strftime('%Y-%m-%d')}
    response = requests.get(link + '/campuses/' + campus_id + '/stores/' + cafeteria_id, headers=header, params=param)
    return response.json()


def food_request_main(campus, where):
    campus_dic = {'Seoul': '7EGUyZyheS', 'ERICA': 'BVRPhfbjvn'}
    cafeteria_dic = {'student_erica': 'LTI0MTE0NTE5', 'dorm_erica': 'LTI0MTEyNjM2', 
        'teacher_erica': 'LTI0MTE2NDAw', 'changbo_erica': 'LTI0MTA4ODY0', 'foodcoart_erica': 'LTI0MTEwNzUx',
        'student_seoul': 'LTI0MTA2OTc1', 'teacher_seoul': 'LTI0MTAzMTkx', 'hangwon_seoul': 'LTI0MDkzNjk2','sarang_seoul': 'LTI0MTAxMjk2', 
        'dorm2_seoul': 'LTI0MDk1NTk5', 'newstudent_seoul': 'LTI0MDk5Mzk5', 'newteacher_seoul': 'LTI0MDk3NTAw'}
    return food_request(campus_dic[campus], cafeteria_dic[where])