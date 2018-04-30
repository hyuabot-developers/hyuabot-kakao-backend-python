import lxml, requests
from bs4 import BeautifulSoup

def weather_request(campus):
    if campus == 1:
        link = 'http://www.weather.go.kr/wid/queryDFSRSS.jsp?zone=4127153700'
    else:
        link = 'http://www.weather.go.kr/wid/queryDFSRSS.jsp?zone=1120056000'
    response = requests.get(link)
    soup = BeautifulSoup(response.content,'lxml-xml')
    weather_result = soup.findAll('data')
    now = weather_result[0]
    string = '현재 날씨: ' + now.find('wfKor').string +'\n'
    string += '온도: ' + str(int(float(now.find('temp').string))) + '도\n'
    string += now.find('wdKor').string + '풍: ' + str(int(float(now.find('ws').string))) + 'm/s\n'
    for weather in weather_result:
        if weather.find('hour').string == '12':
            string += '\n'
            if weather.find('day').string == '0':
                string += '오늘 날씨: ' + weather.find('wfKor').string +'\n'
            else:
                string += '내일 날씨: ' + weather.find('wfKor').string +'\n'
            string += '온도: ' + str(int(float(weather.find('temp').string))) + '도\n'
            string += weather.find('wdKor').string + '풍: ' + str(int(float(weather.find('ws').string))) + 'm/s\n'
            break
    if campus == 1:
        stn = '호수동'
    elif campus == 2:
        stn = '강변북로'
    link = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=US2a7bn1A3XMUfP%2FR0BRT22upj74Dt2SdSx4rs%2BAuICHKq39N9yqCBwzqik1FsjnjHxg9xAt1yQtBlEcxIgR9A%3D%3D&numOfRows=1&pageSize=1&pageNo=1&startPage=1&stationName=' + stn + '&dataTerm=DAILY&ver=1.3'
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'lxml-xml')
    pm10value = int(soup.find('pm10Value24').string)
    string += '\n미세먼지:'
    if pm10value <= 54:
        string += str(pm10value) +'(좋음)\n'
    elif pm10value <= 154:
        string += str(pm10value) +'(보통)\n'
    elif pm10value <= 254:
        string += str(pm10value) +'(민감군에 나쁨)\n'
    elif pm10value <= 354:
        string += str(pm10value) +'(나쁨)\n'
    elif pm10value <= 424:
        string += str(pm10value) +'(매우 나쁨)\n'
    else:
        string += str(pm10value) +'(위험)\n'
    try:
        pm25value = int(soup.find('pm25Value24').string)
        string += '초미세먼지: '
        if pm25value <= 12:
            string += str(pm25value) +'(좋음)\n'
        elif pm25value <= 35:
            string += str(pm25value) +'(보통)\n'
        elif pm25value <= 55:
            string += str(pm25value) +'(민감군에 나쁨)\n'
        elif pm25value <= 150:
            string += str(pm25value) +'(나쁨)\n'
        elif pm25value <= 250:
            string += str(pm25value) +'(매우 나쁨)\n'
        else:
            string += str(pm25value) +'(위험)\n'
    except:
        pass
    if string[-1] == '\n':
        string = string[:-1]
    return string


