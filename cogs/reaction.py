import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        if channel.id == 1198291214672347311:
            await channel.send('{} has added {} to the the message {}'.format(user.name, reaction.emoji, reaction.message.content))

async def setup(bot):
    await bot.add_cog(reaction(bot))