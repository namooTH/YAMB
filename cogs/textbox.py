import discord
from discord.ext import commands
from discord import app_commands

from io import BytesIO
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class textbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generatetextbox(avatarurl, text):
        img = Image.open("dtbg.png")

        port = Image.open(BytesIO(requests.get(avatarurl).content))
        port = port.resize((134,134), resample=Image.Resampling.NEAREST)
        img.paste(port, (16,16))

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("dtmono.ttf", 30)
        textpos = 155
        textposlimit = 565
        lines = []
        while True:
            nextline = ""
            if textpos + font.getlength(text) < textposlimit:
                lines.append(text)
                break
            while textpos + font.getlength(text) >= textposlimit:
                nextline += text[-1] # <--
                text = text[:-1] # <--
            lines.append(text)
            #[::-1] = reverse the string since we are reading from the back
            text = nextline[::-1]

        # assemble
        for line in range(len(lines)):
            draw.text((textpos, 30 * (line + 1)),lines[line],(255,255,255),font=font)
        border = Image.open("dt.png")
        img.paste(border, (0, 0), border)

        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            return discord.File(fp=image_binary, filename='image.png')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author.id == 899113384660844634:
            print(type(message.author.avatar.url))
            image = await self.generatetextbox(message.author.avatar.url, message.content)
            await message.channel.send(file=image)


async def setup(bot):
    await bot.add_cog(textbox(bot))