import aiohttp 
import discord 
import settings 
import humanize 
import datetime 
import bs4
from bs4 import BeautifulSoup
from discord.ext import commands

class GameInfo(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        
    @commands.command()
    async def dota2now(self,ctx):
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
                url = "https://steamcharts.com/app/570"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น dota2 ในตอนนี้",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg?t=1608587587")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')
            
            if server_language == "English":
                url = "https://steamcharts.com/app/570"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น dota2 ในตอนนี้",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg?t=1608587587")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def csgonow(self,ctx):
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
                url = "https://steamcharts.com/app/730"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น CS:GO",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg?t=1607046958")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

            if server_language == "English":
                url = "https://steamcharts.com/app/730"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น CS:GO",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg?t=1607046958")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def pubgnow(self,ctx):
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
                url = "https://steamcharts.com/app/578080"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น PUBG ในตอนนี้",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/578080/header.jpg?t=1608093288")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')
            
            if server_language == "English":
                url = "https://steamcharts.com/app/578080"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น PUBG ในตอนนี้",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/578080/header.jpg?t=1608093288")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def rb6now(self,ctx):
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
                url = "https://steamcharts.com/app/359550"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น RB6 ในตอนนี้",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/359550/header.jpg?t=1606776740")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

            if server_language == "English":
                url = "https://steamcharts.com/app/359550"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น RB6 ในตอนนี้",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/359550/header.jpg?t=1606776740")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def apexnow(self,ctx):
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
                url = "https://steamcharts.com/app/1172470"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น APEX LEGEND ในตอนนี้",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/1172470/header.jpg?t=1609705061")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

            if server_language == "English":
                url = "https://steamcharts.com/app/1172470"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น APEX LEGEND ในตอนนี้",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/1172470/header.jpg?t=1609705061")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def gtanow(self,ctx):
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
                url = "https://steamcharts.com/app/271590"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น GTAV ในตอนนี้",
                            description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1592866696")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

            if server_language == "Thai":
                url = "https://steamcharts.com/app/271590"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        div = soupObject.find_all('div', class_='app-stat')[0]
                        div1 = soupObject.find_all('div', class_='app-stat')[1]
                        div2 = soupObject.find_all('div', class_='app-stat')[2]

                        online = div.contents[1].string
                        online24 = div1.contents[1].string
                        onlineall = div2.contents[1].string
                        player = humanize.intcomma(online)
                        player24 = humanize.intcomma(online24)
                        playerall = humanize.intcomma(onlineall)

                        embed = discord.Embed(
                            color=0x75ff9f,
                            title = "จํานวนคนที่เล่น GTAV ในตอนนี้",
                            description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                        embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1592866696")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

    @commands.command()
    async def apexstat(self,ctx, username):
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
            headers = {
                'TRN-Api-Key': settings.trackerapi
            }
            server_language = languageserver["Language"]

            url = f"https://public-api.tracker.gg/v2/apex/standard/profile/origin/{username}"
            async with aiohttp.ClientSession(headers = headers) as session:
                async with session.get(url) as r:
                    r = await r.json()

                if server_language == "Thai":
                    if not r["errors"]:
                        platform = r["data"]["platformInfo"]["platformSlug"]
                        username = r["data"]["platformInfo"]["platformUserId"]
                        avatar = r["data"]["platformInfo"]["avatarUrl"]
                        level = r["data"]["segments"][0]["stats"]["level"]["value"]
                        kills = r["data"]["segments"][0]["stats"]["kills"]["value"]

                        level = int(level)
                        kills = int(kills)
                        kills = humanize.intcomma(kills)
                        embed= discord.Embed(
                            colour = 0x00FFFF,
                            title = f"🎮 Stat เกม apex legend ของ {username}",
                            description =f"""```
💻 เพลตฟอร์ม : {platform}
👀 ชื่อในเกม : {username}
📁 เลเวลในเกม : {level}
🔫 ฆ่าทั้งหมด : {kills}```
                        """)

                        embed.set_thumbnail(url=avatar)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` ไม่พบผู้เล่น ``{username}``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
            
                if server_language == "English":
                    if not r["errors"]:
                        platform = r["data"]["platformInfo"]["platformSlug"]
                        username = r["data"]["platformInfo"]["platformUserId"]
                        avatar = r["data"]["platformInfo"]["avatarUrl"]
                        level = r["data"]["segments"][0]["stats"]["level"]["value"]
                        kills = r["data"]["segments"][0]["stats"]["kills"]["value"]

                        level = int(level)
                        kills = int(kills)
                        kills = humanize.intcomma(kills)
                        embed= discord.Embed(
                            colour = 0x00FFFF,
                            title = f"🎮 apex legend stat of {username}",
                            description =f"""```
💻 Platform : {platform}
👀 Username : {username}
📁 Level : {level}
🔫 Kills : {kills}```
                """)

                        embed.set_thumbnail(url=avatar)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('🎮')

                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` Player not found ``{username}``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')

    @apexstat.error
    async def apexstat_error(self,ctx, error):
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
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมใส่ชื่อของผู้เล่น ``{settings.COMMAND_PREFIX}apexstat (username)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a username ``{settings.COMMAND_PREFIX}apexstat (username)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')


def setup(bot: commands.Bot):
    bot.add_cog(GameInfo(bot))