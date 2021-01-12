# External Module
from fastapi import APIRouter
from fastapi.responses import JSONResponse

# Internal Module
from food.menu import update_recipe
from kakao.common.models import KakaoRequest, ShuttleRequest, FoodRequest, ReadingRoomRequest, ShuttleStopRequest
from kakao.answer.answer_shuttle import make_answer_shuttle_depart_info  # To get departure info
from kakao.answer.answer_shuttle import make_answer_shuttle_stop_detail  # To get shuttle stop info
from kakao.answer.answer_shuttle import make_answer_shuttle_main  # To get shuttle main page
from kakao.answer.answer_library import make_answer_reading_room_info  # To get seat info in reading room
from kakao.answer.answer_food import make_answer_food_menu  # To get food menu
from kakao.answer.answer_subway import make_answer_subway
from kakao.answer.answer_bus import make_answer_bus_info
from kakao.answer.answer_common import answer_transport_main
from kakao.common.sender import *

kakao_url = APIRouter()


# Route urls
@kakao_url.post('/transport')
async def transport_main(request: KakaoRequest):
    """셔틀 정류장을 사용자로부터 입력받아 행선지별 도착 정보를 최대 두개씩 반환합니다."""
    user_id, user_answer = request.userRequest.user.id, request.userRequest.utterance
    result_json = answer_transport_main()
    return JSONResponse(result_json)


@kakao_url.post('/shuttle')
async def get_shuttle_departure(request: ShuttleRequest):
    """셔틀 정류장을 사용자로부터 입력받아 행선지별 도착 정보를 최대 두개씩 반환합니다."""
    user_id, user_answer = request.userRequest.user.id, request.userRequest.utterance
    result_json = make_answer_shuttle_depart_info(user_answer)
    return JSONResponse(result_json)


@kakao_url.post('/shuttle/main')
async def get_shuttle_main(request: KakaoRequest):
    """셔틀 메인 메뉴를 보여줍니다.."""
    result_json = make_answer_shuttle_main()
    return JSONResponse(result_json)


@kakao_url.post('/shuttle/detail')
async def get_shuttle_stop_info(request: ShuttleStopRequest):
    """셔틀 정류장을 사용자로부터 입력받아 정류장 위치 및 첫막차 정보를 반환합니다."""
    user_id, user_answer = request.userRequest.user.id, request.userRequest.utterance
    result_json = make_answer_shuttle_stop_detail(user_answer)
    return JSONResponse(result_json)


@kakao_url.post('/subway')
async def get_subway_departure(request: KakaoRequest):
    """전철역의 행선지별 도착 정보를 최대 한개씩 반환합니다."""
    result_json = make_answer_subway()
    return JSONResponse(result_json)


@kakao_url.post('/bus')
async def get_bus_departure(request: KakaoRequest):
    """버스 정류장의 행선지별 도착 정보를 최대 두개씩 반환합니다."""
    result_json = make_answer_bus_info()
    return JSONResponse(result_json)


@kakao_url.post('/food')
async def get_food_menu(request: FoodRequest):
    """원하는 캠퍼스 또는 식당을 입력받아 식당별 메뉴를 반환합니다."""
    user_id, answer = request.userRequest.user.id, request.userRequest.utterance
    if '의 식단입니다' in answer:
        result_json = make_answer_food_menu(answer.split('의 식단입니다.')[0].strip())
    else:
        response = insert_text('원하는 식당을 선택해주세요.')
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
    if '의 좌석정보입니다.' not in answer:
        response = make_answer_reading_room_info()
    else:
        response = make_answer_reading_room_info(answer.split('의 좌석정보입니다.')[0].strip())
    return JSONResponse(response)


@kakao_url.get('/food')
async def update_menu():
    update_recipe()
    return 'complete'
