import sqlite3
def phone_seoul(content):
    conn = sqlite3.connect('phone_seoul.db')
    cur = conn.cursor()
    sql = "select * from phone"
    cur.execute(sql)
    phones = cur.fetchall()
    total_phone=[]
    for x in phones:
        ok = 1
        for y in content:
            if y in x[0]:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x[0],x[1]]
            total_phone += [phone_list]
    cur.close()
    conn.close()
    string = ''
    if total_phone != []:
        for x in total_phone:
            string += x[0] + ' 02-2220-' + x[1] + '\n'
    else:
        string = '검색된 전화번호가 없습니다.'
    return string


def phone_erica(content):
    if content == "경영":
        return "경영학과는 검색이 불가능합니다."
    conn = sqlite3.connect('phone.db')
    cur = conn.cursor()
    sql = "select * from inschool"
    cur.execute(sql)
    phones = cur.fetchall()
    total_phone=[]
    for x in phones:
        ok = 1
        for y in content:
            if y in x[0]:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x[0],x[1]]
            total_phone += [phone_list]
    sql = "select * from cafe"
    cur.execute(sql)
    phones = cur.fetchall()
    for x in phones:
        ok = 1
        for y in content:
            if y in x[0]:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x[0],x[1]]
            total_phone += [phone_list]
    sql = "select * from pub"
    cur.execute(sql)
    phones = cur.fetchall()
    for x in phones:
        ok = 1
        for y in content:
            if y in x[0]:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x[0],x[1]]
            total_phone += [phone_list]
    sql = "select * from restaurant"
    cur.execute(sql)
    phones = cur.fetchall()
    for x in phones:
        ok = 1
        for y in content:
            if y in x[0]:
                continue
            else:
                ok = 0
                break
        if ok == 1:
            phone_list = [x[0],x[1]]
            total_phone += [phone_list]
    cur.close()
    conn.close()
    string = ''
    if total_phone != []:
        for x in total_phone:
            string += x[0] + ' ' + x[1] + '\n'
    else:
        string = '검색된 전화번호가 없습니다.'
    return string