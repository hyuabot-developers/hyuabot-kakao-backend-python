from datetime import datetime

from transport.shuttle.get_info import get_departure_info
from kakao.common.sender import *

def make_answser_shuttle_depart_info(user_answer):
    dest_stop = user_answer[2:]
    depart_info = get_departure_info(dest_stop)
    # 운행 중지 일자 일 때,
    if depart_info == '오늘 셔틀 운행을 하지 않습니다.':
        server_answer = insert_text(depart_info)

    else:
        bus_to_come_dh, bus_to_come_dy, bus_to_come_c = depart_info
        # 도착정보를 응답으로 변환
        if dest_stop == '기숙사':
            result = '기숙사→셔틀콕(5분),한대앞(15분)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n기숙사→셔틀콕(5분),예술인(15분)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n기숙사→셔틀콕(5분),한대앞(15분),예술인(20분)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '셔틀콕':
            result = '셔틀콕→한대앞(10분)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n셔틀콕→예술인A(10분)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n셔틀콕→한대앞(10분),예술인(15분)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '한대앞':
            result = '한대앞→셔틀콕(10분)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n한대앞→예술인(5분),셔틀콕(15분)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '예술인A':
            result = '예술인→셔틀콕(10분)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '셔틀콕 건너편':
            result = '셔틀콕 건너편→기숙사(5분)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        server_answer = insert_text(result)
    
    # 하단 버튼 추가
    reply = make_reply('🔍 정류장', f'{dest_stop} 정류장 정보입니다.', '5ebf702e7a9c4b000105fb25')
    response = insert_replies(server_answer, reply)
    reply = make_reply('🚫 오류제보', '셔틀 오류 제보하기','5cc3fced384c5508fceec5bb')
    response = insert_replies(response, reply)
    return server_answer