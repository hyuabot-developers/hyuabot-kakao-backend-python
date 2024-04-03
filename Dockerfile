FROM python:3.12-bookworm

COPY . /

RUN pip install -U pip && \
    pip install --no-cache-dir -e /

WORKDIR /src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "38001"]