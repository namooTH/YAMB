import wavelink
import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
from wavelink import Queue

from time import strftime
from time import gmtime

from io import BytesIO
import requests
from PIL import Image, ImageStat

class graph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(self, ctx):
        async for message in ctx.channel.history(limit=500):
            print(message.content) # Print the messages and show each in a new line


async def setup(bot):
    await bot.add_cog(graph(bot))