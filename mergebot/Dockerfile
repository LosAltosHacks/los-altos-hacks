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

COPY ./src ./src

ARG environment=dev

# ensure environment has a "good" value
RUN [[ "$environment" == "dev" || "$environment" == "prod" ]]

# Include cert and secret in dev env only
COPY ffmergebot.private-key.pem .
COPY webhook-secret.txt .
RUN if [[ "$environment" != "dev" ]]; then rm ffmergebot.private-key.pem webhook-secret.txt; fi


ENV ENVIRONMENT $environment

EXPOSE 8000

ENTRYPOINT ["python", "./src/main.py"]
