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
    if string[-1] == '\n':
        string = string[:-1]
    return string