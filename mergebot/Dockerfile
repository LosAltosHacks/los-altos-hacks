# TODO: why does this break if I specify the patch version of python
FROM python:3.8-alpine3.10
RUN apk update && apk add \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    git \
    ;

WORKDIR /opt/mergebot
RUN mkdir -p /opt/mergebot

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./src/main.py"]
