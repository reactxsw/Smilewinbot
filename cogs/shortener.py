import settings
import nextcord
import requests
import datetime
import urllib
import aiohttp
from utils.languageembed import languageEmbed
from nextcord import Webhook
from urllib.parse import urlencode
from nextcord.ext import commands


class Shortener(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def ascii(self, ctx: commands.Context, *, text):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}"
                    ) as r:
                        response = await r.text()
                        if len(f"```{response}```") > 2000:
                            embed = nextcord.Embed(
                                colour=0x983925,
                                description=f" ⚠️``{ctx.author}`` ตัวอักษรมากเกินไป ``",
                            )
                            message = await ctx.send(embed=embed)
                            await message.add_reaction("⚠️")

                        else:

                            embed = nextcord.Embed(
                                colour=0x00FFFF,
                                title="🎨 ASCII ",
                                description=(f"```{response}```"),
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed=embed)
                            await message.add_reaction("🎨")

            if server_language == "English":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}"
                    ) as r:
                        response = await r.text()
                        if len(f"```{response}```") > 2000:
                            embed = nextcord.Embed(
                                colour=0x983925,
                                description=f" ⚠️``{ctx.author}`` Too much letter ``",
                            )
                            message = await ctx.send(embed=embed)
                            await message.add_reaction("⚠️")

                        else:

                            embed = nextcord.Embed(
                                colour=0x00FFFF,
                                title="🎨 ASCII ",
                                description=(f"```{response}```"),
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed=embed)
                            await message.add_reaction("🎨")

    @ascii.error
    async def ascii_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่ต้องการสร้าง ascii art ``{settings.COMMAND_PREFIX}ascii (word)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` please specify what to turn into ascii art ``{settings.COMMAND_PREFIX}ascii (word)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    async def hastebin(self, ctx: commands.Context, *, message):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://hastebin.com/documents", data=message
                ) as r:
                    r = await r.json()

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"Hastebin link ของ {ctx.author}",
                    description=f"""
```📒 นี้คือลิงค์ Hastebin ของคุณ : 

https://hastebin.com/{r['key']}```""",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("📒")
                print(
                    f"{ctx.author} have made a hastebinlink : https://hastebin.com/{r['key']}"
                )

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"Hastebin link ของ {ctx.author}",
                    description=f"""
```📒 This is your Hastebin link : 

https://hastebin.com/{r['key']}```""",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("📒")
                print(
                    f"{ctx.author} have made a hastebinlink : https://hastebin.com/{r['key']}"
                )

    @hastebin.error
    async def hastebin_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ข้อความที่ต้องการที่จะใส่",
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{settings.COMMAND_PREFIX}hastebin (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="message",
                        description=f" ⚠️``{ctx.author}`` need to specify of messages to put in hastebin ``{settings.COMMAND_PREFIX}hastebin (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    async def pastebin(self, ctx: commands.Context, *, message):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            data = {
                "api_option": "paste",
                "api_dev_key": settings.pastebinapi,
                "api_paste_code": message,
                "api_paste_name": "Smilewinbot",
                "api_paste_expire_date": "N",
                "api_user_key": "",
                "api_paste_format": "python",
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://pastebin.com/api/api_post.php", data=data
                ) as r:
                    r = await r.text()

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"Pastebin link ของ {ctx.author}",
                    description=f"""
```📒 นี้คือลิงค์ Pastebin ของคุณ : 

{r}```""",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("📒")
                print(f"{ctx.author} have made a Pastebinlink : {r}")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"Pastebin link ของ {ctx.author}",
                    description=f"""
```📒 This is your Pastebin link : 

{r}```""",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("📒")
                print(f"{ctx.author} have made a Pastebinlink : {r}")

    @pastebin.error
    async def pastebin_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ข้อความที่ต้องการที่จะใส่",
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{settings.COMMAND_PREFIX}pastebin (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="message",
                        description=f" ⚠️``{ctx.author}`` need to specify of messages to put in pastebin ``{settings.COMMAND_PREFIX}pastebin (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    async def qr(self, ctx: commands.Context, *, text):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)}"

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title="💻 QR CODE GENERATOR",
                    description=f"ลิงค์ : [คลิกที่นี้](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)})",
                )
                embed.set_image(url=url)
                await ctx.send(embed=embed)

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title="💻 QR CODE GENERATOR",
                    description=f"link : [click here](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)})",
                )
                embed.set_image(url=url)
                await ctx.send(embed=embed)

    @qr.error
    async def qr_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่จะเขียนใน QR code ``{settings.COMMAND_PREFIX}qr [message]``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` need to specify what to write on QR code ``{settings.COMMAND_PREFIX}qr [message]``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    async def say(self, ctx: commands.Context, message):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            if "//" in message:
                message = message.replace("//", "\n")

            await ctx.send(message)

    @commands.command()
    async def embed(self, ctx: commands.Context, *, message):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            if "/*/" in message:
                message = message.replace("/*/", "\n")

            embed = nextcord.Embed(colour=0x00FFFF, description=f"{message}")

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)

    @embed.error
    async def embed_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็น embed ``{settings.COMMAND_PREFIX}embed (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` Specify text to make into embed ``{settings.COMMAND_PREFIX}embed (message)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    async def webhook(self, ctx: commands.Context, webhook_url, *, message):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                try:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhook_url, session=session)
                        await webhook.send(
                            message,
                            avatar_url=self.bot.user.avatar.url,
                            username="Smilewinbot",
                        )

                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ส่งข้อความไปยังwebhook",
                        description=f"""```
    ข้อความ :
    {message}```""",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                except nextcord.InvalidArgument:
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ไม่สามารถส่งข้อความไปยังwebhook",
                        description="Webhook อาจจะผิดโปรดตรวจสอบ",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                try:
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(webhook_url, session=session)
                        await webhook.send(
                            message,
                            avatar_url=self.bot.user.avatar.url,
                            username="Smilewinbot",
                        )

                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="sending message to webhook",
                        description=f"""```
    message :
    {message}```""",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                except nextcord.InvalidArgument:
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Unable to send to webhook",
                        description="Webhook might not be valid",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")


def setup(bot: commands.Bot):
    bot.add_cog(Shortener(bot))
