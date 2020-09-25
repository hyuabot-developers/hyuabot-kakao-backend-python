# External Module
from flask import request
from flask_restx import Namespace, Resource

# Internal Module
from transport.shuttle.get_info import get_departure_info

# Declare namespace object
kakao_url = Namespace('kakao')

# Route urls
@kakao_url.route('/shuttle')
class get_shuttle(Resource):
    def get(self):
        get_departure_info()
        return 'shuttle'

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