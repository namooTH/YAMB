import discord
from discord.utils import get
from discord.ext import commands
from discord import app_commands
from discord.ext import tasks

class goat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="slash", description="test slash command")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("i kissed your mom last night!!!")

async def setup(bot):
    await bot.add_cog(goat(bot))