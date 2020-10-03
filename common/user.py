from firebase_admin import get_app, initialize_app, firestore, _apps

from firebase.firebase_init import get_cred
from kakao_i_hanyang.common.sender import *


# 봇 사용시 기존 사용자 정보 조회
def get_user(user_id):
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()
    user_query = db.collection('botuser').where('id', '==', user_id).limit(1)
    for user_info in user_query.stream():
        return user_info.to_dict()


# 봇 사용시 사용자 정보 생성
def create_user(user_key, campus):
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.set({'id': user_key, 'campus': campus})


# 봇 사용자 캠퍼스 정보 변경
def update_user(user_key, campus):
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.update({'campus': campus})


# 새 사용자 판별
def find_is_new_user(user_id, answer):
    block_id = '5eaa9bf741559f000197775d'
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
    return response
