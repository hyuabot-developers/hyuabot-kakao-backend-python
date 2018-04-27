import lxml, requests
from bs4 import BeautifulSoup
from datetime import datetime
# stn_list = ['216000070','216000141','216000383','216000379','216000719']
# route_list = {'216000068':9,'216000026':3100,'216000043':3101,'216000061':3102,'241006370':700,'216000001':707,'217000014':110,'200000015':909,'241006320':737,'241006360':8467,'217000007':99,'216000011':55,'216000016':62,'216000012':22,'216000036':31,'216000004':70}
def bus_request(content):
    if content == "시내":
        string = '10-1번 (게스트하우스 > 상록수역)\n'
        stn = '216000379'
        route = '216000068'
        string += bus_request_api(stn, route)
        string += '\n\n62번 (꿈의 교회 > 중앙역)\n'
        stn = '216000152'
        route = '216000016'
        string += bus_request_api(stn, route)
    elif content == "강남":
        string = '700번 (한양대입구)\n'
        route = '241006370'
        stn = '216000070'
        string += bus_request_api(stn, route)
        string += '\n\n3100번 (한양대정문)\n'
        route = '216000026'
        stn = '216000719'
        string += bus_request_api(stn, route)
        string += '\n\n3101번 (한양대정문)\n'
        route = '216000043'
        string += bus_request_api(stn, route)
        string += '\n\n3102번 (한양대게스트하우스)\n'
        route = '216000061'
        stn = '216000379'
        string += bus_request_api(stn, route)
    elif content == "수원/성남":
        stn = '216000070'
        string = '8467번 (성남/모란)\n'
        route = '241006360'
        string += bus_request_api(stn, route)
        string += '\n\n737번 (수원)\n'
        route = '241006320'
        string += bus_request_api(stn, route)
        string += '\n\n110번 (수원)\n'
        route = '217000014'
        string += bus_request_api(stn, route)
        string += '\n\n707번 (수원)\n'
        route = '216000001'
        string += bus_request_api(stn, route)
        string += '\n\n909번 (수원)\n'
        route = '200000015'
        string += bus_request_api(stn, route)    
    return string


def bus_request_api(stn, route):
    link = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey=1234567890&routeId=' + route + '&stationId=' + stn
    response = requests.get(link)
    soup = BeautifulSoup(response.content,'lxml-xml')
    arrival_result = soup.findAll('busArrivalItem')
    now = datetime.now()
    if len(arrival_result) == 0:
        return "도착 예정인 버스가 없습니다."
    else:
        string = '이번 버스:'
        if (route == '216000068' or route == '216000061') and arrival_result[0].find('locationNo1').string == '7':
            string += '회차점 대기중입니다.'
            return string
        string += arrival_result[0].find('locationNo1').string + '번째 전/'
        string += arrival_result[0].find('predictTime1').string + '분 후 도착'
        minute = int(arrival_result[0].find('predictTime1').string)
        if route == '241006370':
            arrival_togo = 65
        elif route == '216000026':
            arrival_togo = 82
        elif route == '216000043':
            arrival_togo = 86
        elif route == '216000061':
            arrival_togo = 75
        try:
            arrival_time = minute + arrival_togo
            arrival_minute = now.minute + arrival_time
            arrival_hour = now.hour + arrival_minute // 60
            arrival_minute = arrival_minute % 60
            string += '\n강남역 ' + str(arrival_hour) + '시 '+ str(arrival_minute) + '분 도착 예정\n'
        except:
            pass
        if arrival_result[0].find('locationNo2').string != None:
            string += '\n다음 버스:'
            if (route == '216000068' or route == '216000061') and arrival_result[0].find('locationNo2').string == '7':
                string += '회차점 대기중입니다.'
                return string
            string += arrival_result[0].find('locationNo2').string + '번째 전/'
            string += arrival_result[0].find('predictTime2').string + '분 후 도착'
            minute = int(arrival_result[0].find('predictTime2').string)
            if route == '241006370':
                arrival_togo = 65
            elif route == '216000026':
                arrival_togo = 82
            elif route == '216000043':
                arrival_togo = 86
            elif route == '216000061':
                arrival_togo = 75
            try:
                arrival_time = minute + arrival_togo
                arrival_minute = now.minute + arrival_time
                arrival_hour = now.hour + arrival_minute // 60
                arrival_minute = arrival_minute % 60
                string += '\n강남역 ' + str(arrival_hour) + '시 '+ str(arrival_minute) + '분 도착 예정\n'
            except:
                pass
    if string[-1] == '\n':
        string = string[:-1]
    return string

