# 카카오톡 채널 상 사용자 응답 정보 처리 함수
def get_user_data(json_request):
    user_answer = json_request['userRequest']['utterance']
    user_id = json_request['userRequest']['user']['id']

    return user_id, user_answer
