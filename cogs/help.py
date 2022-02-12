from os import name
import nextcord
import settings
from nextcord.ext import commands
from utils.languageembed import languageEmbed


class Help(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
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
                    title="คำสั่งสำหรับใช้งานบอท",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}help``",
                    value="ช่วยเหลือคําสั่งช่วยเหลือ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpbot``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับตัวบอท",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpmusic``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับการเปิดเพลง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpfun``",
                    value="ช่วยเหลือคําสั่งบรรเทิง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpgeneral``",
                    value="ช่วยเหลือคําสั่งทั่วไป",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpgame``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับเกม",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpadmin``",
                    value="ช่วยเหลือคําสั่งของเเอดมิน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpsetup``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับตั้งค่า",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpinfo``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับข้อมูล",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpimage``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับรูป",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpeconomy``",
                    value="ช่วยเหลือคําสั่งเกี่ยวกับระบบเศรษฐกิจ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpuser``",
                    value="ช่วยเหลือคําสั่งข้อมูลของสมาชิกเช่น เลเวล",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpnsfw``",
                    value="ช่วยเหลือคําสั่ง 18 +",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpscam``",
                    value="ช่วยเหลือคําสั่งกันลิ้งค์ที่ไม่ปลอดภัย",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helptictactoe``",
                    value="ช่วยเหลือคําสั่งเกม tictactoe(xo)",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="Help command",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}help``", value="help commands"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpbot``",
                    value="help commands related to bot",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpmusic``",
                    value="help commands related to Music",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpfun``",
                    value="help commands related to fun",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpgeneral``",
                    value="help general commands",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpgame``",
                    value="help commands related to game",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpadmin``",
                    value="help commands related to moderator",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpsetup``",
                    value="help commands related to setup",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpinfo``",
                    value="help commands related to information",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpimage``",
                    value="help commands related to image",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpeconomy``",
                    value="help commands related to economy",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpuser``",
                    value="help commands related to user",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpnsfw``",
                    value="help commands related to NSFW",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helpscam``",
                    value="help commands related to scam",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}helptictactoe``",
                    value="help commands related to tictactoe",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpmusic(self, ctx):
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
                    title="คำสั่งสำหรับใช้งานบอท",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}musicsetup ``",
                    value="ตั้งค่าห้องเล่นเพลง",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )

                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "Engish":
                embed = nextcord.Embed(
                    title="คำสั่งสำหรับใช้งานบอท",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}musicsetup ``",
                    value="music room setup",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    Inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpeconomy(self, ctx):
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
                    title="คําสั่งต่างๆเกี่ยวกับระบบเศรษฐกิจ",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}openbal``",
                    value="เปิดบัญชีธนาคาร",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}bal [@member]``",
                    value="ดูเงินของคุณหรือของสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}deposit [amount]``",
                    value="ฝากเงินเข้าธนาคาร",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}withdraw [amount]``",
                    value="ถอนเงินจากธนาคาร",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pay [@member]``",
                    value="โอนเงินจากธนาคารให้สชาชิกในเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}slot [amount]``",
                    value="เล่นพนัน slot",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rob [@member]``",
                    value="ขโมยเงินจากสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}addcredit [amount] [@member]``",
                    value="เพิ่มตังให้สมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}resetmoney [@member]``",
                    value="รีเซ็ทเงินของสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}work``", value="ทํางานหาเงิน"
                )
                embed.add_field(name=f"``{settings.COMMAND_PREFIX}beg``", value="ขอทาน")
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="Instructions for use economy command",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}openbal``",
                    value="open a new balance account",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}bal [@member]``",
                    value="check your balance",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}deposit [amount]``",
                    value="deposit money to the bank",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}withdraw [amount]``",
                    value="withdraw money from the bank",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pay [@member]``",
                    value="pay money to user in the server",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}slot [amount]``",
                    value="slot machine",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rob [@member]``",
                    value="steal money",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}addcredit [amount] [@member]``",
                    value="add money to user",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}resetmoney [@member]``",
                    value="reset a member balance",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}work``",
                    value="work to earn money",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}beg``", value="beg for money"
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    Inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpbot(self, ctx):
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
                    title="คําสั่งเกี่ยวกับตัวบอท",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}test``",
                    value="ดูว่าบอทonline ไหม",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ping``", value="ส่ง ping ของบอท"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}uptime``",
                    value="ส่ง เวลาทำงานของบอท",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botinvite``",
                    value="ส่งลิงค์เชิญบอท",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botvote``", value="โหวตให้บอท"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}credit``", value="เครดิตคนทําบอท"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botinfo``",
                    value="ข้อมูลเกี่ยวกับตัวบอท",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}support [text]``",
                    value="ส่งข้อความหา support หากพบปัญหา",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="help commands related to bot",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}test``",
                    value="test command to see if the bot is online",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ping``", value="send bot ping"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}uptime``", value="send bot uptime"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botinvite``",
                    value="send bot invite link",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botvote``", value="Vote for bot"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}credit``",
                    value="developer credit",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}botinfo``",
                    value="information about bot",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}support [text]``",
                    value="send support if error occur",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpuser(self, ctx):
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
                    title="คําสั่งข้อมูลของสมาชิก",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rank <@member>``",
                    value="เช็คเเรงค์ของคุณหรือสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}leaderboard``",
                    value="ดูอันดับเลเวลของคุณในเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ind``", value="เเนะนําตัว"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}vfy``",
                    value="ยืนยันตัวตนโดย captcha",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="help commands related to user",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rank <@member>``",
                    value="show your level or member level in the server",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}leaderboard``",
                    value="show leaderboard",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ind``", value="introduce yourself"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}vfy``",
                    value="captcha verification",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpsetup(self, ctx):
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
                    title="คําสั่งเกี่ยวกับตั้งค่า",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setting``",
                    value="ดูการตั้งค่าของเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setup``",
                    value="ลงทะเบียนเซิฟเวอร์ในฐานข้อมูล",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setwelcome [#text-channel]``",
                    value="ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setleave [#text-channel]``",
                    value="ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setwebhook [#text-channel]``",
                    value=f"ตั้งค่าห้องที่จะใช้คําสั่ง {settings.COMMAND_PREFIX}anon (message) เพื่อคุยกับคนเเปลกหน้าโดยที่ไม่เปิดเผยตัวตนกับเซิฟเวอร์ที่เปิดใช้คําสั่งนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setintroduce [#text-channel]``",
                    value=f"ตั้งค่าห้องที่จะให้ส่งข้อมูลของสมาชิกหลังจากเเนะนําตัวเสร็จ *พิม {settings.COMMAND_PREFIX}ind เพื่อเเนะนําตัว",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setframe``",
                    value="ตั้งกรอบที่ใส่ข้อมูลของสมาชิกจากปกติเป็น ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setrole give/remove [@role]``",
                    value=f"ตั้งค่าที่จะ ให้/ลบหลังจากเเนะนําตัว",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setverify [#text-channel]``",
                    value=f"ตั้งค่าห้องยืนยันตัวตน (captcha) *พิม {settings.COMMAND_PREFIX}vfy เพื่องยืนยันตัวตน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}verifyrole give/remove [@role]``",
                    value=f"ตั้งค่าที่จะ ให้/ลบหลังจากยืนยันตัวตน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}verifytime [time]``",
                    value=f"ตั้งค่าเวลาในการยืนยันตัวตน (ห้ามเกิน 120 วินาที)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}verification on/off``",
                    value=f"ตั้งค่าที่จะ ให้/ลบหลังจากยืนยันตัวตน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}chat on/off``",
                    value="เปิด / ปิดใช้งานห้องคุยกับคนเเปลกหน้า",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}level on/off``",
                    value="เปิด / ปิดใช้งานระบบเลเวล",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}introduce on/off``",
                    value="เปิด / ปิดการใช้งานคําสั่งเเนะนําตัว",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}economy on/off``",
                    value="เปิด / ปิดการใช้งานระบบเศรษฐกิจ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}logvoice on/off``",
                    value="เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setlog [#text-channel]``",
                    value="เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setserverstat``",
                    value="เปิดใช้งานระบบโชว์สถิตืเซิฟเวอร์",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="help commands related to setup",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setting``",
                    value="show server setting",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setup``",
                    value="set up your server to our database",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}welcomeset [#text-channel]``",
                    value="set up a channel to notify if new member join",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}leaveset [#text-channel]``",
                    value="set up a channel to notify if member left",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setwebhook [#text-channel]``",
                    value=f"setup room to talk to a stranger and use {settings.COMMAND_PREFIX}anon (message) to talk to stranger",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setintroduce [#text-channel]``",
                    value=f"setup a room for member to introduce themself and use {settings.COMMAND_PREFIX}ind to introduce",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setrole give/remove [@role]``",
                    value=f"setup a role to give/remove after a member finish introducing himself/herself",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setframe``",
                    value="set the frame around member information after they introduce themself, Normal frame: ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}chat on/off``",
                    value="turn on/off ability to talk to a stranger",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}level on/off``",
                    value="turn on/off level system",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}introduce on/off``",
                    value="turn on/off introduce command",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}economy on/off``",
                    value="turn on/off an economy system",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}verification on/off``",
                    value="turn on/off an verification system",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}logvoice on/off``",
                    value="เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setlog [#text-channel]``",
                    value="เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}setserverstat``",
                    value="เปิดใช้งานระบบโชว์สถิตืเซิฟเวอร์",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpgame(self, ctx):
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
                    title="คําสั่งเกี่ยวกับเกม",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}coinflip``", value="ทอยเหรียญ"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rps``",
                    value="เป่ายิ้งฉับเเข่งกับบอท",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}roll``",
                    value="ทอยลูกเต๋า",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}8ball [question] ``",
                    value="ดูว่าควรจะทําสิงๆนั้นไหม",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}csgonow``",
                    value="จํานวนคนที่เล่น CSGO ขณะนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}apexnow``",
                    value="จํานวนคนที่เล่น APEX ขณะนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rb6now``",
                    value="จํานวนคนที่เล่น RB6 ขณะนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pubgnow``",
                    value="จํานวนคนที่เล่น PUBG ขณะนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gtanow``",
                    value="จํานวนคนที่เล่น GTA V ขณะนี้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}apexstat [username]``",
                    value="ดูข้อมูลเกม apex ของคนๆนั้น",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="คําสั่งเกี่ยวกับเกม",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}coinflip``", value="flip a coin"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rps``",
                    value="play rock paper scissor",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}roll``", value="roll a dice"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}8ball [question] ``",
                    value="plau 8ball",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}csgonow``",
                    value="People playing CSGO at this time",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}apexnow``",
                    value="People playing Apex at this time",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}rb6now``",
                    value="People playing RB6 at this time",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pubgnow``",
                    value="People playing PUBG at this time",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gtanow``",
                    value="People playing gtanow at this time",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}apexstat [user]``",
                    value="see a user apex in-game stat",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpinfo(self, ctx):
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
                    title="คําสั่งเกี่ยวกับข้อมูล",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}serverinfo``",
                    value="ข้อมูลเกี่ยวกับเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}membercount``",
                    value="จํานวนสมาชิกในเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}userinfo [@member]``",
                    value="ข้อมูลเกี่ยวกับสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}covid19th``",
                    value="ข้อมูลเกี่ยวกับcovid19 ในไทย",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}covid19``",
                    value="ข้อมูลเกี่ยวกับcovid19ทั่วโลก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}geoip [ip]``",
                    value="ข้อมูลเกี่ยว IP นั้น",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}weather [city]``",
                    value="ดูสภาพอากาศของจังหวัด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}country [country]``",
                    value="ดูข้อมูลของประเทศ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}btc``",
                    value="ข้อมูลเกี่ยวกับราคา Bitcoin",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}eth``",
                    value="ข้อมูลเกี่ยวกับราคา Ethereum ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}github [username]``",
                    value="ดูข้อมูลในของคนใน Github",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}avatar [@member]``",
                    value="ดูรูปโปรไฟล์ของสมาชิก และ ตัวเอง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}searchavatar [@member]``",
                    value="search หารูปโปรไฟล์ของสมาชิก และ ตัวเอง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}guildicon``",
                    value="ดูรูปโปรไฟล์ของเซิฟเวอร์",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gethttp``",
                    value="ค้นหา proxy HTTP",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gethttps``",
                    value="ค้นหา proxy HTTPS",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getproxy``", value="ค้นหา proxy"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getsock4``",
                    value="ค้นหา proxy Sock4",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getsock5``",
                    value="ค้นหา proxy Sock5",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="help commands related to information",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}serverinfo``",
                    value="info about your server",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}membercount``",
                    value="Number of members in the server",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}userinfo [@member]``",
                    value="info about member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}covid19th``",
                    value="Thailand COVID-19 status",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}covid19``",
                    value="Covid-19 around the world",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}geoip [ip]``",
                    value="Info about the ip address",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}weather [city]``",
                    value="display weather of a city",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}country [country]``",
                    value="see info of a country",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}btc``", value="Bitcoin prices"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}eth``", value="Ethereum prices"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}github [username]``",
                    value="info of Github user",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}avatar [@member]``",
                    value="View your profile picture or a member profile picture",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}searchavatar [@member]``",
                    value="search your profile picture or a member profile picture",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}guildicon``",
                    value="View server icon",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gethttp``",
                    value="search for proxy HTTP",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gethttps``",
                    value="search for proxy HTTPS",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getproxy``",
                    value="search for proxy",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getsock4``",
                    value="search for proxy Sock4",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}getsock5``",
                    value="search for proxy Sock5",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpadmin(self, ctx):
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
                    title="คําสั่งเกี่ยวเเอดมิน",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}kick [@member]``",
                    value="เเตะสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ban [@member]``",
                    value="เเบนสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}unban [member#1111]``",
                    value="ปลดเเบนสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}giverole [@member] [@role]``",
                    value="ให้ยศกับสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}removerole [@member] [@role]``",
                    value="เอายศของสมาชิกออก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}roleall [@role]``",
                    value="ให้ยศกับสมาชิกทุกคนที่สามารถให้ได้",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}removeroleall [@role]``",
                    value="ลบยศกับสมาชิกทุกคน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}changenick [@member] [newnick]``",
                    value="เปลี่ยนชื่อของสมาชิก",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}clear [จํานวน] ``",
                    value="เคลียข้อความตามจํานวน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}movetome [@member]``",
                    value="ย้ายสมาชิกมาห้องของเรา",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="คําสั่งเกี่ยวเเอดมิน",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}kick [@member]``",
                    value="ban a member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ban [@member]``",
                    value="kick a member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}unban [member#1111]``",
                    value="unban a member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}giverole [@member] [@role]``",
                    value="give role to member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}removerole [@member] [@role]``",
                    value="remove role from member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}roleall [@role]``",
                    value="give role to all member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}removeroleall [@role]``",
                    value="remove role to all member",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}changenick [@member] [newnick]``",
                    value="change member nickname",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}clear [จํานวน] ``",
                    value="clear messages",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}movetome [@member]``",
                    value="move a member to your voice chat",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpfun(self, ctx):
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
                    title="คําสั่งบรรเทิง",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}anon [message]``",
                    value=f"พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {settings.COMMAND_PREFIX}helpsetup",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}sreddit [subreddit]``",
                    value="ส่งรูปจาก subreddit",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}meme``", value="ส่งมีม"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ascii [message]``",
                    value="เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}tweet [username] [message]``",
                    value="สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}phcomment [text]``",
                    value="สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}wasted [@member]``",
                    value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง',
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gay [@member]``",
                    value="ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}trigger [@member]``",
                    value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง',
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}slim``",
                    value="สุ่มส่งคําพูดของสลิ่ม",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}youtube [ชื่อคลิป]``",
                    value="ดูข้อมูลของคลิปใน YouTube",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ytsearch [keyword]``",
                    value="ค้นหาคลิปใน YouTube",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}captcha [text]``",
                    value="ทํา captcha จากคําที่ใส่",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}love [@member]``",
                    value="ดู % ความรักของตัวเองกับเพื่อนในเซิร์ฟเวอร์หากไม่ @เพื่อนระบบจะสุ่มให้",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="คําสั่งบรรเทิง",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}anon [message]``",
                    value=f"พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {settings.COMMAND_PREFIX}helpsetup",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}sreddit [subreddit]``",
                    value="ส่งรูปจาก subreddit",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}meme``", value="ส่งมีม"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ascii [message]``",
                    value="เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}tweet [username] [message]``",
                    value="สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}phcomment [text]``",
                    value="สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}wasted [@member]``",
                    value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง',
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}gay [@member]``",
                    value="ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}trigger [@member]``",
                    value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง',
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}slim``",
                    value="สุ่มส่งคําพูดของสลิ่ม",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}youtube [ชื่อคลิป]``",
                    value="ดูข้อมูลของคลิปใน YouTube",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}ytsearch [keyword]``",
                    value="ค้นหาคลิปใน YouTube",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}captcha [text]``",
                    value="ทํา captcha จากคําที่ใส่",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}love [@member]``",
                    value="ดู % ความรักของตัวเองกับเพื่อนในเซิร์ฟเวอร์หากไม่ @เพื่อนระบบจะสุ่มให้",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpgeneral(self, ctx):
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
                    title="คําสั่งทั่วไป",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}qr [message]``",
                    value="สร้าง qr code",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}hastebin [message]``",
                    value="สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pastebin [message]``",
                    value="สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}lmgtfy [message]``",
                    value="สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}timer [second]``",
                    value="นาฬิกานับถอยหลัง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}count [second``",
                    value="นาฬิกานับเวลา",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}upper [message]``",
                    value="เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}lower [message]``",
                    value="เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}enbinary [message]``",
                    value="เเปลคําพูดเป็น binary (0101)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}debinary [binnary]``",
                    value="เเปลbinary เป็นคําพูด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}calculator [equation]``",
                    value="คํานวนคณิตศาสตร์ + - * / ^ ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}say [message]``",
                    value="ส่งข้อความผ่านบอท (ใส่//เพื่อเริ่มบรรทัดต่อไป)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}embed [message]``",
                    value="สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}length [text]``",
                    value="นับจำนวนตัวอักษร",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}reverse [message]``",
                    value="กลับหลังประโยค",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="คําสั่งทั่วไป",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}qr [message]``",
                    value="สร้าง qr code",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}hastebin [message]``",
                    value="สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}pastebin [message]``",
                    value="สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}lmgtfy [message]``",
                    value="สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}timer [second]``",
                    value="นาฬิกานับถอยหลัง",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}count [second]``",
                    value="นาฬิกานับเวลา",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}upper [message]``",
                    value="เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}lower [message]``",
                    value="เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}enbinary [message]``",
                    value="เเปลคําพูดเป็น binary (0101)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}debinary [binnary]``",
                    value="เเปลbinary เป็นคําพูด",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}calculator [equation]``",
                    value="คํานวนคณิตศาสตร์ + - * / ^ ",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}say [message]``",
                    value="ส่งข้อความผ่านบอท (ใส่//เพื่อเริ่มบรรทัดต่อไป)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}embed [message]``",
                    value="สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}length [text]``",
                    value="นับจำนวนตัวอักษร",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}reverse [message]``",
                    value="กลับหลังประโยค",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpimage(self, ctx):
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
                    title="คําสั่งเกี่ยวกับรูป",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}bird``", value="ส่งภาพนก"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}panda``", value="ส่งภาพเเพนด้า"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}cat``", value="ส่งภาพเเมว"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}dog``", value="ส่งภาพหมา"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}fox``", value="ส่งภาพสุนัขจิ้งจอก"
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}koala``", value="ส่งภาพหมีโคอาล่า"
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":
                embed = nextcord.Embed(
                    title="คําสั่งเกี่ยวกับรูป",
                    description=f"{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}bird``",
                    value="Send a picture of a bird",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}panda``",
                    value="Send a picture of a panda",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}cat``",
                    value="Send a picture of a cat",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}dog``",
                    value="Send a picture of a dog",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}fox``",
                    value="Send a picture of a fox",
                )
                embed.add_field(
                    name=f"``{settings.COMMAND_PREFIX}koala``",
                    value="Send a picture of a koala",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpnsfw(self, ctx):
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
                    title="คําสั่งnsfw",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"""

    **18+**""",
                    value=f"""```
{settings.COMMAND_PREFIX}porn
{settings.COMMAND_PREFIX}gsolo
{settings.COMMAND_PREFIX}classic
{settings.COMMAND_PREFIX}pussy
{settings.COMMAND_PREFIX}eroyuri
{settings.COMMAND_PREFIX}yuri
{settings.COMMAND_PREFIX}solo
{settings.COMMAND_PREFIX}anal
{settings.COMMAND_PREFIX}erofeet
{settings.COMMAND_PREFIX}feet
{settings.COMMAND_PREFIX}hentai
{settings.COMMAND_PREFIX}boobs
{settings.COMMAND_PREFIX}tits
{settings.COMMAND_PREFIX}blowjob
{settings.COMMAND_PREFIX}lewd
{settings.COMMAND_PREFIX}lesbian```""",
                )
                embed.add_field(
                    name=f"""

    **Not 18+**""",
                    value=f"""```
{settings.COMMAND_PREFIX}feed
{settings.COMMAND_PREFIX}tickle 
{settings.COMMAND_PREFIX}slap
{settings.COMMAND_PREFIX}hug
{settings.COMMAND_PREFIX}smug
{settings.COMMAND_PREFIX}pat
{settings.COMMAND_PREFIX}kiss```
""",
                )
                embed.add_field(
                    name="📢หมายเหตุ",
                    value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

            if server_language == "English":

                embed = nextcord.Embed(
                    title="NSFW commands",
                    description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``",
                    color=0xFED000,
                )
                embed.add_field(
                    name=f"""

    **18+**""",
                    value=f"""
{settings.COMMAND_PREFIX}porn
{settings.COMMAND_PREFIX}gsolo
{settings.COMMAND_PREFIX}classic
{settings.COMMAND_PREFIX}pussy
{settings.COMMAND_PREFIX}eroyuri
{settings.COMMAND_PREFIX}yuri
{settings.COMMAND_PREFIX}solo
{settings.COMMAND_PREFIX}anal
{settings.COMMAND_PREFIX}erofeet
{settings.COMMAND_PREFIX}feet
{settings.COMMAND_PREFIX}hentai
{settings.COMMAND_PREFIX}boobs
{settings.COMMAND_PREFIX}tits
{settings.COMMAND_PREFIX}blowjob
{settings.COMMAND_PREFIX}lewd
{settings.COMMAND_PREFIX}lesbian""",
                )
                embed.add_field(
                    name=f"""

    **Not 18+**""",
                    value=f"""
{settings.COMMAND_PREFIX}feed
{settings.COMMAND_PREFIX}tickle 
{settings.COMMAND_PREFIX}slap
{settings.COMMAND_PREFIX}hug
{settings.COMMAND_PREFIX}smug
{settings.COMMAND_PREFIX}pat
{settings.COMMAND_PREFIX}kiss
""",
                )
                embed.add_field(
                    name="📢Note",
                    value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                    inline=False,
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("👍")

    @commands.command()
    async def helpscam(self, ctx):
        await ctx.invoke(self.bot.get_command("scam"))

    @commands.command()
    async def helptictactoe(self, ctx):
        await ctx.invoke(self.bot.get_command("tictactoe"))


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
