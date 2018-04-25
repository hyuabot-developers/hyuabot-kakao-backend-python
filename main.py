import os, sqlite3
from flask import Flask, request, jsonify


app = Flask(__name__)
button_list = ["학식", "교통", "날씨", "기타 기능", "캠퍼스 변경"]


@app.route('/keyboard')
def keyboard():
    global button_list
    data = {"type": "buttons", "buttons": button_list}
    return jsonify(data)


@app.route('/message', method=['POST'])
def message():
    global button_list
    received_data = request.get_json()
    content = received_data['content']
    user = received_data['user_key']
    string = content
    data = {"message": {"text": string}, "keyboard": {"type": "buttons", "buttons": button_list}}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')