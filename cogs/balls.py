import discord
from discord.ext import commands

class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(event, member):
        print(member.name)

async def setup(bot):
    await bot.add_cog(MainCog(bot))