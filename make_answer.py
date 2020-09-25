from transport.shuttle.get_info import get_departure_info
from kakao.common.sender import insert_text

def make_answser_shuttle_depart_info(user_answer):
    dest_stop = user_answer[2:]
    depart_info = get_departure_info(dest_stop)
    if depart_info == '오늘 셔틀 운행을 하지 않습니다.':
        server_answer = insert_text(depart_info)

    else:
        bus_to_come_dh, bus_to_come_dy, bus_to_come_c = depart_info

        # 도착정보를 응답으로 변환
        if dest_stop == '기숙사' or dest_stop == '셔틀콕':
            pass
        elif dest_stop == '한대앞':
            pass
        elif dest_stop == '예술인A':
            pass
    
    # 하단 버튼 추가
    reply = make_reply('🔍 정류장', f'{dest_stop} 정류장 정보입니다.', '5ebf702e7a9c4b000105fb25')
    response = insert_replies(server_answer, reply)
    reply = make_reply('🚫 오류제보', '셔틀 오류 제보하기','5cc3fced384c5508fceec5bb')
    response = insert_replies(response, reply)
    return server_answer