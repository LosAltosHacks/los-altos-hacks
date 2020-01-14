# TODO: why does this break if I specify the patch version of python
FROM python:3.8-alpine3.10

RUN apk add --no-cache libffi-dev


WORKDIR /opt/registration
RUN mkdir -p /opt/registration

COPY requirements.txt .

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev make && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY ./app ./app

EXPOSE 8000

ENTRYPOINT ["python", "./app/src/main.py"]
