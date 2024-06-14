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
            print()
            if reaction.emoji == "👍":
                await channel.send(f'test')

async def setup(bot):
    await bot.add_cog(reaction(bot))