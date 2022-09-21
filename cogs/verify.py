import settings
import nextcord
import asyncio
import datetime
import random
import os
from utils.languageembed import languageEmbed
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from nextcord.ext import commands


class Verify(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(aliases=["ind"])
    async def introduction(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                data = await settings.collection.find_one({"guild_id": ctx.guild.id})
                status = data["introduce_status"]
                frame = data["introduce_frame"]
                channel = data["introduce_channel_id"]
                give = data["introduce_role_give_id"]
                remove = data["introduce_role_remove_id"]
                if channel != "None":
                    introduction_channel = self.bot.get_channel(int(channel))

                else:
                    introduction_channel = ctx.channel

                if status == "YES":
                    try:
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                            description="┗[1] ชื่อ",
                        )

                        embed.set_footer(text="คำถามที่ [1/3]")
                        message = await ctx.send(embed=embed)

                        username = await self.bot.wait_for(
                            "message",
                            check=lambda user: user.author.id == ctx.author.id,
                            timeout=20,
                        )
                        name = username.content
                        await asyncio.sleep(1)
                        await username.delete()

                    except asyncio.TimeoutError:
                        await message.delete()

                    try:
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                            description="┗[2] อายุ",
                        )

                        embed.set_footer(text="คำถามที่ [2/3]")
                        await message.edit(embed=embed)

                        userage = await self.bot.wait_for(
                            "message",
                            check=lambda user: user.author.id == ctx.author.id,
                            timeout=20,
                        )
                        age = userage.content
                        await asyncio.sleep(1)
                        await userage.delete()

                    except asyncio.TimeoutError:
                        await message.delete()

                    try:
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                            description="┗[3] เพศ",
                        )

                        embed.set_footer(text="คำถามที่ [3/3]")
                        await message.edit(embed=embed)

                        usersex = await self.bot.wait_for(
                            "message",
                            check=lambda user: user.author.id == ctx.author.id,
                            timeout=20,
                        )
                        sex = usersex.content
                        await asyncio.sleep(1)
                        await usersex.delete()

                    except asyncio.TimeoutError:
                        await message.delete()

                    if give != "None":
                        role = int(give)
                        role = ctx.guild.get_role(role)
                        if role:
                            try:
                                await ctx.author.add_roles(role)

                            except nextcord.Forbidden:
                                pass

                    if remove != "None":
                        role = int(remove)
                        role = ctx.guild.get_role(role)
                        if role:
                            try:
                                await ctx.author.remove_roles(role)

                            except nextcord.Forbidden:
                                pass

                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        description=(f"สวัสดี {ctx.author}! ยินดีต้อนรับสู่ {ctx.guild}"))
                    embed.add_field(name = "ชื่อ", value = f"{name}", inlines = True)
                    embed.add_field(name = "อายุ", value = f"{age}", inlines = True)
                    embed.add_field(name = "เพศ", value = f"{sex}", inlines = True)
                    embed.set_thumbnail(url=f"{ctx.author.avatar.url}")
                    embed.set_author(
                        name=f"{ctx.author}", icon_url=f"{ctx.author.avatar.url}"
                    )
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=ctx.author.id)
                    await message.delete()
                    await introduction_channel.send(ctx.author.mention)
                    await introduction_channel.send(embed=embed)

            if server_language == "English":
                data = await settings.collection.find_one({"guild_id": ctx.guild.id})
                status = data["introduce_status"]
                frame = data["introduce_frame"]
                channel = data["introduce_channel_id"]
                give = data["introduce_role_give_id"]
                remove = data["introduce_role_remove_id"]
                introduction_channel = self.bot.get_channel(int(channel))
                if status == "YES":
                    if frame == "None":
                        frame = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

                        if channel == "None":
                            try:
                                embed = nextcord.Embed(
                                    colour=0x00FFFF,
                                    title="Please fill in all information. 📝",
                                    description="┗[1] Name",
                                )

                                embed.set_footer(text="Question [1/3]")
                                message = await ctx.send(embed=embed)

                                username = await self.bot.wait_for(
                                    "message",
                                    check=lambda user: user.author.id == ctx.author.id,
                                    timeout=20,
                                )
                                name = username.content
                                await asyncio.sleep(1)
                                await username.delete()

                            except asyncio.TimeoutError:
                                await message.delete()

                            try:
                                embed = nextcord.Embed(
                                    colour=0x00FFFF,
                                    title="Please fill in all information. 📝",
                                    description="┗[2] Age",
                                )

                                embed.set_footer(text="Question [2/3]")
                                await message.edit(embed=embed)

                                userage = await self.bot.wait_for(
                                    "message",
                                    check=lambda user: user.author.id == ctx.author.id,
                                    timeout=20,
                                )
                                age = userage.content
                                await asyncio.sleep(1)
                                await userage.delete()

                            except asyncio.TimeoutError:
                                await message.delete()

                            try:
                                embed = nextcord.Embed(
                                    colour=0x00FFFF,
                                    title="Please fill in all information. 📝",
                                    description="┗[3] Gender",
                                )

                                embed.set_footer(text="Question [3/3]")
                                await message.edit(embed=embed)

                                usersex = await self.bot.wait_for(
                                    "message",
                                    check=lambda user: user.author.id == ctx.author.id,
                                    timeout=20,
                                )
                                sex = usersex.content
                                await asyncio.sleep(1)
                                await usersex.delete()

                            except asyncio.TimeoutError:
                                await message.delete()

                            embed = nextcord.Embed(
                                colour=0x00FFFF,
                                description=(f"Hello there {ctx.author}! Welcome to {ctx.guild}!"))
                            embed.add_field(name = "์Name", value = f"{name}", inlines = True)
                            embed.add_field(name = "Age", value = f"{age}", inlines = True)
                            embed.add_field(name = "Gender", value = f"{sex}", inlines = True)
                            embed.set_thumbnail(url=f"{ctx.author.avatar.url}")
                            embed.set_author(
                                name=f"{ctx.author}",
                                icon_url=f"{ctx.author.avatar.url}",
                            )
                            embed.timestamp = datetime.datetime.utcnow()
                            embed.set_footer(text=ctx.author.id)
                            await message.delete()
                            await ctx.send(ctx.author.mention)
                            await ctx.send(embed=embed)

                            if not give == "None":
                                role = int(give)
                                role = ctx.guild.get_role(role)
                                if role:
                                    try:
                                        await ctx.author.add_roles(role)

                                    except nextcord.Forbidden:
                                        pass

                            if not remove == "None":
                                role = int(remove)
                                role = ctx.guild.get_role(role)
                                if role:
                                    try:
                                        await ctx.author.remove_roles(role)

                                    except nextcord.Forbidden:
                                        pass

    @commands.command(aliases=["vfy"])
    async def verify(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                await ctx.message.delete()
                data = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if not data is None:
                    time = data["verification_time"]
                    status = data["verification_system"]
                    vfchannel = data["verification_channel_id"]
                    give = data["verification_role_give_id"]
                    remove = data["verification_role_remove_id"]
                    if status == "YES":
                        if vfchannel != "None":
                            channel_id = int(vfchannel)
                            channel = self.bot.get_channel(channel_id)
                            print("6")
                            if int(ctx.channel.id) == vfchannel:
                                print("7")
                                if not Path("arial.ttf").exists():
                                    dirname = os.path.dirname(os.path.abspath(__file__))
                                    fontfile = os.path.join(dirname, "arial.ttf")

                                else:
                                    fontfile = "arial.ttf"

                                chars = (
                                    "abcdefghfkmnopqrstwxyzABCDEFGHIJKLMNOP12345678910"
                                )
                                text = ""
                                for i in range(6):
                                    text = text + random.choice(chars)
                                img = Image.new("RGB", (200, 50))

                                font = ImageFont.truetype(fontfile, 40)
                                imgdraw = ImageDraw.Draw(img)
                                imgdraw.text(
                                    (45, 5), text, fill=(255, 255, 0), font=font
                                )
                                img.save("image/verify.png")
                                file = nextcord.File(
                                    "image/verify.png", filename="verify.png"
                                )
                                print("2")
                                embed = nextcord.Embed(colour=0x00FFFF, title="Captcha")
                                embed.set_image(url="attachment://verify.png")
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                embed.set_author(
                                    name=f"กรุณาพิมพ์ข้อความตามภาพเพื่อยืนยันตัวตน",
                                    icon_url=f"{ctx.author.avatar.url}",
                                )

                                message = await ctx.send(embed=embed, file=file)

                                try:
                                    answer = await self.bot.wait_for(
                                        "message",
                                        check=lambda user: user.author.id
                                        == ctx.author.id,
                                        timeout=time,
                                    )
                                    answeruser = answer.content
                                    if answeruser == text:
                                        await message.delete()
                                        await asyncio.sleep(1)
                                        await answer.delete()

                                        embed = nextcord.Embed(
                                            description=f":white_check_mark: คุณได้รับการยืนยันแล้ว",
                                            colour=0x76FF03,
                                        )
                                        embed.set_author(
                                            name=f"{ctx.author.name}",
                                            icon_url=f"{ctx.author.avatar.url}",
                                        )
                                        message = await ctx.send(embed=embed)
                                        await asyncio.sleep(3)
                                        await message.delete()

                                        if give != "None":
                                            role = int(give)
                                            role = ctx.guild.get_role(role)
                                            if role:
                                                try:
                                                    await ctx.author.add_roles(role)

                                                except nextcord.Forbidden:
                                                    pass

                                        if remove != "None":
                                            role = int(remove)
                                            role = ctx.guild.get_role(role)
                                            if role:
                                                try:
                                                    await ctx.author.remove_roles(role)

                                                except nextcord.Forbidden:
                                                    pass

                                    else:
                                        await message.delete()
                                        await asyncio.sleep(1)
                                        await answer.delete()
                                        embed = nextcord.Embed(
                                            description=f":x: คุณพิมพ์ข้อความใน captcha ไม่ถูกต้องกรุณาพิมพ์ {settings.COMMAND_PREFIX}verify บนห้อง {ctx.channel.mention} เพื่อยืนยันตัวตนใหม่อีกครั้ง",
                                            colour=0x983925,
                                        )
                                        embed.set_author(
                                            name=f"{ctx.author.name}",
                                            icon_url=f"{ctx.author.avatar.url}",
                                        )
                                        message = await ctx.send(embed=embed)
                                        await asyncio.sleep(3)
                                        await message.delete()

                                except asyncio.TimeoutError:
                                    await message.delete()
                                    embed = nextcord.Embed(
                                        description=f":x: คุณใช้เวลานานเกินไป {settings.COMMAND_PREFIX}verify บนห้อง {ctx.channel.mention} เพื่อยืนยันตัวตนใหม่อีกครั้ง",
                                        colour=0x983925,
                                    )
                                    embed.set_author(
                                        name=f"{ctx.author.name}",
                                        icon_url=f"{ctx.author.avatar.url}",
                                    )
                                    message = await ctx.send(embed=embed)
                                    await asyncio.sleep(3)
                                    await message.delete()

                            else:
                                embed = nextcord.Embed(
                                    description=f":x: คุณสามารถใช้คําสั่งนี้ได้ในห้อง {channel}",
                                    colour=0x983925,
                                )
                                embed.set_author(
                                    name=f"{ctx.author.name}",
                                    icon_url=f"{ctx.author.avatar.url}",
                                )
                                await ctx.send(embed=embed)

                        else:
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                                colour=0x983925,
                            )

                            await ctx.send(embed=embed)

                    else:
                        embed = nextcord.Embed(
                            title=f"เซิฟเวอร์นี้ปิดใช้งาน verify",
                            description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX} #channel",
                            colour=0x983925,
                        )

                        await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}verification on",
                        colour=0x983925,
                    )

                    await ctx.send(embed=embed)

            if server_language == "English":
                await ctx.message.delete()
                data = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if not data is None:
                    time = data["verification_time"]
                    status = data["verification_system"]
                    vfchannel = data["verification_channel_id"]
                    give = data["verification_role_give_id"]
                    remove = data["verification_role_remove_id"]
                    if status == "YES":
                        if vfchannel != "None":
                            channel_id = int(vfchannel)
                            channel = self.bot.get_channel(channel_id)

                            if int(ctx.channel.id) == vfchannel:
                                if not Path("arial.ttf").exists():
                                    dirname = os.path.dirname(os.path.abspath(__file__))
                                    fontfile = os.path.join(dirname, "arial.ttf")

                                else:
                                    fontfile = "arial.ttf"

                                chars = (
                                    "abcdefghfkmnopqrstwxyzABCDEFGHIJKLMNOP12345678910"
                                )
                                text = ""
                                for i in range(6):
                                    text = text + random.choice(chars)
                                img = Image.new("RGB", (200, 50))

                                font = ImageFont.truetype(fontfile, 40)
                                imgdraw = ImageDraw.Draw(img)
                                imgdraw.text(
                                    (45, 5), text, fill=(255, 255, 0), font=font
                                )
                                img.save("image/verify.png")
                                file = nextcord.File(
                                    "image/verify.png", filename="verify.png"
                                )

                                embed = nextcord.Embed(colour=0x00FFFF, title="Captcha")
                                embed.set_image(url="attachment://verify.png")
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                embed.set_author(
                                    name=f"Please type text in the picture to verify",
                                    icon_url=f"{ctx.author.avatar.url}",
                                )

                                message = await ctx.send(embed=embed, file=file)

                                try:
                                    answer = await self.bot.wait_for(
                                        "message",
                                        check=lambda user: user.author.id
                                        == ctx.author.id,
                                        timeout=time,
                                    )
                                    answer = answer.content
                                    if answer == text:
                                        await answer.delete()
                                        await asyncio.sleep(1)
                                        await message.delete()
                                        embed = nextcord.Embed(
                                            description=f":white_check_mark: You have been verified",
                                            colour=0x76FF03,
                                        )
                                        embed.set_author(
                                            name=f"{ctx.author.name}",
                                            icon_url=f"{ctx.author.avatar.url}",
                                        )
                                        message = await ctx.send(embed=embed)
                                        await asyncio.sleep(3)
                                        await message.delete()

                                        if give != "None":
                                            role = int(give)
                                            role = ctx.guild.get_role(role)
                                            if role:
                                                try:
                                                    await ctx.author.add_roles(role)

                                                except nextcord.Forbidden:
                                                    pass

                                        if remove != "None":
                                            role = int(remove)
                                            role = ctx.guild.get_role(role)
                                            if role:
                                                try:
                                                    await ctx.author.remove_roles(role)

                                                except nextcord.Forbidden:
                                                    pass

                                    else:
                                        await message.delete()
                                        await asyncio.sleep(1)
                                        await answer.delete()
                                        embed = nextcord.Embed(
                                            description=f":x: Incorrect captcha please try again use {settings.COMMAND_PREFIX}verify in {ctx.channel.mention} to reverify",
                                            colour=0x983925,
                                        )
                                        embed.set_author(
                                            name=f"{ctx.author.name}",
                                            icon_url=f"{ctx.author.avatar.url}",
                                        )
                                        message = await ctx.send(embed=embed)
                                        await asyncio.sleep(3)
                                        await message.delete()

                                except asyncio.TimeoutError:
                                    await message.delete()
                                    await answer.delete()
                                    embed = nextcord.Embed(
                                        description=f":x: timeout please try again use {settings.COMMAND_PREFIX}verify in {ctx.channel.mention} to reverify",
                                        colour=0x983925,
                                    )
                                    embed.set_author(
                                        name=f"{ctx.author.name}",
                                        icon_url=f"{ctx.author.avatar.url}",
                                    )
                                    message = await ctx.send(embed=embed)
                                    await asyncio.sleep(3)
                                    await message.delete()

                            else:
                                embed = nextcord.Embed(
                                    description=f":x: คุณสามารถใช้คําสั่งนี้ได้ในห้อง {channel}",
                                    colour=0x983925,
                                )
                                embed.set_author(
                                    name=f"{ctx.author.name}",
                                    icon_url=f"{ctx.author.avatar.url}",
                                )
                                await ctx.send(embed=embed)

                        else:
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                                colour=0x983925,
                            )
                            await ctx.send(embed=embed)

                    else:
                        embed = nextcord.Embed(
                            title=f"เซิฟเวอร์นี้ปิดใช้งาน verify",
                            description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX} #channel",
                            colour=0x983925,
                        )

                        await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Verify(bot))
