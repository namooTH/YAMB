import discord
from discord.ext import commands
from discord import app_commands
import os
import json

class stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="stat", description="gets the deltafall server stat")
    async def stat(self, interaction: discord.Interaction):
        quotes = json.load(open("data/quote.json"))
        embed=discord.Embed(title="Statistics", description=f'{len(os.listdir("data/just_joined/"))} people came in from 2 days ago.\nThere are {len(quotes)} quote(s) being added so far', color=0x57e389)
        await interaction.response.send_message(embed=embed, allowed_mentions=discord.AllowedMentions.none())

async def setup(bot):
    await bot.add_cog(stat(bot))