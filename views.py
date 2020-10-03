import json

# Try restful api framework later
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.response import Response
# from rest_framework.parsers import JSONParser

# Use Normal django framework
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from kakao_i_hanyang.answer.answer_food import make_answer_food_menu
from kakao_i_hanyang.answer.answer_library import make_answer_reading_room_info
from kakao_i_hanyang.answer.answer_shuttle import make_answer_shuttle_depart_info, make_answer_shuttle_stop_detail
from kakao_i_hanyang.common.receiver import get_user_data
from kakao_i_hanyang.common.sender import insert_text, make_reply, insert_replies
from kakao_i_hanyang.common.user import get_user, find_is_new_user, update_user


@csrf_exempt
def get_shuttle_departure_info(request):
    _, user_answer = get_user_data(request)
    response = make_answer_shuttle_depart_info(user_answer)
    return JsonResponse(response)


@csrf_exempt
def get_shuttle_stop_info(request):
    _, user_answer = get_user_data(request)
    response = make_answer_shuttle_stop_detail(user_answer)
    return JsonResponse(response)


@csrf_exempt
def get_food_menu(request):
    user_id, user_answer = get_user_data(request)
    user_info = get_user(user_id)
    if not user_info:
        response = find_is_new_user(user_id, user_answer)
        return JsonResponse(response)
    if '의 식단입니다.' in user_answer:
        response = make_answer_food_menu(user_info['campus'], user_answer.split('의 식단입니다.')[0].strip())
    else:
        response = insert_text('원하는 식당을 선택해주세요.')
        if user_info['campus']:
            rest_list = ['학생식당', '신학생식당', '교직원식당', '신교직원식당', '제1생활관식당', '제2생활관식당', '사랑방', '행원파크']
        else:
            rest_list = ['학생식당', '교직원식당', '창의인재원식당', '푸드코트', '창업보육센터']
        for restaurant in rest_list:
            reply = make_reply(restaurant, f'{restaurant}의 식단입니다.', '5eaa9b11cdbc3a00015a23fb')
            response = insert_replies(response, reply)
    return JsonResponse(response)


@csrf_exempt
def get_reading_room_seat_info(request):
    user_id, user_answer = get_user_data(request)
    user_info = get_user(user_id)
    if not user_info:
        response = find_is_new_user(user_id, user_answer)
        return JsonResponse(response)
    if '열람실 정보' in user_answer:
        response = make_answer_reading_room_info(user_info['campus'])
    else:
        response = make_answer_reading_room_info(user_info['campus'], user_answer.split('의 좌석정보입니다.')[0].strip())
    return JsonResponse(response)


@csrf_exempt
def update_campus(request):
    """사용자 ID를 기반으로 서울캠퍼스 ↔ ERICA 캠퍼스 상호 전환이 가능하게 합니다."""
    user_id, answer = get_user_data(request)
    user_info = get_user(user_id)
    block_id = '5eaa9bf741559f000197775d'
    if user_info:
        if user_info['campus']:
            update_user(user_id, 0)
            response = insert_text('ERICA 캠퍼스로 변경되었습니다.')
        else:
            update_user(user_id, 1)
            response = insert_text('서울 캠퍼스로 변경되었습니다.')
    else:
        response = find_is_new_user(user_id, answer)
    return JsonResponse(response)
