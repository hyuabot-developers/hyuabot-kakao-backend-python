from library.reading_room import get_reading_room_seat
from kakao.common.sender import *


def make_answer_reading_room_info(user_answer=''):
    result, active_room = get_reading_room_seat(user_answer)
    if user_answer:
        result_str = f'{user_answer}\n'
        result_str += f'총 좌석:{result["activeTotal"]}\n'
        result_str += f'사용중:{result["occupied"]}\n'
        result_str += f'잔여 좌석:{result["available"]}\n'
    else:
        result_str = 'ERICA 캠퍼스 열람실 잔여좌석\n'
        for room in result:
            result_str += f'{room["name"]} {room["available"]}석\n'
    response = insert_text(result_str.strip())

    block_id = '5e0df82cffa74800014bc838'
    for lib in active_room:
        reply = make_reply(f'📖 {lib}', f"{lib}의 좌석정보입니다.", block_id)
        response = insert_replies(response, reply)
    return response
