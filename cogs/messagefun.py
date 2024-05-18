import discord
from discord.ext import commands
from discord import app_commands

import random
#from typing import Optional


class messagefun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "@someone" in message.content.lower():
            members = message.guild.members
            await message.channel.send(f'<@{members[random.randint(0, len(members) - 1)].id}>', reference=message)
        if message.content.lower() == "nerdify":
            messager = await message.channel.fetch_message(message.reference.message_id)
            await message.channel.send(f'ermm acukally {messager.content} - 🤓 `{messager.author}`', reference=message)

async def setup(bot):
    await bot.add_cog(messagefun(bot))