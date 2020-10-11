from transport.subway.get_info import get_subway_info, get_subway_timetable
from transport.shuttle.date import is_semester
from kakao.common.sender import *

import time


def make_answer_subway(campus, language="Korean") -> dict:

    _, is_weekend = is_semester()
    is_weekend = True if is_weekend == 'weekend' else False
    line_main = get_subway_info(campus)
    line_sub = get_subway_timetable(is_weekend)

    station_eng = {
        '한대앞': 'Hanyang Univ. Ansan', '중앙': 'Jungang', '고잔': 'Gojan', '초지': 'Choji', '안산': 'Ansan',
        '신길온천': 'SingilOncheon', '정왕': 'Jeongwang', '오이도': 'Oido', '달월': 'Dalwol', '월곶': 'Wolgot',
        '소래포구': 'Soraepogu', '인천논현': 'Incheonnonhyeon', '호구포': 'Hogupo', '상록수': 'Sangnoksu', '반월': 'Banwol',
        '대야미': 'Daeyami', '수리산': 'Surisan', '산본': 'Sanbon', '금정': 'Gumjeong', '범계': 'Beomgye', '평촌': 'Pyeongchon',
        '인덕원': 'Indeokwon', '정부과천청사': 'Government Complex Gwacheon', '과천': 'Gwacheon', '사리': 'Sari', '야목': 'Yamok',
        '어천': 'Eocheon', '오목천': 'Ohmokcheon', '고색': 'Gosaek', '수원': 'Suwon', '매교': 'Maegyo', '수원시청': 'Suwon City Hall',
        '매탄권선': 'Maetankwonseon', '성수': 'Seongsu', '신도림': 'Shindorim', '서울대입구': 'Seoul Univ', '홍대입구': 'Hongik Univ.',
        '을지로입구': 'Euljiro 1(il)-ga', '당고개': 'Danggogae', '노원': 'Nowon', '한성대입구': 'Hansung Univ', '사당': 'Sadang',
        '왕십리':'Wangsimni', '죽전': 'Jukjeon', '신인천': 'Incheon', '상왕십리': 'Sangwangsimni', '신당': 'Sindang',
        '동대문역사문화공원':'DDP', '을지로 4가': 'Euljiro 4(sa)-ga', '을지로 3가': 'Euljiro 3(sam)-ga', '뚝섬': 'Ddukseom',
        '건대입구': 'Geonguk Univ','구의': 'Guui', '강변': 'Gangbyeon', '잠실나루': 'Jamsilnaru', '잠실': 'Jamsil'
    }

    status_eng = {'진입': 'Around at', '도착': 'Arrived at', '출발': 'Departed from', '전역출발': 'Departed from previous stn',
                  '전역진입': 'Around at prev stn', '전역도착': 'Arrived at prev stn', '운행중': 'Moving to'}

    if campus:
        if language == "Korean":
            result = '2호선(한양대역/내선)\n'
            if line_main['up']:
                end_station, pos, remained_time, status = line_main['up'][0]
                if '전역' in status:
                    result += f'{end_station}행 {status} {remained_time//60}분 후 도착\n'
                else:
                    result += f'{end_station}행 {pos} {remained_time//60}분 후 도착\n'
            else:
                result += '내선 방면 열차가 없습니다\n\n'
            result += '\n2호선(한양대역/외선)\n'
            if line_main['down']:
                end_station, pos, remained_time, status = line_main['down'][0]
                if '전역' in status:
                    result += f'{end_station}행 {status} {remained_time//60}분 후 도착\n'
                else:
                    result += f'{end_station}행 {pos} {remained_time//60}분 후 도착\n'
            else:
                result += '외선 방면 열차가 없습니다\n'
        else:
            result = 'Line no.2(Inner)\n'
            if line_main['up']:
                end_station, pos, remained_time, status = line_main['up'][0]
                result += f'→ {station_eng[end_station]} {int(remained_time // 60)} mins left\n'
            else:
                result += 'There is no more train for inner line\n'
            result += '\nLine no.2(Outer)\n'
            if line_main['down']:
                end_station, pos, remained_time, status = line_main['down'][0]
                result += f'→ {station_eng[end_station]} {int(remained_time // 60)} mins left\n'
            else:
                result += 'There is no more train for outer line\n'
    else:
        if language == "Korean":
            result = '4호선(한대앞역)\n'
            if line_main['up']:
                end_station, pos, remained_time, status = line_main['up'][0]
                if '전역' in status:
                    result += f'{end_station}행 {status} {int(remained_time)}분 후 도착\n'
                else:
                    result += f'{end_station}행 {pos} {int(remained_time)}분 후 도착\n'
            else:
                result += '당고개 방면 열차가 없습니다\n'
            if line_main['down']:
                end_station, pos, remained_time, status = line_main['down'][0]
                if '전역' in status:
                    result += f'{end_station}행 {status} {int(remained_time)}분 후 도착\n'
                else:
                    result += f'{end_station}행 {pos} {int(remained_time)}분 후 도착\n\n'
            else:
                result += '오이도 방면 열차가 없습니다\n'
            result += '\n수인선(한대앞역)\n'
            if line_sub['up']:
                end_station, arrival_time = line_sub['up'][0]['endStn'], line_sub['up'][0]['time']
                print(arrival_time)
                result += f'{end_station}행 {arrival_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '인천 방면 열차가 없습니다\n'
            if line_sub['down']:
                end_station, arrival_time = line_sub['down'][0]['endStn'], line_sub['down'][0]['time']
                result += f'{end_station}행 {arrival_time.strftime("%H시 %M분")} 도착\n'
            else:
                result += '왕십리/수원 방면 열차가 없습니다\n'
        else:
            result = 'Line No.4\n'
            if line_main['up']:
                end_station, pos, remained_time, status = line_main['up'][0]
                result += f'→ {station_eng[end_station]} {int(remained_time)}mins left\n'
            else:
                result += 'There is no more train bound for Danggogae(Seoul)\n'
            if line_main['down']:
                end_station, pos, remained_time, status = line_main['down'][0]
                result += f'→ {station_eng[end_station]} {int(remained_time)} mins left\n'
            else:
                result += 'There is no more train bound for Oido\n'
            result += '\nSuinbundang Line\n'
            if line_sub['up']:
                end_station, arrival_time = line_sub['up'][0]['endStn'], line_sub['up'][0]['time']
                result += f'→ {station_eng[end_station]} Arriving at {arrival_time.strftime("%H:%M")}\n'
            else:
                result += 'There is no more train bound for Incheon\n'
            if line_sub['down']:
                end_station, arrival_time = line_sub['down'][0]['endStn'], line_sub['down'][0]['time']
                result += f'→ {station_eng[end_station]} Arriving at {arrival_time.strftime("%H:%M")}\n'
            else:
                result += 'There is no more train bound for Wangsimni/Suwon\n'

    response = insert_text(result.strip())

    return response
