from firebase_admin import _apps, initialize_app, firestore

from firebase.firebase_init import get_cred


# 봇 사용시 기존 사용자 정보 조회
def get_user(user_id):
    if not len(_apps):
        cred = get_cred()
        initialize_app(cred)
    db = firestore.client()
    user_query = db.collection('botuser').where('id', '==', user_id)
    for user_info in user_query.stream():
        return user_info.to_dict()


# 봇 사용시 사용자 정보 생성
def create_user(user_key, campus):
    if not len(_apps):
        cred = get_cred()
        initialize_app(cred)
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.set({'id': user_key, 'campus': campus})


# 봇 사용자 캠퍼스 정보 변경
def update_user(user_key, campus):
    if not len(_apps):
        cred = get_cred()
        initialize_app(cred)
    db = firestore.client()
    user = db.collection('botuser').document(user_key)
    user.update({'campus': campus})
