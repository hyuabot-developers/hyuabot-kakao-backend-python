from transport.shuttle.get_info import get_departure_info, get_first_last_departure
from kakao.common.sender import *


def make_answer_shuttle_main(language='Korean'):
    if language == 'Korean':
        response = insert_text('원하시는 셔틀 정류장을 선택해주세요.')
        bus_stop = ['셔틀콕', '한대앞역', '예술인A', '기숙사', '셔틀콕 건너편']
    else:
        response = insert_text('Choose shuttle bus stop where you want.')
        bus_stop = ['Shuttlecock', 'Station', 'Terminal', 'Dormitory', 'Shuttlecock(Oppo)']
    emoji = ['🏫', '🚆', '🚍', '🏘️', '🏫']
    block_id = '5cc3dc8ee82127558b7e6eba'
    for x in range(len(bus_stop)):
        reply = make_reply(f'{emoji[x]} {bus_stop[x]}', f'{emoji[x]} {bus_stop[x]}', block_id)
        response = insert_replies(response, reply)

    return response


def make_answer_shuttle_depart_info(user_answer, language='Korean') -> str:
    block_id = '5cc3dc8ee82127558b7e6eba'
    if '의 셔틀버스 도착 정보입니다' in user_answer:
        dest_stop = user_answer.split('의 셔틀버스 도착 정보입니다')[0].strip()
    elif 'Departure info at' in user_answer:
        dest_stop = user_answer.split(' ')[-1].strip()
    else:
        dest_stop = user_answer[2:].strip()
    depart_info = get_departure_info(dest_stop)

    # 운행 중지 일자 일 때,
    if depart_info == '오늘 셔틀 운행을 하지 않습니다.':
        if language == 'Korean':
            server_answer = insert_text(depart_info)
        else:
            server_answer = insert_text('Today is no shuttle bus')
    else:
        if language == 'Korean':
            emoji = {"셔틀콕": '🏫 ', "한대앞역": '🚆 ', "예술인A": '🚍 ', "기숙사": '🏘️ ', "셔틀콕 건너편": '🏫 '}
        else:
            emoji = {"Shuttlecock": '🏫 ', "Station": '🚆 ', "Terminal": '🚍 ', "Dormitory": '🏘️ ',
                     'Shuttlecock(Oppo)': '🏫 '}
        block_id = '5cc3dc8ee82127558b7e6eba'
        bus_to_come_dh, bus_to_come_dy, bus_to_come_c, now = depart_info
        # 도착정보를 응답으로 변환
        if dest_stop == '기숙사' or dest_stop == 'Dormitory':
            result = '기숙사→셔틀콕,한대앞(직행)\n' if language == 'Korean' else 'Dorm→Station(Direct)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
            result += '\n기숙사→셔틀콕,예술인(직행)\n' if language == 'Korean' else '\nDorm→Terminal(Direct)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
            result += '\n기숙사→셔틀콕,한대앞,예술인(순환)\n' if language == 'Korean' else '\nDorm→Subway/Terminal(Cycle)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
        elif dest_stop == '셔틀콕' or dest_stop == 'Shuttlecock':
            result = '셔틀콕→한대앞(직행)\n' if language == 'Korean' else 'Shuttlecock→Subway(Direct)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
            result += '\n셔틀콕→예술인A(직행)\n' if language == 'Korean' else '\nShuttlecock→Terminal(Direct)\n'
            if bus_to_come_dy:
                for depart_time in bus_to_come_dy:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
            result += '\n셔틀콕→한대앞,예술인(순환)\n' if language == 'Korean' else '\nShuttlecock→Stn,Terminal(Cycle)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
        elif dest_stop == '한대앞역' or dest_stop == 'Station':
            result = '한대앞→셔틀콕(직행)\n' if language == 'Korean' else 'Subway→School(Direct)\n'
            if bus_to_come_dh:
                for depart_time in bus_to_come_dh:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
            result += '\n한대앞→예술인,셔틀콕(순환)\n' if language == 'Korean' else '\nSubway→Terminal/School(Cycle)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
        elif dest_stop == '예술인A' or dest_stop == 'Terminal':
            result = '예술인→셔틀콕\n' if language == 'Korean' else 'Terminal→School(Cycle)\n'
            if bus_to_come_c:
                for depart_time in bus_to_come_c:
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
        elif dest_stop == '셔틀콕 건너편' or dest_stop == 'Shuttlecock(Oppo)':
            result = '셔틀콕 건너편→기숙사\n' if language == 'Korean' else 'Other side of Shuttlecock→Dorm(Cycle)\n'
            shuttle_list = bus_to_come_dh
            shuttle_list.extend(bus_to_come_dy)
            shuttle_list.extend(bus_to_come_c)
            shuttle_list = sorted(shuttle_list, key=lambda x: x)
            if shuttle_list:
                depart_time = shuttle_list[0]
                if language == 'Korean':
                    result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                else:
                    result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
                if len(shuttle_list) > 1:
                    depart_time = shuttle_list[1]
                    if language == 'Korean':
                        result += f'{depart_time.strftime("%H시 %M분")} 출발({(depart_time - now).seconds // 60}분 후)\n'
                    else:
                        result += f'Depart at {depart_time.strftime("%H:%M")} ({(depart_time - now).seconds // 60}mins later)\n'
            else:
                result += '도착 예정인 버스가 없습니다.\n' if language == 'Korean' else 'There is no more bus to depart\n'
        else:
            result = '잘못된 정류장 정보입니다.' if language == 'Korean' else 'Error!'

        result += "\n도착 정보는 시간표 기반으로 제공함으로 미리 정류장에서 기다리는 것을 권장합니다.\n" if language == "Korean" else "\nPlz be at bus stop earlier than time\n"
        server_answer = insert_text(result.strip())

    # 하단 버튼 추가
    if language == 'Korean':
        reply = make_reply('🔍 정류장', f'{dest_stop} 정류장 정보입니다.', '5ebf702e7a9c4b000105fb25')
    else:
        reply = make_reply('🔍 Stop Detail', f'About {dest_stop}', '5ebf702e7a9c4b000105fb25')
    response = insert_replies(server_answer, reply)

    if language == 'Korean':
        reply = make_reply('🚫 오류제보', '셔틀 오류 제보하기', '5cc3fced384c5508fceec5bb')
    else:
        reply = make_reply('🚫 Error Report', 'Error Report', '5cc3fced384c5508fceec5bb')
    response = insert_replies(response, reply)

    if language == 'Korean':
        for stop_name in emoji.keys():
            if stop_name != dest_stop:
                message = f"{stop_name}의 셔틀버스 도착 정보입니다"

                reply = make_reply(f'{emoji[stop_name]}{stop_name}', message, block_id)
                response = insert_replies(response, reply)
    else:
        for stop_name in emoji.keys():
            if stop_name != dest_stop:
                message = f"Departure info at {stop_name}"

                reply = make_reply(f'{emoji[stop_name]}{stop_name}', message, block_id)
                response = insert_replies(response, reply)

    return response


def make_answer_shuttle_stop_detail(user_answer, language='Korean'):
    if language == 'Korean':
        stop_list = {"셔틀콕": "shuttle", "셔틀콕 건너편": "shuttle", "한대앞역": "station", "예술인A": "terminal", "기숙사": "dormitory"}
    else:
        stop_list = {"Shuttlecock": "shuttle", "Shuttlecock(Oppo)": "shuttle", "Station": "station",
                     "Terminal": "terminal", "Dormitory": "dormitory"}
    stop_view = {"shuttle": "http://kko.to/Kf-ZqboYH", "station": "http://kko.to/IyyXgzPDo",
                 "dormitory": "http://kko.to/vClEubBDj", "terminal": "http://kko.to/guG2uboYB"}

    if language == 'Korean':
        stop_name = user_answer.split('정류장 정보입니다')[0].strip()
    else:
        stop_name = user_answer.split(' ')[1].strip()
    stop_key = stop_list[stop_name]
    bool_semester, bool_weekend, bus_to_come_dh, bus_to_come_dy, bus_to_come_c = get_first_last_departure(stop_name)
    if bool_semester == 'halt':
        if language == 'Korean':
            result_str = '당일은 운행하지 않습니다.'
        else:
            result_str = 'Shuttle is not working today'
    else:
        if language == 'Korean':
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
        else:
            result_str = 'Info about first/last bus\n'
            if stop_name == 'Dormitory' or stop_name == 'Shuttlecock':
                if bus_to_come_dh:
                    result_str += f'Station(Direct) {bus_to_come_dh[0].strftime("%H:%M")}/{bus_to_come_dh[-1].strftime("%H:%M")}\n'
                if bus_to_come_dy:
                    result_str += f'Terminal(Direct) {bus_to_come_dy[0].strftime("%H:%M")}/{bus_to_come_dy[-1].strftime("%H:%M")}\n'
                if bus_to_come_c:
                    result_str += f'Cycle {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
            elif stop_name == 'Station':
                if bus_to_come_dh:
                    result_str += f'School(Direct) {bus_to_come_dh[0].strftime("%H:%M")}/{bus_to_come_dh[-1].strftime("%H:%M")}\n'
                if bus_to_come_c:
                    result_str += f'Cycle {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
            elif stop_name == 'Terminal':
                if bus_to_come_c:
                    result_str += f'School(Direct) {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
            elif stop_name == 'Shuttlecock(Oppo)':
                if bus_to_come_c:
                    result_str += f'Residence {bus_to_come_c[0].strftime("%H:%M")}/{bus_to_come_c[-1].strftime("%H:%M")}\n'
            else:
                result_str = 'Error happened.\nPlease report to manager when you see this display.'
    if language == 'Korean':
        response = insert_card(f'{stop_name} 정류장 정보', result_str.strip())
        response = insert_button(response, '👀 로드뷰로 보기', stop_view[stop_key])
    else:
        response = insert_card(f'About {stop_name}', result_str.strip())
        response = insert_button(response, '👀 Road View', stop_view[stop_key])
    return response
