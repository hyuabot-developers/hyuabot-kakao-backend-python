import json


# 카카오톡 채널 상 사용자 응답 정보 처리 함수
def get_user_data(request):
    user_answer = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    user_id = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']

    return user_id, user_answer
