import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

from io import BytesIO
import requests

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter 
from pilmoji import Pilmoji

import math
import re

class textbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generatetextbox(self, text, avatar=None, name=None, animated=None, border=None, asterisk=None, fontfile=None, custom_background=None):
        # setup stuff
        if fontfile:
            fontfile = f"data/fonts/{fontfile}"
        else:
            fontfile = "data/fonts/determination-mono.ttf"

        if asterisk:
            text = "* " + text

        # border & background
        if not border: # default setting
            border = Image.open("data/textbox/border/dt.png")
            mask = Image.open("data/textbox/dtbg.png")
            x_offset = 16
            y_offset = 16
        else:
            if border in ["dt.png"]:
                mask = Image.open("data/textbox/dtbg.png")
                x_offset = 16
                y_offset = 16
            if border in ["ut.png", "earthbound.png", "thunder.png"]:
                mask = Image.open("data/textbox/utbg.png")
                x_offset = 7
                y_offset = 7

            border = Image.open(f"data/textbox/border/{border}")

        if custom_background:
            img = custom_background
            img.thumbnail((mask.size[0] * 2,mask.size[1] * 2), resample=Image.Resampling.NEAREST)
            img = img.filter(ImageFilter.GaussianBlur(5))
            width, height = img.size
            left = (width - mask.size[0])/2
            top = (height - mask.size[1])/2
            right = (width + mask.size[0])/2
            bottom = (height + mask.size[1])/2
            img = img.crop((left, top, right, bottom))
            img = img.resize((mask.size[0], mask.size[1]))
        else:
            img = Image.new("RGB", (mask.size[0], mask.size[1]), (0,0,0))

        bg = Image.new("RGB", (mask.size[0], mask.size[1]))
        bg.putalpha(0)
        img = Image.composite(img,bg,mask)

        # draw port if exists
        if avatar:
            avatar.thumbnail((134,134), resample=Image.Resampling.NEAREST)
            middle_img_y = int((img.size[1] - avatar.size[1]) / 2)
            port_x_pos = int((134 - avatar.size[0]) / 2) + x_offset
            try:
                img.paste(avatar, (port_x_pos, middle_img_y), avatar)
            except:  # noqa: E722
                img.paste(avatar, (port_x_pos, middle_img_y))

        # init font
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(fontfile, 30)
        if avatar:
            textpos = 139 + x_offset
        else:
            textpos = 12 + x_offset
        textposlimit = 549 + x_offset
        lines = []

        # autowrap text (word mode) (also math jumpscare)

        #finds emoji and not replace it
        pattern = r'(<.*?>)'
        replacement = '■'
        finds = re.findall(pattern, text)
        text = re.sub(pattern, replacement, text)

        while True:
            if len(lines) >= 3:
                break
            
            textlength = font.getlength(text)
            if textlength < textposlimit - textpos:
                lines.append(text)
                break
            length = math.ceil((textlength - (textposlimit - textpos)) / (textlength / len(text)))

            # if text is too long or too short
            while font.getlength(text[:int(len(text) - length)]) > textposlimit - textpos:
                length -= 1
            while font.getlength(text[:int(len(text) - length)]) - (textposlimit - textpos) < -100:
                length += 1

            nextline = text[int(len(text) - length):]
            text = text[:int(len(text) - length)]

            # detect if space is found
            spacerange = 10
            if " " in (text[len(text) - spacerange:]):
                for num in range(1, spacerange):
                    if text[-num] == " ":
                        nextline = text[-num:][1:] + nextline
                        text = text[:-num]
                        break
            lines.append(text)
            text = nextline

        # assemble
        text = ""
        for line in range(len(lines)):
            text += lines[line] + "\n"
        for emoji in finds:
            text = text.replace(replacement, emoji, 1)

        # nametag
        if name:
            font = ImageFont.truetype(fontfile, 16)
            namepos = (((int(134 - font.getlength(name))) / 2) + x_offset, 114 + y_offset)
            draw.text((namepos[0] + 2, namepos[1] + 2),name,(0,0,0),font=font)
            draw.text(namepos,name,(255,255,255),font=font)

        # put border
        img.paste(border, (0, 0), border)

        # check if is animated and put text
        font = ImageFont.truetype(fontfile, 30)
        if animated:
            duration_frames = []
            images = []
            drawtext = ""
            for char in text:
                drawtext += char
                temp = img.copy()
                draw = ImageDraw.Draw(temp)
                if not custom_background:
                    draw.text((textpos,16 + y_offset),drawtext,(255,255,255),font=font,spacing=10)
                else:
                    draw.text((textpos + 2, 30 + 2),text,(0,0,0),font=font, spacing=10)
                    draw.text((textpos, 30),text,(255,255,255),font=font, spacing=10)
                images.append(temp.copy())
                duration_frames.append(70) # pause 70 ms
            duration_frames.pop()
            duration_frames.append(4000) # pause for 4 seconds
            with BytesIO() as image_binary:
                images[0].save(image_binary, 'GIF', save_all=True,append_images=images[1:],duration=duration_frames,loop=0)
                image_binary.seek(0)
                return discord.File(fp=image_binary, filename='image.gif')
        else:
            if not custom_background:
                with Pilmoji(img) as pilmoji:
                    pilmoji.text((textpos, 16 + y_offset), text.strip(), (255, 255, 255), font, spacing=10, emoji_scale_factor=1, emoji_position_offset=(0, -2))
            else:
                draw = ImageDraw.Draw(img)
                draw.text((textpos + 2, 30 + 2),text,(0,0,0),font=font, spacing=10)
                draw.text((textpos, 30),text,(255,255,255),font=font, spacing=10)
            #draw.text(,text,(255,255,255),font=font,spacing=10)
            with BytesIO() as image_binary:
                img.save(image_binary, 'PNG')
                image_binary.seek(0)
                return discord.File(fp=image_binary, filename='image.png')




    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.id == 1234430787924000778:
            image = await self.generatetextbox(avatar=Image.open(BytesIO(requests.get(message.author.avatar.url).content)), text=message.clean_content)
            await message.channel.send(file=image)
            await message.delete()
        if message.content.lower() == "mtbq":
            messager = await message.channel.fetch_message(message.reference.message_id)
            if messager.content == "":
                return await message.channel.send("cant", reference=message)
            if messager.author == self.bot.user:
                return
            image = await self.generatetextbox(avatar=Image.open(BytesIO(requests.get(messager.author.avatar.url).content)), text=messager.content, name=messager.author.name)
            await message.channel.send("generated by deltafall-bot", file=image, reference=message)




    @app_commands.command(name="textbox", description="makes a textbox")
    @app_commands.choices(border_style=[
        app_commands.Choice(name="Deltarune", value="dt.png"),
        app_commands.Choice(name="Undertale", value="ut.png"),
        app_commands.Choice(name="Earthbound", value="earthbound.png"),
        app_commands.Choice(name="TS!UNDERSWAP", value="thunder.png")])
    @app_commands.choices(font=[
        app_commands.Choice(name="Determination Mono", value="determination-mono.ttf"),
        app_commands.Choice(name="Comic Sans", value="comic-sans.ttf"),
        app_commands.Choice(name="Earthbound", value="earthbound.ttf"),
        app_commands.Choice(name="Minecraft", value="minecraft.ttf"),
        app_commands.Choice(name="Papyrus", value="papyrus.ttf"),
        app_commands.Choice(name="Wingdings", value="wingdings.ttf")])
    @app_commands.choices(asterisk=[
        app_commands.Choice(name="Yes", value="True"),
        app_commands.Choice(name="No", value="False")])
    @app_commands.choices(animated=[
        app_commands.Choice(name="Yes", value="True"),
        app_commands.Choice(name="No", value="False")])
    @app_commands.choices(portrait=[
        app_commands.Choice(name="ralsei", value="ralsei.webp"),
        app_commands.Choice(name="susie", value="susie.webp"),
        app_commands.Choice(name="sans", value="sans.webp"),
        app_commands.Choice(name="papyrus", value="papyrus.webp"),
        app_commands.Choice(name="queen", value="queen.webp"),
        app_commands.Choice(name="berdly", value="berdly.webp"),
        app_commands.Choice(name="asgore", value="asgore.webp"),
        app_commands.Choice(name="alphys", value="alphys.webp"),
        app_commands.Choice(name="bratty", value="bratty.webp"),
        app_commands.Choice(name="catti", value="catti.webp"),
        app_commands.Choice(name="catty", value="catty.webp")])
        
    async def textbox(
        self,
        interaction: discord.Interaction,
        text: str,
        animated: Optional[app_commands.Choice[str]],
        font: Optional[app_commands.Choice[str]],
        asterisk: Optional[app_commands.Choice[str]],
        border_style: Optional[app_commands.Choice[str]],
        portrait: Optional[app_commands.Choice[str]],
        custom_portrait: Optional[discord.Attachment],
        custom_background: Optional[discord.Attachment],
        nametag: Optional[str]):
        port = None
        if portrait and not custom_portrait:
            port = Image.open(f"data/textbox/portraits/{portrait.value}")
        if custom_portrait:
            port = Image.open(BytesIO(requests.get(custom_portrait.url).content))
        
        if animated and animated.value == "True":
            animated = True
        if asterisk and asterisk.value == "True":
            asterisk = True
        if font:
            font = font.value
        if custom_background:
            custom_background = Image.open(BytesIO(requests.get(custom_background.url).content))
        if border_style:
            border_style = border_style.value

        image = await self.generatetextbox(avatar=port, text=text, name=nametag, animated=animated, border=border_style, asterisk=asterisk, fontfile=font, custom_background=custom_background)
        await interaction.response.send_message(file=image)

async def setup(bot):
    await bot.add_cog(textbox(bot))