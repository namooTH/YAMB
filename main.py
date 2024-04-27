import discord
import os
import logging
from discord.ext import commands
import asyncio

cogsfolder = "cogs"

#get bot token from file
token = open("token", "r").readline()

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
logging.basicConfig(level=logging.ERROR)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

async def load_extensions():
    for file in os.listdir(cogsfolder):
        if file.endswith(".py"):
            await client.load_extension(f"{cogsfolder}.{file[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(token)
asyncio.run(main())