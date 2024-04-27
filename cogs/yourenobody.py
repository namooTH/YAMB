from discord.utils import get
from discord.ext import commands
import time
from discord.ext import tasks
import os

class yourenobody(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_time.start()
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for file in os.listdir("data/just_joined/"):
            with open(f"data/just_joined/{file}", "r") as f:
                time = float(f.readline())
                while time in self.cooldowns:
                    time += 1
                self.cooldowns[time] = int(file)
        self.cooldowns = dict(sorted(self.cooldowns.items()))

    @tasks.loop(seconds=1)
    async def check_time(self):
        if len(self.cooldowns) >= 1: 
            if next(iter(self.cooldowns)) - time.time() < -5:
                usr_id = self.cooldowns[next(iter(self.cooldowns))]
                guild = self.bot.get_guild(1089557218153738260)
                usr = guild.get_member(usr_id)
                await usr.remove_roles(get(guild.roles, id=1089877303443599370))

                os.remove(f"data/just_joined/{usr_id}")
                del self.cooldowns[next(iter(self.cooldowns))]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = get(member.guild.roles, id=1089877303443599370)
        await member.add_roles(role)
        
        with open(f"data/just_joined/{member.id}", "x") as file:
            file.write(str(time.time()))
            self.cooldowns[time.time()] = int(member.id)

async def setup(bot):
    await bot.add_cog(yourenobody(bot))