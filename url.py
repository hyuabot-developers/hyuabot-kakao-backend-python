# External Module
from flask import request, jsonify
from flask_restx import Resource

# Internal Module
from kakao.common.receiver import get_user_data  # To parse answer json
from kakao.answer_shuttle import make_answer_shuttle_depart_info  # To get departure info
from kakao.answer_shuttle import make_answer_shuttle_stop_detail  # To get shuttle stop info
from kakao.common.models import kakao_data, kakao_url


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


@kakao_url.route('/library')
class SearchBook(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """원하는 캠퍼스 또는 열람실을 입력받아 열람실별 잔여 좌석을 반환합니다."""
        return 'library'


@kakao_url.route('/update/campus')
class UpdateCampus(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """사용자 ID를 기반으로 서울캠퍼스 ↔ ERICA 캠퍼스 상호 전환이 가능하게 합니다."""
        return 'campus update'


@kakao_url.route('/shuttle/detail')
class ShuttleStopDetail(Resource):
    # @kakao_url.expect(kakao_data)
    def post(self):
        """셔틀 정류장을 사용자로부터 입력받아 정류장 위치 및 첫막차 정보를 반환합니다."""
        _, user_answer = get_user_data(request.get_json())
        result_json = make_answer_shuttle_stop_detail(user_answer)
        return jsonify(result_json)
