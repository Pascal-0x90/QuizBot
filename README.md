# QuizBot

## Description

In general, this bot is just a simple Discord python quiz bot.
Checkout the `quizzes` folder for an example of how one should
formulate their JSON quiz. 


## Future Work
Currently, it is not that robust to where you can have more than 
4 potential answers. In the future, I plan to make this more
robust. Right now I just wanted to study. 

## General Operation

You can use the Docker container or use it from the command line
like so:

```console
DISCORD_BOT_TOKEN="yourtokenhere" python ./app.py
```

Which then will load up the bot using your token. Some key things
to keep in mind:

- You can change the command prefix in `app.py`.
- You can add more cogs for different things (yay cogs)

## Thanks
This project is created with the help of these resources:
- https://github.com/pknull/pk.shado
- https://discordpy.readthedocs.io/
