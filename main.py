import os, sqlite3
from flask import Flask, request, jsonify
from handler import handler


app = Flask(__name__)
button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
find_user = 'select * from user where user_id=?'
insert_user = 'insert into user (user_key, campus) values (?,?)'


@app.route('/keyboard')
def keyboard():
    global button_list
    data = {"type": "buttons", "buttons": button_list}
    return jsonify(data)


@app.route('/message', methods=['POST'])
def message():
    global button_list, find_user
    received_data = request.get_json()
    content = received_data['content']
    user = received_data['user_key']
    conn = sqlite3.connect('user.db', timeout=30)
    cur = conn.cursor()
    cur.execute(find_user, (user))
    if cur.fetchall() == []:
        cur.execute(insert_user, (user, 1))
        campus = 1
    else:
        campus = cur.fetchall()[0][1]
    string, button_list = handler(content, campus)
    data = {"message": {"text": string}, "keyboard": {"type": "buttons", "buttons": button_list}}
    cur.close()
    conn.close()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')