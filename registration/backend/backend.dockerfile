FROM python:3.7-alpine3.8

COPY ./app /app

EXPOSE 80

CMD ["python", "/app/src/main.py"]
