import discord
from discord.ext import commands
from discord import app_commands

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def purge(self, channel, number, user=None):
        await channel.purge(limit=number)

    async def delete(self, message):
        await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        message_content = message.content.lower()
        if not message_content.startswith(".m") or not message.author.guild_permissions.manage_messages:
            return
        actions = await self.bot.parse_args(args=message_content,prefix=".m")
        errors = actions[1]
        actions = actions[0]
        # execute
        for d in actions:
            for var in d.items():
                try:
                    match var[0]:

                        # requires no parameters
                        case "d" | "delete":
                            messager = await message.channel.fetch_message(message.reference.message_id)
                            await self.delete(message=messager)

                        # requires parameters
                        case "p" | "purge":
                            allowedtype = (int)
                            if isinstance(var[1], allowedtype):
                                await self.purge(channel=message.channel, number=var[1])
                            else:
                                errors.append(f"invaild action at `{var[0]}`: {type(var[1])} not in {allowedtype}")
                                break

                        # what the fuck
                        case _:
                            errors.append(f"invaild action: `{var[0]}`")
                            break

                except Exception as e:
                    errors.append((f"invaild action at `{var[0]}`:\n```{e}```"))
                    break
        if errors:
            errors = '\n'.join(errors)
            await message.channel.send(errors, reference=message)
        await message.delete()
        

async def setup(bot):
    await bot.add_cog(mod(bot))