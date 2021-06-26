import discord
import aiohttp
import settings
from discord.ext import commands


class Proxy(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    async def gethttp(ctx):
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
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/http.txt", "w") as file:
                    file.write(r)
                file.close()
                f = discord.File("data/http.txt", filename="http.txt")
                await ctx.send(file = f)
            
            if server_language == "English":
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/http.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/http.txt", filename="http.txt")
                await ctx.send(file = file)

    @commands.command()
    async def gethttps(ctx):
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
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/https.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/https.txt", filename="https.txt")
                await ctx.send(file = file)
            
            if server_language == "English":
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/https.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/https.txt", filename="https.txt")
                await ctx.send(file = file)

    @commands.command()
    async def getproxy(ctx):
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
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/proxy.txt", "w") as file:
                    file.write(r)
                file.close()
                f = discord.File("data/proxy.txt", filename="proxy.txt")
                await ctx.send(file = f)
            
            if server_language == "English":
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/proxy.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/proxy.txt", filename="proxy.txt")
                await ctx.send(file = file)

    @commands.command()
    async def getsock4(ctx):
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
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/sock4.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/sock4.txt", filename="sock4.txt")
                await ctx.send(file = file)
            
            if server_language == "English":
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/sock4.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/sock4.txt", filename="sock4.txt")
                await ctx.send(file = file)

    @commands.command()
    async def getsock5(ctx):
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
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/sock5.txt", "w") as file:
                    file.write(r)
                file.close()
                f = discord.File("data/sock5.txt", filename="data/sock5.txt")
                await ctx.send(file = f)
            
            if server_language == "English":
                url = "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.text()
                with open("data/sock5.txt", "w") as file:
                    file.write(r)
                file.close()
                file = discord.File("data/sock5.txt", filename="data/sock5.txt")
                await ctx.send(file = file)

def setup(bot: commands.Bot):
    bot.add_cog(Proxy(bot))