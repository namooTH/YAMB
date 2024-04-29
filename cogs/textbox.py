import discord
from discord.ext import commands

from io import BytesIO
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class textbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generatetextbox(self, avatarurl, text):
        border = Image.open("data/textbox/dt.png")
        img = Image.open("data/textbox/dtbg.png")

        port = Image.open(BytesIO(requests.get(avatarurl).content))
        port = port.resize((134,134), resample=Image.Resampling.NEAREST)
        img.paste(port, (16,16))

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("data/textbox/dtmono.ttf", 30)
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
        img.paste(border, (0, 0), border)

        with BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            return discord.File(fp=image_binary, filename='image.png')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.id == 1234430787924000778:
            image = await self.generatetextbox(avatarurl=message.author.avatar.url, text=message.content)
            await message.channel.send(file=image)
            await message.delete()

async def setup(bot):
    await bot.add_cog(textbox(bot))