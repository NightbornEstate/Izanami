# This file was created by github.com/ruin332
# He is 100% boss
# he knows de way

from discord.ext import commands
import discord
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFilter
import os
import glob
import random
from io import StringIO, BytesIO
import aiohttp
from unidecode import unidecode
import asyncio


class DeWay:
    def __init__(self, bot):
        self.bot = bot
    # im is the background to use (pass in from PIL's Image.open)
    # offset_x and offset_y refer to avatar img
    # returns BytesIO file-like object for easy use with bot.send_file
    async def welcome_member(self, im, font, member, offset_x=0, offset_y=-70,
                             new_width=1000, new_height=500, ava_sqdim=260,
                             text_offset_x=0, text_offset_y=140, text=None,
                             is_square=False, text_color=None, blur_radius=15,
                             blur_offset_y=0, outline=True):
        im = im.copy()
        width, height = im.size

        name = unidecode(member.name)
        if text is None:
            welcome = 'Welcome {0},\n to {1.server.name}!'.format(name, member)
        else:
            welcome = text

        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = (width + new_width) // 2
        bottom = (height + new_height) // 2
        #im = im.crop((left, top, right, bottom)).convert("RGB")

        # how to set up a gradient from the bottom:
        # fade_from = new_height/4
        # fade_to = new_height-fade_from
        #
        # fade_from = int(fade_from)
        # fade_to = int(fade_to)
        #
        # for i in range(fade_from, new_height+1):
        #     fade = int((i-fade_from)/(fade_to)*255)
        #     draw.rectangle(((0, i), (new_width, i)), fill=(0, 0, 0, fade))

        ov_left = 0
        ov_top = (im.height // 2) + (blur_offset_y)
        ov_right = im.width
        ov_bottom = im.height
        #ov_box = (ov_left, ov_top, ov_right, ov_bottom)

        #ov_ic = im.crop(ov_box)
        #ov_ic = ov_ic.filter(ImageFilter.GaussianBlur(blur_radius))

        #im.paste(ov_ic, ov_box)

        draw = ImageDraw.Draw(im, mode='RGBA')
        #draw.rectangle(((ov_left, ov_top), (ov_right, ov_bottom)), fill=(0, 0, 0, 120))

        avatar_im = None
        url = member.avatar_url
        if not url:
            url = member.default_avatar_url

        retries = 1
        while True:
            async with aiohttp.ClientSession(loop=self.bot.loop) as aiosession:
                with aiohttp.Timeout(10):
                    async with aiosession.get(url) as resp:
                        avatar_im = BytesIO(await resp.read())
                        if avatar_im.getbuffer().nbytes > 0 or retries == 0:
                            await aiosession.close()
                            break
                        retries -= 1
                        print('0 nbytes image found. Retries left: {}'.format(retries+1))
        resize = (ava_sqdim, ava_sqdim)
        avatar_im = Image.open(avatar_im).convert("RGBA")
        avatar_im = avatar_im.resize(resize, Image.ANTIALIAS)
        avatar_im.putalpha(avatar_im.split()[3])

        if not is_square:
            mask = Image.new('L', resize, 0)
            maskDraw = ImageDraw.Draw(mask)
            maskDraw.ellipse((0, 0) + resize, fill=255)
            mask = mask.resize(avatar_im.size, Image.ANTIALIAS)
            avatar_im.putalpha(mask)

        img_center_x = im.width // 2
        img_center_y = im.height // 2
        im_scale = 1
        img_offset_x = 150
        img_offset_y = 150
        ava_right = im_scale * (img_offset_x + avatar_im.width//2)
        ava_bottom = im_scale * (img_offset_y + avatar_im.height//2)
        ava_left = (img_offset_x - avatar_im.width//2)
        ava_top = (img_offset_y - avatar_im.height//2)
        im.paste(avatar_im, box=(ava_left, ava_top, ava_right, ava_bottom), mask=avatar_im)

        text_width, text_height = draw.textsize(welcome, font=font)
        x = ((img_center_x - text_width / 2) + text_offset_x)
        y = ((img_center_y - text_height / 2) + text_offset_y)

        if outline:
            border_coords = ((x-10, y), (x+10, y), (x, y-10), (x, y+10), (x-10, y-10),
                             (x+10, y-10), (x-10, y+10), (x+10, y+10))

            for coord in border_coords:
                draw.text(coord, welcome, font=font, align='center', fill='black')
        
        sfont = ImageFont.truetype('Comic Sans.ttf', 60)
        quotes = [
            "show me da wey",
            "show dem da wey",
            "show my brother da wey",
            "does " + name + " know da wey?",
            name + " is one of us now",
            "u no da wae *click click*",
            "welcome them my bruddas",
            "i found de wae"
        ]
        quoteArray = [ [random.randint(0, 1400), random.randint(0, 1000), q] for q in quotes ]
        for a in quoteArray:
            draw.text( [a[0], a[1]] , a[2], fill=random.choice(["white", "red", "green", "yellow", "orange", "blue", "blue"]), font=sfont, align="right")

        for i in range(4):
            ranx = random.randint(0, 1400)
            rany = random.randint(0, 1000)
            files = glob.glob('{}/pods/*.png'.format(cwd))
            files.extend(glob.glob('{}/pods/*.jpg'.format(cwd)))
            #font = ImageFont.truetype('Comic Sans.ttf', 100)
            # kwargs['ava_sqdim'] = 200
            # kwargs['blur_offset_y'] = 100
            rand_img = random.choice(files)
            pod = Image.open(rand_img)
            pod = Image.eval(pod, lambda px: px // 2)
            im.paste(pod, box=(ranx, rany), mask=pod)

        draw.text((x, y), welcome, fill=text_color, font=font, align='center')

        temp = BytesIO()
        im.save(temp, format='png')
        temp.seek(0)
        return temp

    async def setup_welcome(self, member, ch=False):
        if member.bot:
            return

        cwd = os.getcwd()
        send_to = self.bot.get_server('300155035558346752').get_channel(ch) if ch else None
        kwargs = dict.fromkeys(['offset_x', 'offset_y', 'text_offset_x',
                                'text_offset_y', 'new_width', 'new_height',
                                'ava_sqdim', 'is_square', 'text', 'text_color',
                                'blur_radius', 'blur_offset_y', 'outline'])

        if member.server.id == '300155035558346752':
            files = glob.glob('{}/images3/*.png'.format(cwd))
            files.extend(glob.glob('{}/images3/*.jpg'.format(cwd)))
            font = ImageFont.truetype('Comic Sans.ttf', 100)
            # kwargs['ava_sqdim'] = 200
            # kwargs['blur_offset_y'] = 100
            rand_img = random.choice(files)
            im = Image.open(rand_img)
        else:
            return
        keys_to_remove = [key for key, value in kwargs.items() if value is None]
        for k in keys_to_remove:
            kwargs.pop(k, None)
        im = await self.welcome_member(im, font, member, **kwargs)
        if send_to is None:
            send_to = member.server.default_channel
        content = 'Welcome {0.mention} to {0.server.name}!'.format(member)
        await self.bot.send_file(send_to, im, content=content, filename='welcome.jpg')

def setup(bot):
    bot.add_cog(DeWay(bot))
