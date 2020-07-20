import json, requests, os
def phonesearch(content):
    total_phone=[]
    if content == "경영":
        return "경영학과는 검색이 불가능합니다."
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/phonenum/inschool.json') as json_file:
            json_data = json.load(json_file)
    except:
        link = 'https://raw.githubusercontent.com/jil8885/ERICA_api/master/inschool.json'
        response = requests.get(link)
        json_data = response.json()
    for x in json_data.keys():
        ok = 1
        for y in content:
            if y in x:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x, json_data[x]["phone"]]
            total_phone += [phone_list]
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/phonenum/cafe.json') as json_file:
            json_data = json.load(json_file)
    except:
        link = 'https://raw.githubusercontent.com/jil8885/ERICA_api/master/cafe.json'
        response = requests.get(link)
        json_data = response.json()
    for x in json_data.keys():
        ok = 1
        for y in content:
            if y in x:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x, json_data[x]["phone"]]
            total_phone += [phone_list]
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/phonenum/pub.json') as json_file:
            json_data = json.load(json_file)
    except:
        link = 'https://raw.githubusercontent.com/jil8885/ERICA_api/master/pub.json'
        response = requests.get(link)
        json_data = response.json()
    for x in json_data.keys():
        ok = 1
        for y in content:
            if y in x:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x, json_data[x]["phone"]]
            total_phone += [phone_list]
    try:
        with open(os.path.dirname(os.path.realpath(__file__)) + '/phoneNum/restaurant.json') as json_file:
            json_data = json.load(json_file)
    except:
        link = 'https://raw.githubusercontent.com/jil8885/ERICA_api/master/restaurant.json'
        response = requests.get(link)
        json_data = response.json()
    for x in json_data.keys():
        ok = 1
        for y in content:
            if y in x:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x, json_data[x]["phone"]]
            total_phone += [phone_list]
    string = ''
    if total_phone != []:
        for x in total_phone:
            string += x[0] + ' ' + x[1] + '\n'
    else:
        string = '검색된 전화번호가 없습니다.'
    return string.strip()
