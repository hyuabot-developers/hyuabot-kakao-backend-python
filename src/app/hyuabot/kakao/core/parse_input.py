from app.hyuabot.kakao.scheme.request import KakaoRequest


def parse_user_utterance(user_input: KakaoRequest) -> str:
    return user_input.user_request.utterance
