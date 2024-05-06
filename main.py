import discord
from discord.ext import commands
import os
import logging
import asyncio
import wavelink

logging.basicConfig(level=logging.ERROR)
class bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        command_prefix='!'
        super().__init__(command_prefix=command_prefix, intents=intents)

        #get bot token from file
        self.token = open("token.yml", "r").readline()
        self.cogsfolder = "cogs"

        #stuff that should not be reset after cog reload
        self.music_queue = {}

    async def load_extensions(self):
        for file in os.listdir(self.cogsfolder):
            if file.endswith(".py"): 
                await self.load_extension(f"{self.cogsfolder}.{file[:-3]}")

    async def setupwavelink(self):
        node: wavelink.Node = wavelink.Node(uri='https://lavalink4.alfari.id:443', password='catfein')
        #node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.Pool.connect(client=self, nodes=[node])
bot = bot()

@bot.command()
async def reload(ctx, cog):
    if ctx.author.id == 899113384660844634: # add ur own id 
        await bot.reload_extension(f"{bot.cogsfolder}.{cog}")
        await ctx.send(f"Reloaded {cog}")

@bot.command()
async def sync(ctx):
    if ctx.author.id == 899113384660844634: # add ur own id 
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} command(s).")

@bot.listen()
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.setupwavelink()

async def main():
    async with bot:
        await bot.load_extensions()
        await bot.start(bot.token)
asyncio.run(main())