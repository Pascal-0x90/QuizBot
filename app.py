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
STARTX = ["quiz"]

bot = commands.Bot(
    command_prefix="#",
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
            pass
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




