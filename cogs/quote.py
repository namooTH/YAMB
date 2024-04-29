import discord
from discord.ext import commands
from discord import app_commands
import json
import random

class randomquote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="random_quote", description="get random quote")
    async def quote(self, interaction: discord.Interaction):
        data = json.load(open("data/quote.json"))
        quote = list(data)[random.randint(0, len(list(data)) - 1)]
        author = data[quote]
        await interaction.response.send_message(f'"{quote}"\n### `- {author}`', allowed_mentions=discord.AllowedMentions.none())

    @app_commands.command(name="addquote", description="add a quote")
    async def addquote(self, interaction: discord.Interaction, quote: str, by: str):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("u dont have manage message permission",ephemeral=True)
        else:
            data = json.load(open("data/quote.json"))
            data[quote] = by
            json.dump(data, open("data/quote.json", 'w'))
            await interaction.response.send_message(f"added {quote} by {by}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "aq" or message.content == "<@949479338275913799>":
            messager = await message.channel.fetch_message(message.reference.message_id)
            if messager.content == "" and not messager.attachments:
                return await message.channel.send("its just an empty text you idiot", reference=message)
            if messager.author == self.bot.user:
                return
            content = messager.content
            if messager.attachments:
                content = (f"{content} | {messager.attachments[0].url}")
            data = json.load(open("data/quote.json"))
            data[content] = messager.author.name
            json.dump(data, open("data/quote.json", 'w'))
            embed=discord.Embed(title="Quote Added", description=f'"{content}"\n\nby {messager.author.name}', color=0x57e389)
            await message.channel.send(embed=embed, reference=message)

        if message.content == "dq":
            messager = await message.channel.fetch_message(message.reference.message_id)
            if messager.author != message.author:
                return await message.channel.send("ur not the author of that message :)", reference=message)
            content = messager.content
            if messager.attachments:
                content = (f"{content} | {messager.attachments[0].url}")
            data = json.load(open("data/quote.json"))
            if data[content] != message.author.name:
                return await message.channel.send("u dont own that quote", reference=message)
            try:
                data.pop(content)
            except:  # noqa: E722
                return await message.channel.send("quote doesnt exist in the database", reference=message)
            json.dump(data, open("data/quote.json", 'w'))
            embed=discord.Embed(title="Quote Deleted", description=f'{message.author.name} deleted it', color=0x57e389)
            await message.channel.send(embed=embed, reference=message)

async def setup(bot):
    await bot.add_cog(randomquote(bot))