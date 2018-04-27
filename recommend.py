import random, sqlite3
def recommend_bob():
    conn = sqlite3.connect('recommend.db')
    cur = conn.cursor()
    sql = "select * from bob"
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
    conn = sqlite3.connect('recommend.db')
    cur = conn.cursor()
    sql = "select * from cafe"
    cur.execute(sql)
    phones = cur.fetchall()

recommend_bob()