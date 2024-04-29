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

    async def generatetextbox(self, avatarurl, text, name):
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

        # autowrap text (word mode (btw i coded it))

        while True:
            nextline = ""
            if textpos + font.getlength(text) < textposlimit:
                lines.append(text)
                break
            while textpos + font.getlength(text) >= textposlimit:
                nextline += text[-1] # <--
                text = text[:-1] # <--
            # detect if space is presented in the last 10 chars
            for num in range(1, 10):
                if text[-num] == " ":
                    nextline = nextline + text[-num:][::-1] # looks cursed but it needs to be reverse
                    text = text[:-num]
                    break
            lines.append(text)
            #[::-1] = reverse the string since we are reading from the back
            text = nextline[::-1].strip()

        # assemble
        text = ""
        for line in range(len(lines)):
            text += lines[line] + "\n"
        draw.text((textpos, 30),text,(255,255,255),font=font)

        # nametag
        font = ImageFont.truetype("data/textbox/dtmono.ttf", 16)
        namepos = ((165 - font.getlength(name)) / 2, 130)
        draw.text((namepos[0] + 2, namepos[1] + 2),name,(0,0,0),font=font)
        draw.text(namepos,name,(255,255,255),font=font)

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
            image = await self.generatetextbox(avatarurl=message.author.avatar.url, text=message.clean_content, name=message.author.name)
            await message.channel.send(file=image)
            await message.delete()

async def setup(bot):
    await bot.add_cog(textbox(bot))