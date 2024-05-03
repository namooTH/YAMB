import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

from io import BytesIO
import requests

class train(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content.lower() == "train" and message.author == 899113384660844634:
            channel = message.channel
            messages = await channel.history(limit=200).flatten()
            for msg in messages:
                print(msg.jump_url)


async def setup(bot):
    await bot.add_cog(train(bot))