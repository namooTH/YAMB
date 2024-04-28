import discord
from discord.ext import commands
from discord import app_commands
import json
import random

class banword(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "banword":
            pass

async def setup(bot):
    await bot.add_cog(banword(bot))