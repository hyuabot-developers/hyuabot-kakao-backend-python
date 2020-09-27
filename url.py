# External Module
from flask import request, jsonify
from flask_restx import Resource

# Internal Module
from kakao.common.user import *
from kakao.common.receiver import get_user_data  # To parse answer json
from kakao.answer_shuttle import make_answer_shuttle_depart_info  # To get departure info
from kakao.answer_shuttle import make_answer_shuttle_stop_detail  # To get shuttle stop info
from kakao.answer_library import make_answer_reading_room_info  # To get seat info in reading room
from kakao.answer_food import make_answer_food_menu  # To get food menu
from kakao.common.sender import *
from kakao.common.models import kakao_url


# Route urls
@kakao_url.route('/shuttle')
class GetShuttle(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """셔틀 정류장을 사용자로부터 입력받아 행선지별 도착 정보를 최대 두개씩 반환합니다."""
        _, user_answer = get_user_data(request.get_json())
        result_json = make_answer_shuttle_depart_info(user_answer)
        return jsonify(result_json)


@kakao_url.route('/food')
class GetFood(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """원하는 캠퍼스 또는 식당을 입력받아 식당별 메뉴를 반환합니다."""
        user_id, answer = get_user_data(request.get_json())
        user_info = get_user(user_id)
        if not user_info:
            response = find_is_new_user(user_id, answer)
            return jsonify(response)
        if '의 식단입니다.' in answer:
            result_json = make_answer_food_menu(user_info['campus'], answer.split('의 식단입니다.')[0].strip())
        else:
            response = insert_text('원하는 식당을 선택해주세요.')
            if user_info['campus']:
                rest_list = ['학생식당', '신학생식당', '교직원식당', '신교직원식당', '제1생활관식당', '제2생활관식당', '사랑방', '행원파크']
            else:
                rest_list = ['학생식당', '교직원식당', '창의인재원식당', '푸드코트', '창업보육센터']
            for restaurant in rest_list:
                reply = make_reply(restaurant, '5eaa9b11cdbc3a00015a23fb', f'{restaurant}의 식단입니다.')
                response = insert_replies(response, reply)
            return jsonify(response)
        return jsonify(result_json)


@kakao_url.route('/library/seats')
class SearchBook(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """원하는 캠퍼스 또는 열람실을 입력받아 열람실별 잔여 좌석을 반환합니다."""
        user_id, answer = get_user_data(request.get_json())
        user_info = get_user(user_id)
        if not user_info:
            response = find_is_new_user(user_id, answer)
            return jsonify(response)
        if '열람실 정보' in answer:
            response = make_answer_reading_room_info(user_info['campus'])
        else:
            response = make_answer_reading_room_info(user_info['campus'], answer[1:].split('의 좌석정보입니다.')[0].strip())
        return jsonify(response)


@kakao_url.route('/update/campus')
class UpdateCampus(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """사용자 ID를 기반으로 서울캠퍼스 ↔ ERICA 캠퍼스 상호 전환이 가능하게 합니다."""
        user_id, answer = get_user_data(request.get_json())
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
        return jsonify(response)


@kakao_url.route('/shuttle/detail')
class ShuttleStopDetail(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """셔틀 정류장을 사용자로부터 입력받아 정류장 위치 및 첫막차 정보를 반환합니다."""
        _, user_answer = get_user_data(request.get_json())
        result_json = make_answer_shuttle_stop_detail(user_answer)
        return jsonify(result_json)
