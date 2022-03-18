FROM python:3.10.2-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
WORKDIR /code/src

CMD ["hypercorn", "--bind", "0.0.0.0:8081", "app.hyuabot.kakao.main:app"]
