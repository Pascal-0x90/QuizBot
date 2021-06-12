#!/usr/bin/env python3

# Standard Imports
import os
import sys
import string
import logging

# Third-party Imports
import discord
from discord.ext import commands

# Constants
B_LOG = logging.getLogger('quizbot')
LANGUAGE = "english"
STARTX = ["Quiz"]

bot = commands.Bot(
    command_prefix="!",
    description="A bot so you can not be dumb.",
    pm_help=True
)

DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']

# Initial Start Methods
def main():
    # Initialize the logger
    B_LOG.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    B_LOG.addHandler(ch)

    # Load our extensions
    for ext in STARTX:
        try:
            bot.load_extension("cogs." + ext)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"Failed to load extension {exc}")

    # Start the bot!
    bot.run(DISCORD_BOT_TOKEN)

# Command Parsing
@bot.event
async def on_message(message):
    # Assure no loopback
    if message.author == bot.user:
        return

    # What is our bot currently doing?
    await bot.change_presence(activity=discord.Game(name="Playing with your feelings."))

    # Remove the bot's name from the message
    if bot.user in message.mentions:
        directed = True
        AT_BOT = "<@" + bot.user.id + ">"
        plain_message = message.content[len(AT_BOT):]
    else:
        directed = False
        plain_message = message.content

    # Clean up message
    plain_message = plain_message.lower().strip(string.whitespace)

    # Execute command
    await bot.process_commands(message)

# Administrative events
@bot.event
async def on_ready():
    B_LOG.info('Logged in as %s, id: %s', bot.user.name, bot.user.id)


@bot.event
async def on_server_join(server):
    B_LOG.info('Bot joined: %s', server.name)


@bot.event
async def on_server_remove(server):
    B_LOG.info('Bot left: %s', server.name)


@bot.event
async def on_command_completion(ctx):
    B_LOG.info('parsed command:%s', ctx.message.content)


@bot.command(pass_context=True)
async def killbot(ctx):
    print("Shutting down!")
    await bot.say("Shutting down.")
    await bot.close()

if __name__ == '__main__':
    main()
