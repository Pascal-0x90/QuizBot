#!/bin/bash

# Need to export your token first
export DISCORD_BOT_TOKEN="token_here"

docker build . --build-arg DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN} -t quizbot; docker run quizbot
