#!/usr/bin/env python3

import discord

def make_embed(title: str, msg):
    embed = discord.Embed(
        title=title
    )

    if isinstance(msg, list):
        embed.description = "\n".join(str(x) for x in msg)
    elif isinstance(msg, dict):
        for k, v in msg.items():
            embed.add_field(name=k, value=v, inline=False)
    else:
        embed.description = msg

    return embed
