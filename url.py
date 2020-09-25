# External Module
from flask import request, jsonify
from flask_restx import Namespace, Resource

# Internal Module
from kakao.common.receiver import get_user_data # To parse answer json
from kakao.make_answer import make_answser_shuttle_depart_info # To get departure info

# Declare namespace object
kakao_url = Namespace('kakao')

# Route urls
@kakao_url.route('/shuttle')
class get_shuttle(Resource):
    def post(self):
        _, user_answer = get_user_data(request.get_json())
        result_json = make_answser_shuttle_depart_info(user_answer)
        return jsonify(result_json)

@kakao_url.route('/food')
class get_food(Resource):
    def get(self): 
        return 'food'   

@kakao_url.route('/library')
class search_book(Resource):
    def get(self):
        return 'library'

@kakao_url.route('/update/campus')
class update_campus(Resource):
    def get(self):
        return 'campus update'

@kakao_url.route('/shuttle/detail')
class shuttle_detail(Resource):
    def get(self):
        return 'shuttle stop detail'