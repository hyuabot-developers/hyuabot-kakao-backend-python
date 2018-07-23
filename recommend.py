import random, sqlite3
def recommend_bob():
    conn = sqlite3.connect('phone.db')
    cur = conn.cursor()
    sql = "select * from restaurant"
    cur.execute(sql)
    phones = cur.fetchall()
    result = phones.pop(random.randrange(len(phones)))
    string = '추천 가게:' + result[0] + '\n'
    string += '판매 메뉴:' + result[1] + '\n'
    string += '대략적인 위치:' + result[2] + '\n'
    string += '리뷰:' + result[3] + '\n'
    cur.close()
    conn.close()
    return string



def recommend_cafe():
    conn = sqlite3.connect('phone.db')
    cur = conn.cursor()
    sql = "select * from cafe"
    cur.execute(sql)
    phones = cur.fetchall()
    result = phones.pop(random.randrange(len(phones)))
    string = '추천 가게:' + result[0] + '\n'
    string += '판매 메뉴:' + result[1] + '\n'
    string += '대략적인 위치:' + result[2] + '\n'
    string += '리뷰:' + result[3] + '\n'
    cur.close()
    conn.close()
    return string

def mv_db():
    conn = sqlite3.connect('phone.db')
    conn2 = sqlite3.connect('recommend.db')
    cur = conn.cursor()
    cur2 = conn2.cursor()
    sql = "select * from restaurant"
    cur.execute(sql)
    result = cur.fetchall()
    sql = "insert into bob (store, phone, recommend) values (?, ?, ?)"
    for x in result:
        conn2.execute(sql, (x[0], x[1], 0,))
    conn2.commit()
    sql = "select * from cafe"
    cur.execute(sql)
    result = cur.fetchall()
    sql = "insert into cafe (store, phone, recommend) values (?, ?, ?)"
    for x in result:
        conn2.execute(sql, (x[0], x[1], 0,))
    conn2.commit()
    conn.close()
    conn2.close()
mv_db()