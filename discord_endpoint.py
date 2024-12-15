from __future__ import annotations

import os

import discord
from dotenv import load_dotenv

from src.heroes_training_calculator.calculate import calculate
from src.heroes_training_calculator.config import Config

load_dotenv()
intents = discord.Intents.all()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content: str = message.content
    content = content.removeprefix("!debug")
    try:
        content = content.strip()
        parts = content.split()
        config = Config(**dict(part.split("=", maxsplit=1) for part in parts))
        await message.channel.send(calculate(config))
    except Exception as e:
        if message.content.startswith("!debug"):
            await message.channel.send(e)
        return


if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
