import discord
from discord.ext import commands
from discord import app_commands

import random
#from typing import Optional


class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        if not message_content.startswith(".m "):
            return
        action = message_content[3:]
        if "," in action:
            action = action.split(",")
        else:
            action = [action]
        actions = []

        # parser
        for a in action:
            root_action = None
            child_action = None
            is_assigned = False
            rawaction = a

            while len(rawaction) > 0:
                match rawaction[0]:
                    case "d":
                        root_action = "d"

                    case "=":
                        is_assigned = True
                    case _:
                        additional_info = ""
                        if is_assigned:
                            try:
                                child_action = eval(rawaction)
                                actions.append({root_action: child_action})
                                rawaction = ""
                                break
                            except Exception as e:
                                additional_info = f"\n```{e}```" 
                        print(f"invaild action at `{rawaction}`{additional_info}")
                        #await message.channel.send("invaild action whar", reference=message)
                        break
                rawaction = rawaction[1:]

        for d in actions:
            for var in d.items():
                match var[0]:
                    
                    case "d":
                        await message.delete()

                        #if len(var) > 1:
                        #    
        

async def setup(bot):
    await bot.add_cog(mod(bot))