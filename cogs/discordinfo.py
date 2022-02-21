from ast import alias
import nextcord
from nextcord import colour
import humanize
from utils.languageembed import languageEmbed
import settings
import datetime
import platform
import psutil
import requests
from nextcord.ext import commands

PYTHON_VERSION = platform.python_version()
OS = platform.system()
start_time = datetime.datetime.utcnow()
developer = "REACT#1120"


class DiscordInfo(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def channelinfo(self, ctx, channel: nextcord.TextChannel = None):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if channel is None:
                channel = ctx.channel

            if server_language == "Thai":
                embed = nextcord.Embed(title="ข้อมูลช่องเเชท", colour=0xFED000)
                embed.add_field(name="ชื่อช่องเเชท", value=f"```{channel.name}```")
                embed.add_field(name="ID ช่องเเชท", value=f"```{channel.id}```")
                embed.add_field(
                    name="หัวข้อช่องเเชท", value=f"```{channel.topic}```", inline=False
                )
                embed.add_field(
                    name="ประเภท", value=f"```{(str(channel.type)).upper()}```"
                )
                embed.add_field(
                    name="หมวดหมู่ช่องเเชท", value=f"```{channel.category}```"
                )
                embed.add_field(
                    name="วันที่สร้างเซิฟเวอร์",
                    value="```"
                    + channel.created_at.strftime("%Y/%m/%d %I:%M %p")
                    + "```",
                    inline=False,
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await ctx.send(embed=embed)

            if server_language == "English":
                embed = nextcord.Embed(title="ข้อมูลช่องเเชท", colour=0xFED000)
                embed.add_field(name="ชื่อช่องเเชท", value=f"```{channel.name}```")
                embed.add_field(name="ID ช่องเเชท", value=f"```{channel.id}```")
                embed.add_field(
                    name="หัวข้อช่องเเชท", value=f"```{channel.topic}```", inline=False
                )
                embed.add_field(
                    name="ประเภท", value=f"```{(str(channel.type)).upper()}```"
                )
                embed.add_field(
                    name="หมวดหมู่ช่องเเชท", value=f"```{channel.category}```"
                )
                embed.add_field(
                    name="วันที่สร้างเซิฟเวอร์",
                    value="```"
                    + channel.created_at.strftime("%Y/%m/%d %I:%M %p")
                    + "```",
                    inline=False,
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await ctx.send(embed=embed)

    @commands.command()
    async def myid(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                await ctx.send(
                    f"{ctx.author.mention},\nYour user ID: {ctx.author.id}\nThis server ID: {ctx.guild.id}"
                )

            if server_language == "English":
                await ctx.send(
                    f"{ctx.author.mention},\nYour user ID: {ctx.author.id}\nThis server ID: {ctx.guild.id}"
                )

    @commands.command()
    async def membercount(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            totalmember = ctx.guild.member_count
            memberonly = len([member for member in ctx.guild.members if not member.bot])
            botonly = int(totalmember) - int(memberonly)
            memberonline = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.online
                ]
            )
            memberoffline = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.offline
                ]
            )
            memberidle = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.idle
                ]
            )
            memberbusy = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.dnd
                ]
            )
            totalonline = memberonline + memberidle + memberbusy
            if server_language == "Thai":
                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title=f"สมาชิกใน {ctx.guild.name}",
                    description=f"""

```❤️ สมาชิกทั้งหมด : {totalmember}
🧡 สมาชิกที่เป็นคน : {memberonly}
💛 สมาชิกที่เป็นบอท : {botonly}```
> <:online:{settings.online_id}> ออนไลน์ทั้งหมด : ``{totalonline}``
> <:online:{settings.online_id}> สถานะออนไลน์ : ``{memberonline}``
> <:idle:{settings.idle_id}> สถานะไม่อยู่ : ``{memberidle}``
> <:busy:{settings.busy_id}> สถานะห้ามรบกวน : ``{memberbusy}``
> <:offline:{settings.offline_id}> สถานะออฟไลน์ : ``{memberoffline}``""",
                )

                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("❤️")
            if server_language == "English":
                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title=f"members in {ctx.guild.name}",
                    description=f"""

```❤️ Total member : {totalmember}
🧡 Human member : {memberonly}
💛 Bot member : {botonly}```
> <:online:{settings.online_id}>**Total online**: ``{totalonline}``
> <:online:{settings.online_id}>**Online member**: ``{memberonline}``
> <:idle:{settings.idle_id}>**Idle member**: ``{memberidle}``
> <:busy:{settings.busy_id}>**Busy member**: ``{memberbusy}``
> <:offline:{settings.offline_id}>**Offline member**: ``{memberoffline}``""",
                )

                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("❤️")

    @commands.command()
    async def uptime(self, ctx):
        uptime = datetime.datetime.utcnow() - start_time
        uptime = str(uptime).split(".")[0]
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":

                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title="เวลาทำงานของบอท Smilewin",
                    description="```🕒 " + uptime + "```",
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("🕒")

            if server_language == "English":

                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title="Smilewin bot uptime",
                    description="```🕒 " + uptime + "```",
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("🕒")

    @commands.command()
    async def serverinfo(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            totalmember = ctx.guild.member_count
            memberonly = len([member for member in ctx.guild.members if not member.bot])
            botonly = int(totalmember) - int(memberonly)
            memberonline = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.online
                ]
            )
            memberoffline = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.offline
                ]
            )
            memberidle = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.idle
                ]
            )
            memberbusy = len(
                [
                    member
                    for member in ctx.guild.members
                    if not member.bot and member.status is nextcord.Status.dnd
                ]
            )
            connect = sum(
                [
                    len(voice_channel.members)
                    for voice_channel in ctx.guild.voice_channels
                ]
            )
            totalonline = memberonline + memberidle + memberbusy
            nitro_teir = ctx.guild.premium_tier
            num_boost = ctx.guild.premium_subscription_count
            bannedmember = len(await ctx.guild.bans())
            totalinvite = len(await ctx.guild.invites())
            animated = len([emoji for emoji in ctx.guild.emojis if emoji.animated])
            normal = len([emoji for emoji in ctx.guild.emojis if not emoji.animated])
            time = str(ctx.guild.created_at).split()[0]

            if server_language == "Thai":
                if "COMMUNITY" in ctx.guild.features:  # it's a community server
                    guild_type = "เซิร์ฟเวอร์สาธารณะ"
                else:
                    guild_type = "เซิร์ฟเวอร์ส่วนบุคคล"

                if (
                    "VERIFIED" in ctx.guild.features
                    or "PARTNERED" in ctx.guild.features
                ):
                    verify = "ได้รับการยืนยัน"

                else:
                    verify = "ไม่ได้รับการยืนยัน"

                if "VANITY_URL" in ctx.guild.features:
                    invite = f"https://discord.gg/{ctx.guild.vanity_url_code}"

                else:
                    invite = "ไม่มี"

                if str(ctx.guild.verification_level) == "none":
                    verification_level = "ไม่มี"

                elif str(ctx.guild.verification_level) == "low":
                    verification_level = "ตํ่า"

                elif str(ctx.guild.verification_level) == "medium":
                    verification_level = "ปานกลาง"

                elif str(ctx.guild.verification_level) == "high":
                    verification_level = "สูง"

                elif str(ctx.guild.verification_level) == "extreme":
                    verification_level = "สูงมาก"

                else:
                    verification_level = "ไม่รู้"

                embed = nextcord.Embed(
                    colour=0xFFFF00,
                    title=f"ข้อมูลเซิฟเวอร์📊",
                    description=f"""**ข้อมูลทั่วไป**
❯❯ 🏠**ชื่อเซิฟเวอร์**: {ctx.guild.name}
❯❯ 🆔**ไอดีของเซิฟเวอร์**: {ctx.guild.id}
❯❯ 👑**เจ้าของเซิฟเวอร์**: {ctx.guild.owner} ({ctx.guild.owner.id})
❯❯ 🌎**ภูมิภาคของเซิฟเวอร์**: {ctx.guild.region}
❯❯ <a:partner:{settings.partner_id}>**ประเภทเซิร์ฟเวอร์**: {guild_type}
❯❯ <:verify:{settings.verify_id}>**การยืนยันเซิร์ฟเวอร์**: {verify}
❯❯ 🔗**โคดเชิญแบบกำหนดเอง**: {invite}
❯❯ <:boost:{settings.boost_id}>**บูสทั้งหมด**: {num_boost} บูส Level {nitro_teir}
❯❯ :shield:**ระดับความปลอดภัย**: {verification_level}
❯❯ :timer:**วันที่สร้างเซิฟเวอร์**: {time}

**สถิติของเซิฟเวอร์**
❯❯ <:member:{settings.member_id}>**สมาชิกทั้งหมด**: {ctx.guild.member_count}
❯❯ <:member:{settings.member_id}>**สมาชิกที่เป็นคน**: {memberonly}
❯❯ <:member:{settings.member_id}>**สมาชิกที่เป็นบอท**: {botonly}
❯❯ <:member:{settings.member_id}>**สมาชิกที่ถูกเเบน**: {bannedmember}
❯❯ <:channel:{settings.channel_id}>**ประเภท**: {len(ctx.guild.categories)}
❯❯ <:channel:{settings.channel_id}>**ห้องเเชท**: {len(ctx.guild.text_channels)}
❯❯ <:channel:{settings.channel_id}>**ห้องพูดคุย**: {len(ctx.guild.voice_channels)}
❯❯ <:channel:{settings.channel_id}>**ห้องเเสดง**: {len(ctx.guild.stage_channels)}
❯❯ <:role:{settings.role_id}>**ยศทั้งหมด**: {len(ctx.guild.roles)}
❯❯ <:emoji:{settings.emoji_id}>**อีโมจิทั้งหมด**: {len(ctx.guild.emojis)}
❯❯ <:emoji:{settings.emoji_id}>**อีโมจิแบบเคลื่อนไหว**: {animated}
❯❯ <:emoji:{settings.emoji_id}>**อีโมจิแบบปกติ**: {normal}
❯❯ 🔗**ลิงค์เชิญทั้งหมด**: {totalinvite}

**สถานะของสมาชิกในเซิฟเวอร์**
❯❯ <:online:{settings.online_id}>**ออนไลน์ทั้งหมด**: {totalonline}
❯❯ <:online:{settings.online_id}>**สถานะออนไลน์**: {memberonline}
❯❯ <:idle:{settings.idle_id}>**สถานะไม่อยู่**: {memberidle}
❯❯ <:busy:{settings.busy_id}>**สถานะห้ามรบกวน**: {memberbusy}
❯❯ <:offline:{settings.offline_id}>**สถานะออฟไลน์**: {memberoffline}
❯❯ 🎤**สมาชิกในห้องเสียง**: {connect}
""",
                )
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

            if server_language == "English":
                if "COMMUNITY" in ctx.guild.features:  # it's a community server
                    guild_type = "Community server"
                else:
                    guild_type = "Private server"

                if (
                    "VERIFIED" in ctx.guild.features
                    or "PARTNERED" in ctx.guild.features
                ):
                    verify = "verified"

                else:
                    verify = "not verified"

                if "VANITY_URL" in ctx.guild.features:
                    invite = f"https://discord.gg/{ctx.guild.vanity_url_code}"

                else:
                    invite = "None"

                if str(ctx.guild.verification_level) == "none":
                    verification_level = "None"

                elif str(ctx.guild.verification_level) == "low":
                    verification_level = "Low"

                elif str(ctx.guild.verification_level) == "medium":
                    verification_level = "Medium"

                elif str(ctx.guild.verification_level) == "high":
                    verification_level = "High"

                elif str(ctx.guild.verification_level) == "extreme":
                    verification_level = "Very High"

                else:
                    verification_level = "Don't know"

                embed = nextcord.Embed(
                    colour=0xFFFF00,
                    title=f"Server Information📊",
                    description=f"""**General Information**
❯❯ 🏠**Server Name**: {ctx.guild.name}
❯❯ 🆔**Server ID**: {ctx.guild.id}
❯❯ 👑**Server Owner**: {ctx.guild.owner} ({ctx.guild.owner.id})
❯❯ 🌎**Server Region**: {ctx.guild.region}
❯❯ <a:partner:{settings.partner_id}>**Server type**: {guild_type}
❯❯ <:verify:{settings.verify_id}>**Server Verification**: {verify}
❯❯ 🔗**vanity code**: {invite}
❯❯ <:boost:{settings.boost_id}>**Total boost**: {num_boost} Boost Level {nitro_teir}
❯❯ :shield:**Verification Level**: {verification_level}
❯❯ :timer:**Server creation date**: {time}

**Server Statistics**
❯❯ <:member:{settings.member_id}>**Total members**: {ctx.guild.member_count}
❯❯ <:member:{settings.member_id}>**Members**: {memberonly}
❯❯ <:member:{settings.member_id}>**Bots**: {botonly}
❯❯ <:member:{settings.member_id}>**Banned members**: {bannedmember}
❯❯ <:channel:{settings.channel_id}>**Categories**: {len(ctx.guild.categories)}
❯❯ <:channel:{settings.channel_id}>**Text channels**: {len(ctx.guild.text_channels)}
❯❯ <:channel:{settings.channel_id}>**Voice channels**: {len(ctx.guild.voice_channels)}
❯❯ <:channel:{settings.channel_id}>**Stage channels**: {len(ctx.guild.stage_channels)}
❯❯ <:role:{settings.role_id}>**Total roles**: {len(ctx.guild.roles)}
❯❯ <:emoji:{settings.emoji_id}>**Total emoji**: {len(ctx.guild.emojis)}
❯❯ <:emoji:{settings.emoji_id}>**Animated emoji**: {animated}
❯❯ <:emoji:{settings.emoji_id}>**Normal emoji**: {normal}
❯❯ 🔗**ลิงค์เชิญทั้งหมด**: {totalinvite}

**Server member status**
❯❯ <:online:{settings.online_id}>**Total online**: {totalonline}
❯❯ <:online:{settings.online_id}>**Online**: {memberonline}
❯❯ <:idle:{settings.idle_id}>**Idle**: {memberidle}
❯❯ <:busy:{settings.busy_id}>**Busy**: {memberbusy}
❯❯ <:offline:{settings.offline_id}>**Offline**: {memberoffline}
❯❯ 🎤**Voice connected**: {connect}
""",
                )
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

    @commands.command(aliases=["botstat"])
    async def botinfo(self, ctx):
        uptime = datetime.datetime.utcnow() - start_time
        uptime = str(uptime).split(".")[0]

        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":

                embed = nextcord.Embed(
                    colour=0xFFFF00, title="ข้อมูลของบอท Smilewin bot"
                )

                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(
                    name="🤖 ``ชื่อของบอท``", value=f"{self.bot.user}", inline=False
                )
                embed.add_field(
                    name="🏆 ``ผู้พัฒนาบอท``", value=f"{developer}", inline=False
                )
                embed.add_field(
                    name="📁 ``จํานวนเซิฟเวอร์``",
                    value=f"{humanize.intcomma(len(self.bot.guilds))}",
                )
                embed.add_field(
                    name="📁 ``จํานวนคําสั่ง``", value=f"{len(self.bot.commands)}"
                )
                embed.add_field(
                    name="📁 ``สมาชิกทั้งหมด``",
                    value=f"{humanize.intcomma(len(self.bot.users))}",
                )
                embed.add_field(
                    name="🤖 ``เครื่องหมายหน้าคำสั่ง``",
                    value=f"{settings.COMMAND_PREFIX}",
                )
                embed.add_field(
                    name="🤖 ``คําสั่งช่วยเหลือ``",
                    value=f"{settings.COMMAND_PREFIX}help",
                )
                embed.add_field(name="🤖 ``เวลาทำงาน``", value=f"{uptime}")
                embed.add_field(
                    name="🤖 ``Ping ของบอท``",
                    value=f"{round(self.bot.latency * 1000)}ms",
                )
                embed.add_field(name="💻 ``ระบบปฏิบัติการ``", value=f"{OS}")
                embed.add_field(
                    name="💻 ``เเรมที่ใช้``",
                    value=f"{psutil.virtual_memory().percent} %",
                )
                embed.add_field(
                    name="🤖 ``ภาษาที่ใช้เขียนบอท``", value=f"Python {PYTHON_VERSION}"
                )
                embed.add_field(
                    name="🤖 ``Nextcord.py``",
                    value=f"Nextcord.py {nextcord.__version__}",
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_thumbnail(url=self.bot.user.avatar.url)

                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

            if server_language == "English":

                embed = nextcord.Embed(colour=0xFFFF00, title="Smilewin bot info")

                embed.timestamp = datetime.datetime.utcnow()
                embed.add_field(
                    name="🤖 ``Bot name``", value=f"{self.bot.user}", inline=False
                )
                embed.add_field(
                    name="🏆 ``Developer``", value=f"{developer}", inline=False
                )
                embed.add_field(
                    name="📁 ``Total servers``",
                    value=f"{humanize.intcomma(len(self.bot.guilds))}",
                )
                embed.add_field(
                    name="📁 ``Total commands``", value=f"{len(self.bot.commands)}"
                )
                embed.add_field(
                    name="📁 ``Total user``",
                    value=f"{humanize.intcomma(len(self.bot.users))}",
                )
                embed.add_field(
                    name="🤖 ``Command prefix``", value=f"{settings.COMMAND_PREFIX}"
                )
                embed.add_field(
                    name="🤖 ``Help command``", value=f"{settings.COMMAND_PREFIX}help"
                )
                embed.add_field(name="🤖 ``Bot uptime``", value=f"{uptime}")
                embed.add_field(
                    name="🤖 ``Bot ping``", value=f"{round(self.bot.latency * 1000)}ms"
                )
                embed.add_field(name="💻 ``OS``", value=f"{OS}")
                embed.add_field(
                    name="💻 ``RAM``", value=f"{psutil.virtual_memory().percent} %"
                )
                embed.add_field(
                    name="🤖 ``Programming language``", value=f"Python {PYTHON_VERSION}"
                )
                embed.add_field(
                    name="🤖 ``Nextcord.py``",
                    value=f"Nextcord.py {nextcord.__version__}",
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_thumbnail(url=self.bot.user.avatar.url)

                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

    @commands.command()
    async def userinfo(self, ctx, member: nextcord.Member = None):

        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if member is None:
                member = ctx.author

            roles = [role for role in member.roles]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=member.color, title=f"ข้อมูลของสมาชิก {member}"
                )
                embed.set_author(
                    name=f"ข้อมูลของ {member}", icon_url=f"{member.avatar.url}"
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(
                    text=f"┗Requested by {ctx.author}", icon_url=ctx.author.avatar.url
                )
                embed.add_field(name="```ID ของสมาชิก:```", value=member.id)
                embed.add_field(name="```ชื่อในเซิฟ:```", value=member.display_name)
                embed.add_field(
                    name="```วันที่สมัคร:```",
                    value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                )
                embed.add_field(
                    name="```วันที่เข้าเซิฟ:```",
                    value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                )
                embed.add_field(
                    name=f"```ยศทั้งหมด:```({len(roles)})",
                    value=" ".join([role.mention for role in roles]),
                )
                embed.add_field(name="```ยศสูงสุด:```", value=member.top_role.mention)
                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

            if server_language == "English":
                embed = nextcord.Embed(colour=member.color, title=f"Info of {member}")
                embed.set_author(
                    name=f"Info of {member}", icon_url=f"{member.avatar.url}"
                )
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(
                    text=f"┗Requested by {ctx.author}", icon_url=ctx.author.avatar.url
                )
                embed.add_field(name="```Member id:```", value=member.id)
                embed.add_field(
                    name="```Member nickname:```", value=member.display_name
                )
                embed.add_field(
                    name="```Creation date:```",
                    value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                )
                embed.add_field(
                    name="```Joined date:```",
                    value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                )
                embed.add_field(
                    name=f"```All roles:```({len(roles)})",
                    value=" ".join([role.mention for role in roles]),
                )
                embed.add_field(
                    name="```Highest role:```", value=member.top_role.mention
                )
                message = await ctx.send(embed=embed)
                await message.add_reaction("🤖")

    @commands.command()
    async def ping(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            latency = requests.get("https://discord.com/").elapsed.total_seconds()
            if server_language == "English":

                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title="Smilewin bot ping",
                    description=f"""
```⌛ Ping : {round(self.bot.latency * 1000)}ms
⌛ Discord Latency : {round(latency * 1000)}ms```
    
    """,
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("⌛")
                print(
                    f"{ctx.author} ping bot and the latency is {round(self.bot.latency * 1000)}ms"
                )

            if server_language == "Thai":

                embed = nextcord.Embed(
                    color=0xFFFF00,
                    title="Smilewin bot ping",
                    description=f"""
```⌛ ปิงของบอท : {round(self.bot.latency * 1000)}ms
⌛ เวลาในการตอบสนอง Discord : {round(latency * 1000)}ms```
        
        """,
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message = await ctx.send(embed=embed)
                await message.add_reaction("⌛")
                print(
                    f"{ctx.author} ping bot and the latency is {round(self.bot.latency * 1000)}ms"
                )

    @commands.command()
    async def avatar(self, ctx, member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if member is None:
                member = ctx.author

            if server_language == "Thai":

                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"รูปของสมาชิก: {member}",
                    description=f"ลิงค์ : [คลิกที่นี้]({member.avatar.url})",
                )
                embed.set_image(url=member.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":

                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"{member} profile picture",
                    description=f"link : [click here]({member.avatar.url})",
                )
                embed.set_image(url=member.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @commands.command()
    async def searchavatar(self, ctx, member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if member is None:
                member = ctx.author

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"หารูปของสมาชิก: {member}",
                    description=f"https://images.google.com/searchbyimage?image_url={member.avatar.url}",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"search for {member} profile picture",
                    description=f"https://images.google.com/searchbyimage?image_url={member.avatar.url}",
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @commands.command()
    async def credit(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    title="💻 เครดิตคนทําบอท",
                    description="""
    ```ดิสคอร์ด : REACT#1120
    เซิฟดิสคอร์ด : https://discord.com/invite/R8RYXyB4Cg
    Github : https://github.com/reactxsw```
                    """,
                    colour=0x00FFFF,
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="💻 Developer",
                    description="""
    ```Discord : REACT#1120
    Discord server : https://discord.com/invite/R8RYXyB4Cg
    Github : https://github.com/reactxsw```
                    """,
                    colour=0x00FFFF,
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def guildicon(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF, title=f"เซิฟเวอร์: {ctx.guild.name}"
                )
                embed.set_image(url=ctx.guild.icon.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF, title=f"Server: {ctx.guild.name}"
                )
                embed.set_image(url=ctx.guild.icon.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @commands.command(alias=["invite"])
    async def botinvite(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":

                invitelink = str(
                    f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot"
                )
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"ลิงค์เชิญบอท SmileWin : ",
                    description=f"[คลิกที่นี้]({invitelink})",
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction("💖")

            if server_language == "English":

                invitelink = str(
                    f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot"
                )
                embed = nextcord.Embed(
                    colour=0x00FFFF,
                    title=f"invite link : ",
                    description=f"[click here]({invitelink})",
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction("💖")

    @commands.command()
    async def setting(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่า",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setup",
                        colour=0x983925,
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("👍")

                else:
                    database_id = server["_id"]
                    welcome_channel_id = server["welcome_id"]
                    leave_channel_id = server["leave_id"]
                    webhook_id = server["webhook_channel_id"]
                    introduce_id = server["introduce_channel_id"]
                    verification_id = server["verification_channel_id"]
                    webhook_stat = server["webhook_status"]
                    economy_stat = server["economy_system"]
                    verification_stat = server["verification_system"]
                    introduce_stat = server["introduce_status"]
                    level_stat = server["level_system"]
                    introduce_give = server["introduce_role_give_id"]
                    introduce_remove = server["introduce_role_remove_id"]
                    verify_give = server["verification_role_give_id"]
                    verify_remove = server["verification_role_remove_id"]
                    verify_time = server["verification_time"]
                    server_currency = server["currency"]
                    intro_frame = server["introduce_frame"]
                    log_voice = server["log_voice_system"]
                    log_channel = server["log_channel_id"]
                    verify_time = str(verify_time)
                    if introduce_give != "None":
                        introduce_give = ctx.guild.get_role(int(introduce_give))
                    else:
                        introduce_give = "None"
                    if introduce_remove != "None":
                        introduce_remove = ctx.guild.get_role(int(introduce_remove))
                    else:
                        introduce_remove = "None"
                    if verify_give != "None":
                        verify_give = ctx.guild.get_role(int(verify_give))
                    else:
                        verify_give = "None"
                    if verify_remove != "None":
                        verify_remove = ctx.guild.get_role(int(verify_remove))
                    else:
                        verify_remove = "None"
                    if log_channel != "None":
                        log_channel = ctx.guild.get_channel(int(log_channel))
                    else:
                        log_channel = "None"
                    if welcome_channel_id != "None":
                        welcome_channel_id = ctx.guild.get_channel(
                            int(welcome_channel_id)
                        )
                        if welcome_channel_id:
                            welcome_channel_id = welcome_channel_id
                        else:
                            welcome_channel_id = "None"
                    else:
                        welcome_channel_id = "None"
                    if leave_channel_id != "None":
                        leave_channel_id = ctx.guild.get_channel(int(leave_channel_id))
                        if leave_channel_id:
                            leave_channel_id = leave_channel_id
                        else:
                            leave_channel_id = "None"
                    else:
                        leave_channel_id = "None"
                    if webhook_id != "None":
                        webhook_id = ctx.guild.get_channel(int(webhook_id))
                        if webhook_id:
                            webhook_id = webhook_id
                        else:
                            webhook_id = "None"
                    else:
                        webhook_id = "None"
                    if introduce_id != "None":
                        introduce_id = ctx.guild.get_channel(int(introduce_id))
                        if introduce_id:
                            introduce_id = introduce_id
                        else:
                            introduce_id = "None"
                    else:
                        introduce_id = "None"
                    if verification_id != "None":
                        verification_id = ctx.guild.get_channel(int(verification_id))
                        if verification_id:
                            verification_id = verification_id
                        else:
                            verification_id = "None"
                    else:
                        verification_id = "None"
                    embed = nextcord.Embed(
                        title="การตั้งค่าของ Server",
                        description=f"```Database ID : {database_id}```",
                        colour=0x00FFFF,
                    )
                    embed.add_field(
                        name="ตั้งค่าห้อง",
                        value=f"```ห้องเเจ้งเตือนคนเข้า : {welcome_channel_id}\nห้องเเจ้งเตือนคนออก : {leave_channel_id}\nห้องคุยกับคนเเปลกหน้า : {webhook_id}\nห้องเเนะนําตัว : {introduce_id}\nห้องยืนยันตัวตน : {verification_id}\nห้องลงบันทึก : {log_channel}```",
                    )
                    embed.add_field(
                        name="ID เซิฟเวอร์",
                        value=f"```{ctx.guild.name}\n({ctx.guild.id})```",
                        inline=False,
                    )
                    embed.add_field(
                        name="ตั้งค่ายศ",
                        value=f"```ให้ยศเเนะนําตัว : \n{introduce_give}\nลบยศเเนะนําตัว : \n{introduce_remove}\nให้ยศยืนยันตัวตน : \n{verify_give}\nลบยศยืนยันตัวตน : \n{verify_remove}```",
                    )
                    embed.add_field(
                        name="ตั้งค่าระบบ",
                        value=f"```คุยกับคนเเปลกหน้า : {webhook_stat}\nระบบเลเวล : {level_stat}\nระบบเศรษฐกิจ : {economy_stat}\nระบบยืนยันตัวตน : {verification_stat}\nระบบเเนะนําตัว : {introduce_stat}\nลงบันทึกเข้าห้อง : {log_voice}```",
                    )
                    embed.add_field(
                        name="ตั้งค่าอื่นๆ",
                        value=f"```ค่าเงิน : {server_currency}\nกรอบเเนะนําตัว : {intro_frame}\nเวลายืนยันตัว : {verify_time}วิ```",
                        inline=False,
                    )
                    embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("👍")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่า",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setup",
                        colour=0x983925,
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("👍")

                else:
                    database_id = server["_id"]
                    welcome_channel_id = server["welcome_id"]
                    leave_channel_id = server["leave_id"]
                    webhook_id = server["webhook_channel_id"]
                    introduce_id = server["introduce_channel_id"]
                    verification_id = server["verification_channel_id"]
                    webhook_stat = server["webhook_status"]
                    economy_stat = server["economy_system"]
                    verification_stat = server["verification_system"]
                    introduce_stat = server["introduce_status"]
                    level_stat = server["level_system"]
                    introduce_give = server["introduce_role_give_id"]
                    introduce_remove = server["introduce_role_remove_id"]
                    verify_give = server["verification_role_give_id"]
                    verify_remove = server["verification_role_remove_id"]
                    verify_time = server["verification_time"]
                    server_currency = server["currency"]
                    intro_frame = server["introduce_frame"]
                    log_voice = server["log_voice_system"]
                    log_channel = server["log_channel_id"]
                    verify_time = str(verify_time)
                    if introduce_give != "None":
                        introduce_give = ctx.guild.get_role(int(introduce_give))
                    else:
                        introduce_give = "None"
                    if introduce_remove != "None":
                        introduce_remove = ctx.guild.get_role(int(introduce_remove))
                    else:
                        introduce_remove = "None"
                    if verify_give != "None":
                        verify_give = ctx.guild.get_role(int(verify_give))
                    else:
                        verify_give = "None"
                    if verify_remove != "None":
                        verify_remove = ctx.guild.get_role(int(verify_remove))
                    else:
                        verify_remove = "None"
                    if log_channel != "None":
                        log_channel = ctx.guild.get_channel(int(log_channel))
                    else:
                        log_channel = "None"
                    if welcome_channel_id != "None":
                        welcome_channel_id = ctx.guild.get_channel(
                            int(welcome_channel_id)
                        )
                        if welcome_channel_id:
                            welcome_channel_id = welcome_channel_id
                        else:
                            welcome_channel_id = "None"
                    else:
                        welcome_channel_id = "None"
                    if leave_channel_id != "None":
                        leave_channel_id = ctx.guild.get_channel(int(leave_channel_id))
                        if leave_channel_id:
                            leave_channel_id = leave_channel_id
                        else:
                            leave_channel_id = "None"
                    else:
                        leave_channel_id = "None"
                    if webhook_id != "None":
                        webhook_id = ctx.guild.get_channel(int(webhook_id))
                        if webhook_id:
                            webhook_id = webhook_id
                        else:
                            webhook_id = "None"
                    else:
                        webhook_id = "None"
                    if introduce_id != "None":
                        introduce_id = ctx.guild.get_channel(int(introduce_id))
                        if introduce_id:
                            introduce_id = introduce_id
                        else:
                            introduce_id = "None"
                    else:
                        introduce_id = "None"
                    if verification_id != "None":
                        verification_id = ctx.guild.get_channel(int(verification_id))
                        if verification_id:
                            verification_id = verification_id
                        else:
                            verification_id = "None"
                    else:
                        verification_id = "None"
                    embed = nextcord.Embed(
                        title="การตั้งค่าของ Server",
                        description=f"```Database ID : {database_id}```",
                        colour=0x00FFFF,
                    )
                    embed.add_field(
                        name="Channel settings",
                        value=f"```ห้องเเจ้งเตือนคนเข้า : {welcome_channel_id}\nห้องเเจ้งเตือนคนออก : {leave_channel_id}\nห้องคุยกับคนเเปลกหน้า : {webhook_id}\nห้องเเนะนําตัว : {introduce_id}\nห้องยืนยันตัวตน : {verification_id}\nห้องลงบันทึก : {log_channel}```",
                    )
                    embed.add_field(
                        name="Server ID",
                        value=f"```{ctx.guild.name}\n({ctx.guild.id})```",
                        inline=False,
                    )
                    embed.add_field(
                        name="ตั้งค่ายศ",
                        value=f"```ให้ยศเเนะนําตัว : \n{introduce_give}\nลบยศเเนะนําตัว : \n{introduce_remove}\nให้ยศยืนยันตัวตน : \n{verify_give}\nลบยศยืนยันตัวตน : \n{verify_remove}```",
                    )
                    embed.add_field(
                        name="ตั้งค่าระบบ",
                        value=f"```คุยกับคนเเปลกหน้า : {webhook_stat}\nระบบเลเวล : {level_stat}\nระบบเศรษฐกิจ : {economy_stat}\nระบบยืนยันตัวตน : {verification_stat}\nระบบเเนะนําตัว : {introduce_stat}\nลงบันทึกเข้าห้อง : {log_voice}```",
                    )
                    embed.add_field(
                        name="ตั้งค่าอื่นๆ",
                        value=f"```ค่าเงิน : {server_currency}\nกรอบเเนะนําตัว : {intro_frame}\nเวลายืนยันตัว : {verify_time}วิ```",
                        inline=False,
                    )
                    embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("👍")

    @commands.command()
    async def servers(self, ctx, n: int = 10):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                servers = list(self.bot.guilds)
                n = min(n, len(servers))
                embed = nextcord.Embed(title=f"{n} อันดับเซิฟเวอร์", colour=0x00FFFF)
                for server in sorted(
                    servers, key=lambda x: x.member_count, reverse=True
                )[:n]:
                    embed.add_field(
                        name=server.name,
                        value=f"{server.member_count} members",
                        inline=False,
                    )
                await ctx.send(embed=embed)

            if server_language == "English":
                servers = list(self.bot.guilds)
                n = min(n, len(servers))
                embed = nextcord.Embed(title=f"Top {n} servers", colour=0x00FFFF)
                for server in sorted(
                    servers, key=lambda x: x.member_count, reverse=True
                )[:n]:
                    embed.add_field(
                        name=server.name,
                        value=f"{server.member_count} members",
                        inline=False,
                    )
                await ctx.send(embed=embed)

    @commands.command()
    async def botvote(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    title=f"โหวตให้บอท {self.bot.user}",
                    colour=0x00FFFF,
                    description=f"[discordbotlist](https://discordbotlist.com/bots/smilewin/upvote)"
                    + "\n"
                    + "[Top.gg](https://discordbotlist.com/bots/smilewin/upvote)",
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🙏")

            if server_language == "English":
                embed = nextcord.Embed(
                    title=f"Vote for {self.bot.user}",
                    colour=0x00FFFF,
                    description=f"[discordbotlist](https://discordbotlist.com/bots/smilewin/upvote)"
                    + "\n"
                    + "[Top.gg](https://discordbotlist.com/bots/smilewin/upvote)",
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("🙏")

    @commands.command()
    async def test(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                await ctx.send("Bot online เเล้ว")

            if server_language == "English":
                await ctx.send("Bot is online")

    @commands.command()
    async def support(self, ctx, *, message=None):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                channel = self.bot.get_channel(int(settings.supportchannel))
                if not message is None:
                    embed = nextcord.Embed(
                        title=f"ปัญหาบอทโดย {ctx.author}",
                        description=message,
                        colour=0x00FFFF,
                    )
                    await channel.send(embed=embed)

                    embed = nextcord.Embed(
                        title=f"ขอบคุณครับ",
                        description="ปัญหาได้ถูกเเจ้งเรียบร้อย",
                        colour=0x00FFFF,
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title="ระบุปัญหา",
                        description=f"{ctx.author.mention} จะต้องระบุปัญหาที่จะเเจ้งให้ทีมงานทราบ",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

            if server_language == "English":
                channel = self.bot.get_channel(int(settings.supportchannel))
                if not message is None:
                    embed = nextcord.Embed(
                        title=f"ปัญหาบอทโดย {ctx.author}",
                        description=message,
                        colour=0x00FFFF,
                    )
                    await channel.send(embed=embed)

                    embed = nextcord.Embed(
                        title=f"Thank you",
                        description="Bot developer will fix this soon",
                        colour=0x00FFFF,
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = nextcord.Embed(
                        title="Specify problem",
                        description=f"{ctx.author.mention} Must specify the problem that will be notified to the team.",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DiscordInfo(bot))
