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
        messages = await ctx.channel.history(limit=10).flatten() # Get the history of the channel where the command was invoked
        for message in messages: # Get only the messages and not any extra information
            print(message.content, sep="\n") # Print the messages and show each in a new line


async def setup(bot):
    await bot.add_cog(graph(bot))