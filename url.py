# External Module
from flask import request, jsonify
from flask_restx import Resource

# Internal Module
from kakao.common.user import *
from kakao.common.receiver import get_user_data  # To parse answer json
from kakao.answer_shuttle import make_answer_shuttle_depart_info  # To get departure info
from kakao.answer_shuttle import make_answer_shuttle_stop_detail  # To get shuttle stop info
from kakao.answer_library import make_answer_reading_room_info # To get seat info in reading room
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
        return 'food'


@kakao_url.route('/library/seats')
class SearchBook(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """원하는 캠퍼스 또는 열람실을 입력받아 열람실별 잔여 좌석을 반환합니다."""
        user_id, answer = get_user_data(request.get_json())
        user_info = get_user(user_id)
        if '열람실 정보' in answer:
            seat_info = make_answer_reading_room_info(user_info['campus'])
        else:
            seat_info = make_answer_reading_room_info(user_info['campus'], answer[1:].split('의 좌석정보입니다.')[0].strip())
        return jsonify(seat_info)


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
            if '서울' in answer:
                create_user(user_id, 1)
                response = insert_text('서울캠퍼스로 설정되었습니다.')
            elif 'ERICA' in answer:
                create_user(user_id, 0)
                response = insert_text('ERICA 캠퍼스로 설정되었습니다.')
            else:
                response = insert_text('등록되지 않은 사용자입니다.\n캠퍼스를 등록해 주십시오.')
                reply = make_reply('서울', '서울캠퍼스 선택', block_id)
                response = insert_replies(response, reply)
                reply = make_reply('ERICA', 'ERICA 캠퍼스 선택', block_id)
                response = insert_replies(response, reply)
        return jsonify(response)


@kakao_url.route('/shuttle/detail')
class ShuttleStopDetail(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """셔틀 정류장을 사용자로부터 입력받아 정류장 위치 및 첫막차 정보를 반환합니다."""
        _, user_answer = get_user_data(request.get_json())
        result_json = make_answer_shuttle_stop_detail(user_answer)
        return jsonify(result_json)
