FROM python:3.8.12-alpine3.15
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bitbucket-google-chat-notifications/ /app/

ENV FLASK_APP server.py

ENTRYPOINT [ "gunicorn", "-w", "2", "-b", ":5000", "server:app"]
