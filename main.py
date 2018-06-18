import os, sqlite3
from flask import Flask, request, jsonify
from handler import handler


app = Flask(__name__)
button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
find_user = 'select * from user where user_id=?'
insert_user = 'insert into user (user_id, campus) values (?,?)'
change_campus =  'update user set campus = ? where user_id = ?'
delete = 'delete from user where user_id = ?'


@app.route('/keyboard')
def keyboard():
    data = {"type": "buttons", "buttons": button_list}
    return jsonify(data)


@app.route('/message', methods=['POST'])
def message():
    received_data = request.get_json()
    content = received_data['content']
    user = received_data['user_key']
    conn = sqlite3.connect('user.db', timeout=30)
    cur = conn.cursor()
    cur.execute(find_user, (user,))
    result = cur.fetchall()
    if result == []:
        cur.execute(insert_user, (user, 1))
        campus = 1
    else:
        campus = result[0][1]
    if content == "캠퍼스 변경":
        if campus == 1:
            string = '서울캠퍼스로 변경되었습니다.'
            button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
            cur.execute(change_campus, (2, user))
        elif campus == 2:
            button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]
            string = 'ERICA 캠퍼스로 변경되었습니다.'
            cur.execute(change_campus, (1, user))
    conn.commit()
    cur.close()
    conn.close()
    if content != "캠퍼스 변경":
        string, button_list = handler(content, campus)
    if button_list != []:
        data = {"message": {"text": string}, "keyboard": {"type": "buttons", "buttons": button_list}}
    else:
        data = {"message": {"text": string}, "keyboard": {"type": "text"}}
    return jsonify(data)

@app.route('/chat_room/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('user.db', timeout=30)
    cur = conn.cursor()
    cur.execute(delete, (str(user_id),))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
