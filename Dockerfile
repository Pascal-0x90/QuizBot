FROM python:3.9-slim

ADD VERSION .

COPY . /app
WORKDIR /app

RUN apt update
RUN apt install git -y
RUN pip install -r requirements.txt

RUN useradd -ms /bin/bash basic
USER basic

ARG DISCORD_BOT_TOKEN
ENV DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN

CMD ["python3","app.py"]
