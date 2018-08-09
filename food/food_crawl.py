from bs4 import BeautifulSoup
import requests, os
from datetime import datetime

#밥대생의 open api를 경유한 학식 크롤링
def food_request(campus_id, cafeteria_id):
    bob_api = str(os.getenv('bob'))
    LINK = "https://bablabs.com/openapi/v1" #상수는 대문자로 하는것이 Python Standard
    header = {'Accesstoken': bob_api}
    param = {'date': datetime.today().strftime('%Y-%m-%d')}
    response = requests.get(LINK + '/campuses/' + campus_id + '/stores/' + cafeteria_id, headers=header, params=param)
    return response.json()


def food_request_main(campus, where):
    CAMPUS_DIC = {'Seoul': '7EGUyZyheS', 'ERICA': 'BVRPhfbjvn'}
    CAFATERIA_DIC = {'student_erica': 'LTI0MTE0NTE5', 'dorm_erica': 'LTI0MTEyNjM2', 
        'teacher_erica': 'LTI0MTE2NDAw', 'changbo_erica': 'LTI0MTA4ODY0', 'foodcoart_erica': 'LTI0MTEwNzUx',
        'student_seoul': 'LTI0MTA2OTc1', 'teacher_seoul': 'LTI0MTAzMTkx', 'hangwon_seoul': 'LTI0MDkzNjk2','sarang_seoul': 'LTI0MTAxMjk2', 
        'dorm2_seoul': 'LTI0MDk1NTk5', 'newstudent_seoul': 'LTI0MDk5Mzk5', 'newteacher_seoul': 'LTI0MDk3NTAw'}
    return food_request(CAMPUS_DIC[campus], CAFATERIA_DIC[where])
