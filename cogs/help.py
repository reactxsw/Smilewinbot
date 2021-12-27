from os import name
import discord
import settings
from discord.ext import commands
from utils.languageembed import languageEmbed


class Help(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    async def help(self , ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คำสั่งสำหรับใช้งานบอท',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}help``',value='ช่วยเหลือคําสั่งช่วยเหลือ')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpbot``',value='ช่วยเหลือคําสั่งเกี่ยวกับตัวบอท')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpfun``',value='ช่วยเหลือคําสั่งบรรเทิง')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpgeneral``',value='ช่วยเหลือคําสั่งทั่วไป')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpgame``',value='ช่วยเหลือคําสั่งเกี่ยวกับเกม')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpadmin``',value='ช่วยเหลือคําสั่งของเเอดมิน')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpsetup``',value='ช่วยเหลือคําสั่งเกี่ยวกับตั้งค่า')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpinfo``',value='ช่วยเหลือคําสั่งเกี่ยวกับข้อมูล')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpimage``',value='ช่วยเหลือคําสั่งเกี่ยวกับรูป')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpeconomy``',value='ช่วยเหลือคําสั่งเกี่ยวกับระบบเศรษฐกิจ')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpuser``',value='ช่วยเหลือคําสั่งข้อมูลของสมาชิกเช่น เลเวล')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpnsfw``',value='ช่วยเหลือคําสั่ง 18 +')
                embed.add_field(name="📢หมายเหตุ",value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""")

                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='Help command',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}help``',value='help commands')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpbot``',value='help commands related to bot')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpfun``',value='help commands related to fun')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpgeneral``',value='help general commands')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpgame``',value='help commands related to game')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpadmin``',value='help commands related to moderator')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpsetup``',value='help commands related to setup')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpinfo``',value='help commands related to information')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpimage``',value='help commands related to image')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpeconomy``',value='help commands related to economy')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpuser``',value='help commands related to user')
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}helpnsfw``',value='help commands related to NSFW')
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpeconomy(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งต่างๆเกี่ยวกับระบบเศรษฐกิจ',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}openbal``', value = 'เปิดบัญชีธนาคาร',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}bal [@member]``', value='ดูเงินของคุณหรือของสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}deposit [amount]``', value ='ฝากเงินเข้าธนาคาร', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}withdraw [amount]``', value = 'ถอนเงินจากธนาคาร',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pay [@member]``', value ='โอนเงินจากธนาคารให้สชาชิกในเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}slot [amount]``', value ='เล่นพนัน slot', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rob [@member]``', value ='ขโมยเงินจากสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}addcredit [amount] [@member]``', value ='เพิ่มตังให้สมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}resetmoney [@member]``', value ='รีเซ็ทเงินของสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}work``', value ='ทํางานหาเงิน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}beg``', value ='ขอทาน', inline = True)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='Instructions for use economy command',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}openbal``', value = 'Open a new balance',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}bal [@member]``', value='Check your balance', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}deposit [amount]``', value ='Deposit money to the bank', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}withdraw [amount]``', value = 'Withdraw money from the bank',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pay [@member]``', value ='Pay money to user in the server', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}slot [amount]``', value ='Slot machine', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rob [@member]``', value ='steal money', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}addcredit [amount] [@member]``', value ='add money to user', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}resetmoney [@member]``', value ='reset a member balance', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}work``', value ='work to earn money', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}beg``', value ='beg for money', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpbot(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับตัวบอท',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}test``', value = 'ดูว่าบอทonline ไหม',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ping``', value='ส่ง ping ของบอท', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}uptime``', value ='ส่ง เวลาทำงานของบอท', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botinvite``', value = 'ส่งลิงค์เชิญบอท',inline = True )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botvote``', value = 'โหวตให้บอท',inline = True )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}credit``',value='เครดิตคนทําบอท',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botinfo``', value = 'ข้อมูลเกี่ยวกับตัวบอท',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}support [text]``', value = 'ส่งข้อความหา support หากพบปัญหา',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='help commands related to bot',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}test``', value = 'test command to see if the bot is online',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ping``', value='send bot ping', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}uptime``', value ='send bot uptime', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botinvite``', value = 'send bot invite link',inline = True )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botvote``', value = 'Vote for bot',inline = True )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}credit``',value='developer credit',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}botinfo``', value = 'information about bot',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}support [text]``', value = 'send support if error occur',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpuser(self , ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งข้อมูลของสมาชิก',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rank <@member>``', value = 'เช็คเเรงค์ของคุณหรือสมาชิก',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}leaderboard``', value='ดูอันดับเลเวลของคุณในเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ind``', value='เเนะนําตัว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}vfy``', value='ยืนยันตัวตนโดย captcha', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='help commands related to user',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rank <@member>``', value = 'see your level or member level in the server',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}leaderboard``', value='level leaderboard', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ind``', value='Introduce yourself', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}vfy``', value='captcha verification', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpsetup(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับตั้งค่า',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setting``', value ='ดูการตั้งค่าของเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setup``', value ='ลงทะเบียนเซิฟเวอร์ในฐานข้อมูล', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setwelcome [#text-channel]``', value='ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setleave [#text-channel]``', value ='ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setwebhook [#text-channel]``', value =f'ตั้งค่าห้องที่จะใช้คําสั่ง {settings.COMMAND_PREFIX}anon (message) เพื่อคุยกับคนเเปลกหน้าโดยที่ไม่เปิดเผยตัวตนกับเซิฟเวอร์ที่เปิดใช้คําสั่งนี้', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setintroduce [#text-channel]``', value =f'ตั้งค่าห้องที่จะให้ส่งข้อมูลของสมาชิกหลังจากเเนะนําตัวเสร็จ *พิม {settings.COMMAND_PREFIX}ind เพื่อเเนะนําตัว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setframe``', value ='ตั้งกรอบที่ใส่ข้อมูลของสมาชิกจากปกติเป็น ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setrole give/remove [@role]``', value =f'ตั้งค่าที่จะ ให้/ลบหลังจากเเนะนําตัว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setverify [#text-channel]``', value =f'ตั้งค่าห้องยืนยันตัวตน (captcha) *พิม {settings.COMMAND_PREFIX}vfy เพื่องยืนยันตัวตน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}verifyrole give/remove [@role]``', value =f'ตั้งค่าที่จะ ให้/ลบหลังจากยืนยันตัวตน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}verifytime [time]``', value =f'ตั้งค่าเวลาในการยืนยันตัวตน (ห้ามเกิน 120 วินาที)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}verification on/off``', value =f'ตั้งค่าที่จะ ให้/ลบหลังจากยืนยันตัวตน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}chat on/off``', value ='เปิด / ปิดใช้งานห้องคุยกับคนเเปลกหน้า', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}level on/off``', value ='เปิด / ปิดใช้งานระบบเลเวล', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}introduce on/off``', value ='เปิด / ปิดการใช้งานคําสั่งเเนะนําตัว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}economy on/off``', value ='เปิด / ปิดการใช้งานระบบเศรษฐกิจ', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}logvoice on/off``', value ='เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setlog [#text-channel]``', value ='เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setserverstat``', value ='เปิดใช้งานระบบโชว์สถิตืเซิฟเวอร์', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='help commands related to setup',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setting``', value ='see server setting', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setup``', value ='set up your server to our database', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}welcomeset [#text-channel]``', value='set up a channel to notify if new member join', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}leaveset [#text-channel]``', value ='set up a channel to notify if member left', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setwebhook [#text-channel]``', value =f'setup room to talk to a stranger and use {settings.COMMAND_PREFIX}anon (message) to talk to stranger', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setintroduce [#text-channel]``', value =f'setup a room for member to introduce themself and use {settings.COMMAND_PREFIX}ind to introduce', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setrole give/remove [@role]``', value =f'setup a role to give/remove after a member finish introducing himself/herself', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setframe``', value ='set the frame around member information after they introduce themself, Normal frame: ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}chat on/off``', value ='turn on/off ability to talk to a stranger', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}level on/off``', value ='turn on/off level system', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}introduce on/off``', value ='turn on/off introduce command', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}economy on/off``', value ='turn on/off an economy system', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}verification on/off``', value ='turn on/off an verification system', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}logvoice on/off``', value ='เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setlog [#text-channel]``', value ='เปิด / ปิดการใช้งานระบบเเจ้งเตือนการเข้าห้องเสียง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}setserverstat``', value ='เปิดใช้งานระบบโชว์สถิตืเซิฟเวอร์', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpgame(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับเกม',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}coinflip``', value='ทอยเหรียญ', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rps``', value = 'เป่ายิ้งฉับเเข่งกับบอท',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}roll``', value='ทอยลูกเต๋า', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}8ball [question] ``', value='ดูว่าควรจะทําสิงๆนั้นไหม', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}csgonow``', value = 'จํานวนคนที่เล่น CSGO ขณะนี้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}apexnow``', value = 'จํานวนคนที่เล่น APEX ขณะนี้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rb6now``', value = 'จํานวนคนที่เล่น RB6 ขณะนี้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pubgnow``', value = 'จํานวนคนที่เล่น PUBG ขณะนี้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gtanow``', value = 'จํานวนคนที่เล่น GTA V ขณะนี้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}apexstat [username]``', value = 'ดูข้อมูลเกม apex ของคนๆนั้น',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับเกม',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}coinflip``', value='flip a coin', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rps``', value = 'play rock paper scissor',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}roll``', value='roll a dice', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}8ball [question] ``', value='plau 8ball', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}csgonow``', value = 'People playing CSGO at this time',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}apexnow``', value = 'People playing Apex at this time',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}rb6now``', value = 'People playing RB6 at this time',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pubgnow``', value = 'People playing PUBG at this time',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gtanow``', value = 'People playing gtanow at this time',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}apexstat [user]``', value = 'see a user apex in-game stat',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpinfo(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับข้อมูล',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}serverinfo``', value='ข้อมูลเกี่ยวกับเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}membercount``', value='จํานวนสมาชิกในเซิฟเวอร์', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}userinfo [@member]``', value ='ข้อมูลเกี่ยวกับสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}covid19th``', value = 'ข้อมูลเกี่ยวกับcovid19 ในไทย',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}covid19``', value = 'ข้อมูลเกี่ยวกับcovid19ทั่วโลก',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}geoip [ip]``', value = 'ข้อมูลเกี่ยว IP นั้น',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}weather [city]``', value = 'ดูสภาพอากาศของจังหวัด',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}country [country]``', value = 'ดูข้อมูลของประเทศ',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}btc``',value='ข้อมูลเกี่ยวกับราคา Bitcoin',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}eth``',value='ข้อมูลเกี่ยวกับราคา Ethereum ',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}github [username]``',value='ดูข้อมูลในของคนใน Github',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}avatar [@member]``',value='ดูรูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}searchavatar [@member]``',value='search หารูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}guildicon``',value='ดูรูปโปรไฟล์ของเซิฟเวอร์',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gethttp``',value='ค้นหา proxy HTTP',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gethttps``',value='ค้นหา proxy HTTPS',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getproxy``',value='ค้นหา proxy',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getsock4``',value='ค้นหา proxy Sock4',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getsock5``',value='ค้นหา proxy Sock5',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='help commands related to information',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}serverinfo``', value='info about your server', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}membercount``', value='Number of members in the server', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}userinfo [@member]``', value ='info about member', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}covid19th``', value = 'Thailand COVID-19 status',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}covid19``', value = 'Covid-19 around the world',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}geoip [ip]``', value = 'Info about the ip address',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}weather [city]``', value = 'display weather of a city',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}country [country]``', value = 'see info of a country',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}btc``',value='Bitcoin prices',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}eth``',value='Ethereum prices',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}github [username]``',value='info of Github user',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}avatar [@member]``',value='View your profile picture or a member profile picture',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}searchavatar [@member]``',value='search your profile picture or a member profile picture',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}guildicon``',value='View server icon',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gethttp``',value='search for proxy HTTP',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gethttps``',value='search for proxy HTTPS',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getproxy``',value='search for proxy',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getsock4``',value='search for proxy Sock4',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}getsock5``',value='search for proxy Sock5',inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpadmin(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวเเอดมิน',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}kick [@member]``', value='เเตะสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ban [@member]``', value ='เเบนสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}unban [member#1111]``', value ='ปลดเเบนสมาชิก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}giverole [@member] [@role]``', value = 'ให้ยศกับสมาชิก',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}removerole [@member] [@role]``', value = 'เอายศของสมาชิกออก',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}roleall [@role]``', value = 'ให้ยศกับสมาชิกทุกคนที่สามารถให้ได้',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}removeroleall [@role]``', value = 'ลบยศกับสมาชิกทุกคน',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}changenick [@member] [newnick]``', value = 'เปลี่ยนชื่อของสมาชิก',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}clear [จํานวน] ``', value = 'เคลียข้อความตามจํานวน',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}disconnect [@member]``' ,value = 'disconnect สมาชิกที่อยู่ในห้องพูด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}movetome [@member]``' ,value = 'ย้ายสมาชิกมาห้องของเรา', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวเเอดมิน',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}kick [@member]``', value='ban a member', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ban [@member]``', value ='kick a member', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}unban [member#1111]``', value ='unban a member', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}giverole [@member] [@role]``', value = 'give role to member',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}removerole [@member] [@role]``', value = 'remove role from member',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}roleall [@role]``', value = 'give role to all member',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}removeroleall [@role]``', value = 'remove role to all member',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}changenick [@member] [newnick]``', value = 'change member nickname',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}clear [จํานวน] ``', value = 'clear messages',inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}disconnect [@member]``' ,value = 'disconnect a member', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}movetome [@member]``' ,value = 'move a member to your voice chat', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpfun(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งบรรเทิง',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}anon [message]``', value=f'พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {settings.COMMAND_PREFIX}helpsetup', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}sreddit [subreddit]``', value='ส่งรูปจาก subreddit', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}meme``', value='ส่งมีม', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ascii [message]``', value='เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}tweet [username] [message]``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}phcomment [text]``', value='สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}wasted [@member]``', value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gay [@member]``', value='ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}trigger [@member]``', value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}slim``', value='สุ่มส่งคําพูดของสลิ่ม', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}youtube [ชื่อคลิป]``', value='ดูข้อมูลของคลิปใน YouTube', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ytsearch [keyword]``', value='ค้นหาคลิปใน YouTube', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}captcha [text]``', value='ทํา captcha จากคําที่ใส่', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}love [@member]``', value='ดู % ความรักของตัวเองกับเพื่อนในเซิร์ฟเวอร์หากไม่ @เพื่อนระบบจะสุ่มให้', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='คําสั่งบรรเทิง',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}anon [message]``', value=f'พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {settings.COMMAND_PREFIX}helpsetup', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}sreddit [subreddit]``', value='ส่งรูปจาก subreddit', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}meme``', value='ส่งมีม', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ascii [message]``', value='เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}tweet [username] [message]``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}phcomment [text]``', value='สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}wasted [@member]``', value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}gay [@member]``', value='ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}trigger [@member]``', value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}slim``', value='สุ่มส่งคําพูดของสลิ่ม', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}youtube [ชื่อคลิป]``', value='ดูข้อมูลของคลิปใน YouTube', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}ytsearch [keyword]``', value='ค้นหาคลิปใน YouTube', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}captcha [text]``', value='ทํา captcha จากคําที่ใส่', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}love [@member]``', value='ดู % ความรักของตัวเองกับเพื่อนในเซิร์ฟเวอร์หากไม่ @เพื่อนระบบจะสุ่มให้', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpgeneral(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งทั่วไป',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}qr [message]``', value='สร้าง qr code', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}hastebin [message]``', value='สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pastebin [message]``', value='สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}lmgtfy [message]``', value= 'สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}timer [second]``', value= 'นาฬิกานับถอยหลัง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}count [second``', value= 'นาฬิกานับเวลา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}upper [message]``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}lower [message]``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}enbinary [message]``', value= 'เเปลคําพูดเป็น binary (0101)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}debinary [binnary]``', value= 'เเปลbinary เป็นคําพูด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}calculator [equation]``', value= 'คํานวนคณิตศาสตร์ + - * / ^ ', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}say [message]``', value= 'ส่งข้อความผ่านบอท (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}embed [message]``', value= 'สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}length [text]``', value= 'นับจำนวนตัวอักษร', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}reverse [message]``', value= 'กลับหลังประโยค', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='คําสั่งทั่วไป',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}qr [message]``', value='สร้าง qr code', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}hastebin [message]``', value='สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}pastebin [message]``', value='สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}lmgtfy [message]``', value= 'สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}timer [second]``', value= 'นาฬิกานับถอยหลัง', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}count [second]``', value= 'นาฬิกานับเวลา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}upper [message]``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}lower [message]``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}enbinary [message]``', value= 'เเปลคําพูดเป็น binary (0101)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}debinary [binnary]``', value= 'เเปลbinary เป็นคําพูด', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}calculator [equation]``', value= 'คํานวนคณิตศาสตร์ + - * / ^ ', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}say [message]``', value= 'ส่งข้อความผ่านบอท (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}embed [message]``', value= 'สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}length [text]``', value= 'นับจำนวนตัวอักษร', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}reverse [message]``', value= 'กลับหลังประโยค', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpimage(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับรูป',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}bird``', value='ส่งภาพนก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}panda``', value='ส่งภาพเเพนด้า', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}cat``', value= 'ส่งภาพเเมว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}dog``', value= 'ส่งภาพหมา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}fox``', value= 'ส่งภาพสุนัขจิ้งจอก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}koala``', value= 'ส่งภาพหมีโคอาล่า', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":
                embed=discord.Embed(
                    title='คําสั่งเกี่ยวกับรูป',
                    description=f'{ctx.author.mention} The command prefix is ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}bird``', value='ส่งภาพนก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}panda``', value='ส่งภาพเเพนด้า', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}cat``', value= 'ส่งภาพเเมว', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}dog``', value= 'ส่งภาพหมา', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}fox``', value= 'ส่งภาพสุนัขจิ้งจอก', inline = True)
                embed.add_field(name=f'``{settings.COMMAND_PREFIX}koala``', value= 'ส่งภาพหมีโคอาล่า', inline = True)
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

    @commands.command()
    async def helpnsfw(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":

                embed=discord.Embed(
                    title='คําสั่งnsfw',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f"""

    **18+**""",value=f"""```
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
{settings.COMMAND_PREFIX}lesbian```""",)
                embed.add_field(name=f"""

    **Not 18+**""",value=f"""```
{settings.COMMAND_PREFIX}feed
{settings.COMMAND_PREFIX}tickle 
{settings.COMMAND_PREFIX}slap
{settings.COMMAND_PREFIX}hug
{settings.COMMAND_PREFIX}smug
{settings.COMMAND_PREFIX}pat
{settings.COMMAND_PREFIX}kiss```
""")
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English":

                embed=discord.Embed(
                    title='NSFW commands',
                    description=f'{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``',
                    color=0xFED000   
                    )
                embed.add_field(name=f"""

    **18+**""",value=f"""
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
{settings.COMMAND_PREFIX}lesbian""",)
                embed.add_field(name=f"""

    **Not 18+**""",value=f"""
{settings.COMMAND_PREFIX}feed
{settings.COMMAND_PREFIX}tickle 
{settings.COMMAND_PREFIX}slap
{settings.COMMAND_PREFIX}hug
{settings.COMMAND_PREFIX}smug
{settings.COMMAND_PREFIX}pat
{settings.COMMAND_PREFIX}kiss
""")        
                embed.add_field(name="📢หมายเหตุ",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""")
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
