import discord
from discord.ext import commands
import os
import logging
import asyncio

logging.basicConfig(level=logging.ERROR)
class bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        command_prefix='!'
        super().__init__(command_prefix=command_prefix, intents=intents)

        #get bot token from file
        self.token = open("token.yml", "r").readline()
        self.cogsfolder = "cogs"

    async def load_extensions(self):
        for file in os.listdir(self.cogsfolder):
            if file.endswith(".py"): 
                await self.load_extension(f"{self.cogsfolder}.{file[:-3]}")

    async def test(self):
        pass
bot = bot()

@bot.command(name="sync") 
async def sync(ctx):
    if ctx.author.id == 899113384660844634: # add ur own id 
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")

@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user}')

async def main():
    async with bot:
        await bot.load_extensions()
        await bot.start(bot.token)
asyncio.run(main())