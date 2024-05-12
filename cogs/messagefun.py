import discord
from discord.ext import commands
from discord import app_commands
#from typing import Optional


class speechbubble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        match message.content.lower():
            case "@someone":
                members = message.guild.members
                await message.channel.send(f'<@{members[len(members)].id}>', reference=message)

async def setup(bot):
    await bot.add_cog(speechbubble(bot))