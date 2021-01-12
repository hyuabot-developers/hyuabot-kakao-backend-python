from kakao.common.sender import *
from kakao.answer.answer_subway import make_answer_subway


def answer_transport_main():
    response = insert_text('원하는 정보를 선택해주세요.')
    reply = make_reply('🚌 셔틀버스', '셔틀버스 정보 알려주세요!', '5cc18bd905aaa7027c936c04')
    response = insert_replies(response, reply)
    reply = make_reply('🚍 노선버스', '노선버스 정보 알려주세요!', '5f8149b40b697c65dc56cbff')
    response = insert_replies(response, reply)
    reply = make_reply('🚉 전철', '전철 도착 정보 알려주세요!', '5f8149af49323b0752336006')
    response = insert_replies(response, reply)
    return response
