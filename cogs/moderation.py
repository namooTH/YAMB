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
                    case "d" | 'p':
                        root_action = rawaction[0]
                    case "=":
                        is_assigned = True
                    case _:
                        additional_info = ""
                        if is_assigned:
                            try:
                                child_action = eval(rawaction)
                                rawaction = ""
                                break
                            except Exception as e:
                                additional_info = f"\n```{e}```" 
                        await message.channel.send((f"invaild action at `{rawaction}`{additional_info}"), reference=message)
                        break
                rawaction = rawaction[1:]
            actions.append({root_action: child_action})


        # do it
        for d in actions:
            for var in d.items():
                match var[0]:

                    case "d":
                        messager = await message.channel.fetch_message(message.reference.message_id)
                        await messager.delete()
                    case "p":
                        allowedtype = [int]
                        if len(var) < 2:
                            await message.channel.send((f"invaild action at `{var[0]}`: no value specified"), reference=message)
                            break
                        if type(var) == allowedtype:
                            await message.channel.purge(limit=var[1])
                        await message.channel.send((f"invaild action at `{var[0]}`: {var[1]} not in {allowedtype}"), reference=message)
                        break

        await message.delete()
        

async def setup(bot):
    await bot.add_cog(mod(bot))