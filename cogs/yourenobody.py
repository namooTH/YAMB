from discord.utils import get
from discord.ext import commands
import time
from discord.ext import tasks
import os

class yourenobody(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_time.start()
        self.guildid = 1198291214672347308
        self.stupidrole = 1233821393133768817
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for file in os.listdir("data/just_joined/"):
            with open(f"data/just_joined/{file}", "r") as f:
                time = float(f.readline())
                while time in self.cooldowns:
                    time += 1
                self.cooldowns[time] = int(file)
        self.cooldowns = dict(sorted(self.cooldowns.items(), key=lambda item: item[1]))

    @tasks.loop(seconds=30)
    async def check_time(self):
        if len(self.cooldowns) >= 1:
            if next(iter(self.cooldowns)) - time.time() < -172800: # 2 days 
                usr_id = self.cooldowns[next(iter(self.cooldowns))]
                guild = self.bot.get_guild(self.guildid)
                usr = guild.get_member(usr_id)
                try:
                    await usr.remove_roles(get(guild.roles, id=self.stupidrole))
                except:  # noqa: E722
                    pass
                os.remove(f"data/just_joined/{usr_id}")
                del self.cooldowns[next(iter(self.cooldowns))]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == self.guildid:
            print(member.created_at.day)
            "erm this guy might be an alt <@&1211135690503495740><@&1220416159573213264> can u take a look at this?"
            role = get(member.guild.roles, id=self.stupidrole)
            await member.add_roles(role)
            
            with open(f"data/just_joined/{member.id}", "x") as file:
                file.write(str(time.time()))
                self.cooldowns[time.time()] = int(member.id)

async def setup(bot):
    await bot.add_cog(yourenobody(bot))