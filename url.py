# External Module
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Internal Module
from kakao.common.models import KakaoRequest, ShuttleRequest, FoodRequest, ReadingRoomRequest, ShuttleStopRequest
from kakao.common.user import *
from kakao.answer_shuttle import make_answer_shuttle_depart_info  # To get departure info
from kakao.answer_shuttle import make_answer_shuttle_stop_detail  # To get shuttle stop info
from kakao.answer_library import make_answer_reading_room_info  # To get seat info in reading room
from kakao.answer_food import make_answer_food_menu  # To get food menu
from kakao.common.sender import *

kakao_url = APIRouter()


# Route urls
@kakao_url.post('/shuttle')
async def get_shuttle_departure(request: ShuttleRequest):
    """셔틀 정류장을 사용자로부터 입력받아 행선지별 도착 정보를 최대 두개씩 반환합니다."""
    _, user_answer = request.userRequest.user.id, request.userRequest.utterance
    result_json = make_answer_shuttle_depart_info(user_answer)
    return JSONResponse(result_json)


@kakao_url.post('/food')
async def get_food_menu(request: FoodRequest):
    """원하는 캠퍼스 또는 식당을 입력받아 식당별 메뉴를 반환합니다."""
    user_id, answer = request.userRequest.user.id, request.userRequest.utterance
    user_info = get_user(user_id)
    if not user_info:
        response = find_is_new_user(user_id, answer)
        return JSONResponse(response)
    if '의 식단입니다' in answer:
        result_json = make_answer_food_menu(user_info['campus'], answer.split('의 식단입니다.')[0].strip())
    else:
        response = insert_text('원하는 식당을 선택해주세요.')
        if user_info['campus']:
            rest_list = ['학생식당', '신학생식당', '교직원식당', '신교직원식당', '제1생활관식당', '제2생활관식당', '사랑방', '행원파크']
        else:
            rest_list = ['학생식당', '교직원식당', '창의인재원식당', '푸드코트', '창업보육센터']
        for restaurant in rest_list:
            reply = make_reply(restaurant, f'{restaurant}의 식단입니다.', '5eaa9b11cdbc3a00015a23fb')
            response = insert_replies(response, reply)
        return JSONResponse(response)
    return JSONResponse(result_json)


@kakao_url.post('/library/seats')
async def get_reading_room_info(request: ReadingRoomRequest):
    """원하는 캠퍼스 또는 열람실을 입력받아 열람실별 잔여 좌석을 반환합니다."""
    user_id, answer = request.userRequest.user.id, request.userRequest.utterance
    user_info = get_user(user_id)
    if not user_info:
        response = find_is_new_user(user_id, answer)
        return JSONResponse(response)
    if '의 좌석정보입니다.' not in answer:
        response = make_answer_reading_room_info(user_info['campus'])
    else:
        response = make_answer_reading_room_info(user_info['campus'], answer.split('의 좌석정보입니다.')[0].strip())
    return JSONResponse(response)


@kakao_url.post('/update/campus')
async def update_campus(request: KakaoRequest):
    """사용자 ID를 기반으로 서울캠퍼스 ↔ ERICA 캠퍼스 상호 전환이 가능하게 합니다."""
    user_id, answer = request.userRequest.user.id, request.userRequest.utterance
    user_info = get_user(user_id)
    if user_info:
        if user_info['campus']:
            update_user_campus(user_id, 0)
            response = insert_text('ERICA 캠퍼스로 변경되었습니다.')
        else:
            update_user_campus(user_id, 1)
            response = insert_text('서울 캠퍼스로 변경되었습니다.')
    else:
        response = find_is_new_user(user_id, answer)
    return JSONResponse(response)


@kakao_url.post('/update/language')
async def update_campus(request: KakaoRequest):
    """사용자 ID를 기반으로 한국어 ↔ English 상호 전환이 가능하게 합니다."""
    user_id, answer = request.userRequest.user.id, request.userRequest.utterance
    user_info = get_user(user_id)
    if user_info:
        if user_info['language'] == 'Korean':
            update_user_language(user_id, 'English')
            response = insert_text('Language is changed to English')
        else:
            update_user_language(user_id, 'Korean')
            response = insert_text('한국어로 변경되었습니다.')
    else:
        response = find_is_new_user(user_id, answer)
    return JSONResponse(response)


@kakao_url.post('/shuttle/detail')
async def get_shuttle_stop_info(request: ShuttleStopRequest):
    """셔틀 정류장을 사용자로부터 입력받아 정류장 위치 및 첫막차 정보를 반환합니다."""
    _, user_answer = request.userRequest.user.id, request.userRequest.utterance
    result_json = make_answer_shuttle_stop_detail(user_answer)
    return JSONResponse(result_json)
