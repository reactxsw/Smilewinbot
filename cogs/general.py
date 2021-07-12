import discord
from discord.ext.commands.core import command
import settings
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from urllib.parse import urlencode

from discord.ext import commands

class General(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def lmgtfy(self, ctx, *, message):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            r = urlencode({"q": message})
            url = (f'<https://lmgtfy.com/?{r}>')

            if server_language == "Thai": 
                embed= discord.Embed(
                    colour =0x00FFFF,
                    title= f"ลิงค์ lmgtfy ของคุณ {ctx.author}",
                    description = f"{url}"
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
            
            if server_language == "English": 
                embed= discord.Embed(
                    colour =0x00FFFF,
                    title= f"lmgtfy link for {ctx.author}",
                    description = f"{url}"
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')
        
    @lmgtfy.error
    async def lmgtfy_error(self, ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหาใน lmgtfy ``{settings.COMMAND_PREFIX}lmgtfy [message]``"
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` need to specify what to search on lmgtfy ``{settings.COMMAND_PREFIX}lmgtfy [message]``"
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def timer(self,ctx, second : int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":

                number = second
                embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับถอยหลัง {second} วินาที",
                        description = f"{number}"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                while number >= 0:
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับถอยหลัง {second} วินาที",
                        description = f"```{number}```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    number = number - 1 
                    await asyncio.sleep(1)
                    await message.edit(embed=embed)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับถอยหลัง {second} วินาที",
                    description = "เสร็จ"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await message.edit(embed=embed)
            
            if server_language == "Thai":

                number = second
                embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ countdown for {second} second",
                        description = f"{number}"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                while number >= 0:
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ countdown for {second} second",
                        description = f"```{number}```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    number = number - 1 
                    await asyncio.sleep(1)
                    await message.edit(embed=embed)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ countdown for {second} second",
                    description = "Finished"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await message.edit(embed=embed)

    @timer.error
    async def timer_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับถอยหลัง ``{settings.COMMAND_PREFIX}timer (second)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify how long to countdown ``{settings.COMMAND_PREFIX}timer (second)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def count(self,ctx, second : int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                number = 0
                embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับเลขถึง {second} วินาที",
                        description = f"{number}"
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                while number <= second:
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับเลขถึง {second} วินาที",
                        description = f"```{number}```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    number = number + 1 
                    await asyncio.sleep(1)
                    await message.edit(embed=embed)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = "เสร็จ"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await message.edit(embed=embed)
            
            if server_language == "English":
                number = 0
                embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับเลขถึง {second} วินาที",
                        description = f"{number}"
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                while number <= second:
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"⏱️ นับเลขถึง {second} วินาที",
                        description = f"```{number}```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    number = number + 1 
                    await asyncio.sleep(1)
                    await message.edit(embed=embed)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = "เสร็จ"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await message.edit(embed=embed)

    @count.error
    async def count_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับ ``{settings.COMMAND_PREFIX}count (second)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify how long to coun ``{settings.COMMAND_PREFIX}count (second)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def upper(self,ctx, *, message):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                big = message.upper()
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "UPPERCASE GENERATOR",
                    description = f"""```
ข้อความปกติ : {message}
ข้อความตัวพิมพ์ใหญ่ : {big}```"""

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)
            
            if server_language == "English":
                big = message.upper()
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "UPPERCASE GENERATOR",
                    description = f"""```
Normal text : {message}
Uppercase text : {big}```"""

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @upper.error
    async def upper_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมใหญ่ ``{settings.COMMAND_PREFIX}upper (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what to make into uppercase ``{settings.COMMAND_PREFIX}upper (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def lower(self,ctx, *, message):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                lower = message.lower()
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "LOWERCASE GENERATOR",
                    description = f"""```
ข้อความปกติ : {message}
ข้อความตัวพิมพ์ใหญ่ : {lower}```"""

            )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)
            
            if server_language == "English":
                lower = message.lower()
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "LOWERCASE GENERATOR",
                    description = f"""```
Normal text : {message}
Lowercase text : {lower}```"""

            )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @lower.error
    async def lower_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมเล็ก ``{settings.COMMAND_PREFIX}lower (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what to make into lowercase ``{settings.COMMAND_PREFIX}lower (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def reverse(self,ctx, *, message):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":

                reverse = message[::-1]
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "REVERSE GENERATOR",
                    description = f"""```
ข้อความปกติ : {message}
ข้อความกลับหลัง : {reverse}```"""
            )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)
            
            if server_language == "English":

                reverse = message[::-1]
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "REVERSE GENERATOR",
                    description = f"""```
Normal text : {message}
Reverse text : {reverse}```"""
            )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @reverse.error
    async def reverse_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะกลับด้าน ``{settings.COMMAND_PREFIX}reverse (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what to reverse ``{settings.COMMAND_PREFIX}reverse (message)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def enbinary(self,ctx, *, text): 
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/binary?text={text}") as r:
                        r = await r.json()

                binary = r['binary']

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "Encode Binary",
                    description = f"""```
คําปกติ : {text}
Binary : {binary}```"""
                )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💻')
            
            if server_language == "English":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/binary?text={text}") as r:
                        r = await r.json()

                binary = r['binary']

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "Encode Binary",
                    description = f"""```
Normal text : {text}
Binary : {binary}```"""
                )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💻')

    @commands.command()
    async def debinary(self,ctx, *,text): 
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/binary?decode={text}") as r:
                        r = await r.json()

                binary = r['text']

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "Encode Binary",
                    description = f"""```
Binary : {text}
Normal text : {binary}```"""
                )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💻')
            
            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://some-random-api.ml/binary?decode={text}") as r:
                        r = await r.json()

                binary = r['text']

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "Encode Binary",
                    description = f"""```
Binary : {text}
Normal text : {binary}```"""
                )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💻')

    @commands.command()
    async def length(self,ctx, *, text):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            num = len(text)
            if server_language == "Thai": 
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "LENGTH COUNTER",
                    description = f"""```
ข้อความ : {text}
ความยาว : {num}```"""

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)
            
            if server_language == "English": 
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "LENGTH COUNTER",
                    description = f"""```
text : {text}
length : {num}```"""

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @length.error
    async def length_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะนับตัวอักษร ``{settings.COMMAND_PREFIX}length (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a text ``{settings.COMMAND_PREFIX}length (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def calculator(self,ctx , *,equation):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
            
                url = f"https://api.mathjs.org/v4/?expr={equation}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as req:
                        result = BeautifulSoup(await req.text(), "html.parser")

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "เครื่องคิดเลข",
                    description = f"""
    ```
    โจทย์ : {equation}
    คําตอบ : {result}
    ```""")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)
            
            if server_language == "English":
            
                url = f"https://api.mathjs.org/v4/?expr={equation}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as req:
                        result = BeautifulSoup(await req.text(), "html.parser")

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "Calculator",
                    description = f"""
    ```
    Equation : {equation}
    Answer : {result}
    ```""")
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

    @calculator.error
    async def calculator_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "ระบุสิ่งที่จะคําณวน",
                        description = f" ⚠️``{ctx.author}`` จะต้องระบุใส่สิ่งที่จะคําณวน ``{settings.COMMAND_PREFIX}calculator (equation)``"
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "Specify an equation",
                        description = f" ⚠️``{ctx.author}`` need to specify a math equation ``{settings.COMMAND_PREFIX}calculator (equation)``"
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

def setup(bot: commands.Bot):
    bot.add_cog(General(bot))