from datetime import datetime

from transport.shuttle.get_info import get_departure_info, get_first_last_departure
from kakao_i_hanyang.common.sender import *


def make_answer_shuttle_depart_info(user_answer) -> str:
    if '의 셔틀버스 도착 정보입니다' in user_answer:
        dest_stop = user_answer.split('의 셔틀버스 도착 정보입니다')[0].strip()
    else:
        dest_stop = user_answer[2:].strip()
    depart_info = get_departure_info(dest_stop)
    # 운행 중지 일자 일 때,
    if depart_info == '오늘 셔틀 운행을 하지 않습니다.':
        server_answer = insert_text(depart_info)

    else:
        emoji = {"셔틀콕": '🏫 ', "한대앞역": '🚆 ', "예술인A": '🚍 ', "기숙사": '🏘️ ', "셔틀콕 건너편": '🏫 '}
        block_id = '5cc3dc8ee82127558b7e6eba'

        bus_to_come_dh, bus_to_come_dy, bus_to_come_c, now = depart_info
        # 도착정보를 응답으로 변환
        if dest_stop == '기숙사':
            result = '기숙사→셔틀콕,한대앞(직행)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n기숙사→셔틀콕,예술인(직행)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n기숙사→셔틀콕,한대앞,예술인(순환)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '셔틀콕':
            result = '셔틀콕→한대앞(직행)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n셔틀콕→예술인A(직행)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n셔틀콕→한대앞,예술인(순환)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '한대앞역':
            result = '한대앞→셔틀콕(직행)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
            result += '\n한대앞→예술인,셔틀콕(순환)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '예술인A':
            result = '예술인→셔틀콕\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        elif dest_stop == '셔틀콕 건너편':
            result = '셔틀콕 건너편→기숙사\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n'
        else:
            result = '잘못된 정류장 정보입니다.'
        server_answer = insert_text(result.strip())

    # 하단 버튼 추가
    reply = make_reply('🔍 정류장', f'{dest_stop} 정류장 정보입니다.', '5ebf702e7a9c4b000105fb25')
    response = insert_replies(server_answer, reply)
    reply = make_reply('🚫 오류제보', '셔틀 오류 제보하기', '5cc3fced384c5508fceec5bb')
    response = insert_replies(response, reply)

    for stop_name in emoji.keys():
        if stop_name != dest_stop:
            message = f"{stop_name}의 셔틀버스 도착 정보입니다"

            reply = make_reply(f'{emoji[stop_name]}{stop_name}', message, block_id)
            response = insert_replies(response, reply)

    return response


def make_answer_shuttle_stop_detail(user_answer):
    stop_list = {"셔틀콕": "shuttle", "셔틀콕 건너편": "shuttle", "한대앞역": "station", "예술인A": "terminal", "기숙사": "dormitory"}
    stop_view = {"shuttle": "http://kko.to/Kf-ZqboYH", "station": "http://kko.to/IyyXgzPDo",
                 "dormitory": "http://kko.to/vClEubBDj", "terminal": "http://kko.to/guG2uboYB"}
    stop_name = user_answer.split('정류장 정보입니다')[0].strip()
    stop_key = stop_list[stop_name]
    bool_semester, bool_weekend, bus_to_come_dh, bus_to_come_dy, bus_to_come_c = get_first_last_departure(stop_name)
    if bool_semester == 'halt':
        result_str = '당일은 운행하지 않습니다.'
    else:
        result_str = '첫,막차 정보입니다.\n'
        if stop_name == '기숙사' or stop_name == '셔틀콕':
            if bus_to_come_dh:
                result_str += f'한대앞 직행 {bus_to_come_dh[0].strftime("%H:%M")}/{bus_to_come_dh[-1].strftime("%H:%M")}\n'
            if bus_to_come_dy:
                result_str += f'예술인A 직행 {bus_to_come_dy[0].strftime("%H:%M")}/{bus_to_come_dy[-1].strftime("%H:%M")}\n'
            if bus_to_come_c:
                result_str += f'순환버스 {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
        elif stop_name == '한대앞역':
            if bus_to_come_dh:
                result_str += f'셔틀콕 직행 {bus_to_come_dh[0].strftime("%H:%M")}/{bus_to_come_dh[-1].strftime("%H:%M")}\n'
            if bus_to_come_c:
                result_str += f'순환버스 {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
        elif stop_name == '예술인A':
            if bus_to_come_c:
                result_str += f'셔틀콕 직행 {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
        elif stop_name == '셔틀콕 건너편':
            if bus_to_come_c:
                result_str += f'기숙사 직행 {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
        else:
            result_str = '잘못된 정류장 정보입니다.\n해당 화면을 보실 경우 관리자에게 알려주십시오.'
    response = insert_card(f'{stop_name} 정류장 정보', result_str.strip())
    # response = insert_button(response, '🗺️ 카카오맵에서 보기', stop_map[stop_key])
    response = insert_button(response, '👀 로드뷰로 보기', stop_view[stop_key])
    return response
