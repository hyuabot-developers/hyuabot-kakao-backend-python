# External Module
from flask import Blueprint, request

# Internal Module
from transport.date import get_date

# Declare blueprint object
kakao_url = Blueprint('kakao_url', __name__)

# Route urls
@kakao_url.route('/shuttle')
def shuttle():
    get_date()
    return 'shuttle'

@kakao_url.route('/food')
def food():
    return 'food'

@kakao_url.route('/library')
def library():
    return 'library'

@kakao_url.route('/update/campus')
def update_campus():
    return 'campus update'

@kakao_url.route('/shuttle/detail')
def shuttle_detail():
    return 'shuttle stop detail'