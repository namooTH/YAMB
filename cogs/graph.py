#import wavelink
import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
from wavelink import Queue

#from time import strftime
#from time import gmtime
import datetime
import re

#from io import BytesIO
#import requests
#from PIL import Image, ImageStat

class graph(commands.Cog):
    def __init__(self, bot):
        self.lastmessage_time = None
        self.bot = bot

    @commands.command()
    async def history(self, ctx):
        if ctx.author.id == 899113384660844634:
            async for message in ctx.channel.history(limit=500, after=self.lastmessage_time):
                finds = re.findall(r'<:(.*?):\d+>', message.content)
                for emoji in finds:
                    print(finds)
                self.lastmessage_time = message.created_at



async def setup(bot):
    await bot.add_cog(graph(bot))