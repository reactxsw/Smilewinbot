from discord import colour
from utils.languageembed import languageEmbed
import settings
import discord
import json
import aiohttp
import datetime
from bs4 import BeautifulSoup
import requests
import humanize
from discord.ext import commands
from googleapiclient.discovery import build


class Info(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command(aliases=['bitcoin'])
    async def btc(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,THB") as r:
                    r = await r.json()
                    usd = r['USD']
                    eur = r['EUR']
                    thb = r['THB']
                    embed = discord.Embed(
                        colour = 0xffff00,
                        title = "Bitcoin",
                        description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`\nTHB: `{str(thb)}฿`')
                    embed.set_author(name='Bitcoin', icon_url='https://i.imgur.com/3gVaQ4z.png')
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=embed)

    @commands.command(aliases=['ethereum'])
    async def eth(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,THB') as r:
                    r = await r.json()
                    usd = r['USD']
                    eur = r['EUR']
                    thb = r['THB']  
                    embed = discord.Embed(
                        colour = 0xffff00,
                        title = "Ethereum",
                        description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`\nTHB: `{str(thb)}฿`')
                    embed.set_author(name='Ethereum', icon_url='https://i.imgur.com/vsWBny2.png')
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()

                    await ctx.send(embed=embed)
    
    @commands.command()
    async def github(self,ctx, *, user=None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                url = f"https://api.github.com/users/{user}"
                if user is None:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อของGithubที่จะดู ``{settings.COMMAND_PREFIX}github (user)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.json()
                            
                    if not r["message"] == "Not Found":
                        username = r['login']
                        avatar =  r['avatar_url']
                        githuburl = r['html_url']
                        name = r['name']
                        location = r['location']
                        email = r['email']
                        company = r['company']
                        bio = r['bio']
                        repo = r['public_repos']

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = f"💻 ข้อมูล Github ของ {username}",
                            description = f"""```
ชื่อ Github : {username}
ลิงค์ Github : {githuburl}
ชื่อ : {name}
ที่อยู่ : {location}
อีเมล : {email}
บริษัท : {company}
Bio : {bio}
จํานวนงานที่ลง : {repo}```"""
            )
                        embed.set_thumbnail(url = avatar)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        
                        await message.add_reaction("💻")

                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️ไม่สามารถค้นหาชื่อของGithubได้โปรดเช็คตัวสะกด")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')

            if server_language == "English":
                url = f"https://api.github.com/users/{user}"
                if user is None:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a github username to search ``{settings.COMMAND_PREFIX}github (user)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as r:
                        r = await r.json()
                            
                    if not r["message"] == "Not Found":
                        username = r['login']
                        avatar =  r['avatar_url']
                        githuburl = r['html_url']
                        name = r['name']
                        location = r['location']
                        email = r['email']
                        company = r['company']
                        bio = r['bio']
                        repo = r['public_repos']

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = f"💻 ข้อมูล Github ของ {username}",
                            description = f"""```
Github username: {username}
Github link : {githuburl}
Name : {name}
Location : {location}
Email : {email}
Company : {company}
Bio : {bio}
Repository : {repo}```"""
                )
                        embed.set_thumbnail(url = avatar)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        
                        await message.add_reaction("💻")

                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️Unable to find the github profile please check your spelling")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')

    @github.error
    async def github_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อที่จะค้นหา ``{settings.COMMAND_PREFIX}github (username)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a username to search ``{settings.COMMAND_PREFIX}github (username)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command(aliases=['cv19th','covidthai','covid19thai'])
    async def covid19th(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            async with aiohttp.ClientSession() as session:
                async with session.get('https://covid19.th-stat.com/json/covid19v2/getTodayCases.json') as r:
                    r = await r.json()
                    newconfirm = r['NewConfirmed']
                    newdeath = r['NewDeaths']
                    recover = r['Recovered']
                    death = r['Deaths']
                    source = "https://covid19.th-stat.com/th"
                    update = r['UpdateDate']
                    confirm = r['Confirmed']
                    hospital = r['Hospitalized']
                    hospitalnew = r['NewHospitalized']

                    newconfirm = humanize.intcomma(newconfirm)
                    newdeath = humanize.intcomma(newdeath)
                    recover = humanize.intcomma(recover)
                    death = humanize.intcomma(death)
                    recover = humanize.intcomma(recover)
                    confirm = humanize.intcomma(confirm)
                    hospital = humanize.intcomma(hospital)
                    hospitalnew = humanize.intcomma(hospitalnew)

                    if server_language == "Thai":

                        embed = discord.Embed(
                            title="💊 ข้อมูล COVID-19 ประเทศไทย",
                            description=f"อัพเดตล่าลุดเมื่อ {update}",
                            color=0x00FFFF
                        )

                        embed.add_field(name='🤒 ผู้ป่วยสะสม',value=f"{confirm} คน")
                        embed.add_field(name='😷 ผู้ป่วยรายใหม่',value=f"{newconfirm} คน")
                        embed.add_field(name='🏠 ผู้ป่วยรักษาหายแล้ว',value=f"{recover} คน")
                        embed.add_field(name='🏠 ผู้ป่วยที่เข้าโรงพยาบาลทั้งหมด',value=f"{hospital} คน")
                        embed.add_field(name='🏠 ผู้ป่วยที่อยู่เข้าโรงพยาบาลใหม่',value=f"{hospitalnew} คน")
                        embed.add_field(name='☠️ ผู้ป่วยเสียชีวิตทั้งหมด',value=f"{death} คน")
                        embed.add_field(name='☠️ ผู้ป่วยเสียชีวิตใหม่',value=f"{newdeath} คน")
                        embed.set_footer(text=f'''ข้อมูลจาก {source}''')

                        message= await ctx.send(embed=embed)
                        await message.add_reaction('💊')
            
                    if server_language == "English":

                        embed = discord.Embed(
                            title="💊 Thailand COVID-19 status",
                            description=f"lastest update: {update}",
                            color=0x00FFFF
                        )

                        embed.add_field(name='🤒 Total confirm cases',value=f"{confirm} คน")
                        embed.add_field(name='😷 New cases',value=f"{newconfirm} คน")
                        embed.add_field(name='🏠 Total recover patients',value=f"{recover} คน")
                        embed.add_field(name='🏠 Total hospitalize',value=f"{hospital} คน")
                        embed.add_field(name='🏠 New hospitalize',value=f"{hospitalnew} คน")
                        embed.add_field(name='☠️ Total death',value=f"{death} คน")
                        embed.add_field(name='☠️ New death',value=f"{newdeath} คน")
                        embed.set_footer(text=f'''Source : {source}''')

                        message= await ctx.send(embed=embed)
                        await message.add_reaction('💊')

    @commands.command(aliases = ['covid','corona','cv19'])
    async def covid19(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            async with aiohttp.ClientSession() as session:
                async with session.get('https://disease.sh/v3/covid-19/all') as r:
                    r = await r.json()

                    case = r['cases']
                    todaycase = r['todayCases']
                    totaldeath = r['deaths']
                    todaydeath = r['todayDeaths']
                    recover = r['recovered']
                    todayRecover = r['todayRecovered']      
                    activecase = r['active']

                    case = humanize.intcomma(case)
                    todaycase = humanize.intcomma(todaycase)
                    totaldeath = humanize.intcomma(totaldeath)
                    todaydeath = humanize.intcomma(todaydeath)
                    recover = humanize.intcomma(recover)
                    todayRecover = humanize.intcomma(todayRecover)
                    activecase = humanize.intcomma(activecase)

            if server_language == "Thai": 
                embed = discord.Embed(
                    colour =0x00FFFF,
                    title = "💊สถานะไวรัสโควิด-19 ทั่วโลก",
                    description = "เเหล่งที่มา : https://disease.sh/v3/covid-19/all"

                )
                embed.set_thumbnail(url="https://i.imgur.com/kmabvi8.png")

                embed.add_field(name="📊 ยืนยันเเล้ว : ", value=f"{case}")
                embed.add_field(name="💀 เสียชีวิตแล้ว : ", value=f"{totaldeath}")
                embed.add_field(name="✅ รักษาหายแล้ว : ", value=f"{recover}")
                embed.add_field(name="📈 ผู้ติดเชื่อวันนี้ : ", value=f"{case}")
                embed.add_field(name="💀 จำนวนเสียชีวิตวันนี้ : ", value=f"{todaydeath}")
                embed.add_field(name="✅ รักษาหายวันนี้ : ", value=f"{todayRecover}")
                embed.add_field(name="⚠️ ผู้ติดเชื้อ : ", value=f"{activecase}")

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('💊')
            
            if server_language == "English": 
                embed = discord.Embed(
                    colour =0x00FFFF,
                    title = "💊Covid-19 around the world",
                    description = "Source : https://disease.sh/v3/covid-19/all"

                )
                embed.set_thumbnail(url="https://i.imgur.com/kmabvi8.png")

                embed.add_field(name="📊 Total confirm cases : ", value=f"{case}")
                embed.add_field(name="💀 Total death : ", value=f"{totaldeath}")
                embed.add_field(name="✅ Total recover patients : ", value=f"{recover}")
                embed.add_field(name="📈 Total confirm cases today : ", value=f"{todaycase}")
                embed.add_field(name="💀 New death : ", value=f"{todaydeath}")
                embed.add_field(name="✅ Today recover patients : ", value=f"{todayRecover}")
                embed.add_field(name="⚠️ Active cases : ", value=f"{activecase}")

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('💊')

    @commands.command()
    async def geoip(self,ctx, *, ip):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            ip = str(ip)
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://extreme-ip-lookup.com/json/{ip}') as r:
                    r = await r.json()

            if server_language == "Thai":
                if r["status"] == "success":
                    embed = discord.Embed(
                        colour = 0xfed000,
                        title =f":satellite_orbital: ・ɢᴇᴏ ʟᴏᴄᴀᴛɪᴏɴ ↷",
                        description = f"""
```xl
• 𝗥𝗘𝗦𝗨𝗟𝗧𝗦 ↷
  ประเภทของ IP : {r["ipType"]}
  ประเทศ : {r["country"]}
  โค้ดประเทศ : {r["countryCode"]}
  จังหวัด : {r["city"]}
  ทวีป : {r["continent"]}
  ค่ายเน็ท : {r["isp"]}
  ภูมิภาค : {r["region"]}
  ชื่อองค์กร : {r["org"]}
  ชื่อบริษัท : {r["businessName"]}
  เว็บไซต์บริษัท : {r["businessWebsite"]}
  Logitude : {r["lon"]}
  Latitude : {r["lat"]}
``````xl
• IP ที่ค้นหา : {r['query']}```
                    """
                )
                    embed.add_field(name=":file_cabinet: ᴀᴘɪ ꜱᴛᴀᴛᴜꜱ",value=f"[ꜱᴛᴀᴛᴜꜱ ꜱᴜᴄᴄᴇꜱꜱ](http://extreme-ip-lookup.com/json/{ip})")
                    embed.add_field(name=":desktop: ᴀᴘɪ ᴜꜱᴇᴅ",value=f"[ᴇxᴛʀᴇᴍᴇ-ɪᴘ](http://extreme-ip-lookup.com/json/)")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('💻')

                else:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"ไม่พบ IP",
                        description = f"""
```xl                        
• IP ที่ค้นหา : {ip}```"""
                    )

            if server_language == "English":
                if r["status"] == "success":
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title =f":satellite_orbital: ・ɢᴇᴏ ʟᴏᴄᴀᴛɪᴏɴ ↷",
                        description = f"""
```xl
• 𝗥𝗘𝗦𝗨𝗟𝗧𝗦 ↷
  type of IP : {r["ipType"]}
  country : {r["country"]}
  country code : {r["countryCode"]}
  city : {r["city"]}
  continent : {r["continent"]}
  ISP : {r["isp"]}
  region : {r["region"]}
  organization : {r["org"]}
  business name : {r["businessName"]}
  business website : {r["businessWebsite"]}
  Logitude : {r["lon"]}
  Latitude : {r["lat"]}
``````xl
• IP search : {r['query']}```
                    """
                )
                    embed.add_field(name=":file_cabinet: ᴀᴘɪ ꜱᴛᴀᴛᴜꜱ",value=f"[ꜱᴛᴀᴛᴜꜱ ꜱᴜᴄᴄᴇꜱꜱ](http://extreme-ip-lookup.com/json/{ip})")
                    embed.add_field(name=":desktop: ᴀᴘɪ ᴜꜱᴇᴅ",value=f"[ᴇxᴛʀᴇᴍᴇ-ɪᴘ](http://extreme-ip-lookup.com/json/)")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('💻')
                else:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"IP not found",
                        description = f"""
```xl                        
• IP search : {ip}```"""
                    )
                    
    @geoip.error
    async def geoip_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` กรุณาระบุ IP ที่ต้องการที่จะค้นหา ``{settings.COMMAND_PREFIX}geoip (IP)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify an IP to search for ``{settings.COMMAND_PREFIX}geoip (IP)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def youtube(self,ctx, *, keywords):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            apikey = settings.youtubeapi
            youtube = build('youtube', 'v3', developerKey=apikey)

            snippet = youtube.search().list(part='snippet', q=keywords,type='video',maxResults=50).execute()
            req = (snippet["items"][0])
            

            video_title = req["snippet"]["title"]
            video_id = req["id"]["videoId"]
            thumbnail = req["snippet"]["thumbnails"]["high"]["url"]
            channel_title = req["snippet"]["channelTitle"]
            description = req["snippet"]["description"]

            clip_url = "http://www.youtube.com/watch?v="+ video_id

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={apikey}") as r:
                    r = await r.json()

            stat = r["items"][0]
            view = stat["statistics"]["viewCount"]
            like = stat["statistics"]["likeCount"]
            dislike = stat["statistics"]["dislikeCount"]
            comment = stat["statistics"]["dislikeCount"]

            view = humanize.intcomma(int(view))
            like = humanize.intcomma(int(like))
            dislike = humanize.intcomma(int(dislike))
            comment = humanize.intcomma(int(comment))

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={apikey}") as r:
                    re = await r.json()
            
            items = re["items"][0]
            Age_restriction = False
            rating = items["contentDetails"]["contentRating"]
            if "ytrating" in rating and rating["ytRating"] == "ytAgeRestricted":
                Age_restriction = True
        
            if server_language == "Thai":
                if Age_restriction is True:
                    if ctx.channel.is_nsfw():
                        embed = discord.Embed(
                            title = video_title,
                            colour = 0x00FFFF , 
                            description = f"[ดูคลิปนี้]({clip_url})"
                        )
                        embed.add_field(name ="ชื่อช่อง" , value = f"{channel_title}")
                        embed.add_field(name ="วิวทั้งหมด" , value = f"{view}")
                        embed.add_field(name ="คอมเม้นทั้งหมด" , value = f"{comment}")
                        embed.add_field(name ="ไลค์" , value = f"{like}")
                        embed.add_field(name ="ดิสไลค์" , value = f"{dislike}")
                        embed.add_field(name ="คำอธิบาย" , value = f"{description}")
                        
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.set_image(url=thumbnail)
                        message= await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                    
                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            title =f"NSFW",
                            description = f"คุณไม่สามารถค้นหาเนื้อหา 18+ ในช่องเเชทนี้ได้ โปรดใช้ในห้อง NSFW เท่านั้น"
                            )

                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()

                        message= await ctx.send(embed=embed)
                        await message.add_reaction('✨')

                else:
                    embed = discord.Embed(
                            title = video_title,
                            colour = 0x00FFFF , 
                            description = f"[ดูคลิปนี้]({clip_url})"
                        )
                    embed.add_field(name ="ชื่อช่อง" , value = f"{channel_title}")
                    embed.add_field(name ="วิวทั้งหมด" , value = f"{view}")
                    embed.add_field(name ="คอมเม้นทั้งหมด" , value = f"{comment}")
                    embed.add_field(name ="ไลค์" , value = f"{like}")
                    embed.add_field(name ="ดิสไลค์" , value = f"{dislike}")
                    embed.add_field(name ="คำอธิบาย" , value = f"{description}")
                    
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_image(url=thumbnail)
                    message= await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            
            if server_language == "English":
                if Age_restriction is True:
                    if ctx.channel.is_nsfw():
                        embed = discord.Embed(
                            title = video_title,
                            colour = 0x00FFFF , 
                            description = f"[click here]({clip_url})"
                        )
                        embed.add_field(name ="Channel" , value = f"{channel_title}")
                        embed.add_field(name ="View" , value = f"{view}")
                        embed.add_field(name ="Comment" , value = f"{comment}")
                        embed.add_field(name ="Like" , value = f"{like}")
                        embed.add_field(name ="Dislike" , value = f"{dislike}")
                        embed.add_field(name ="Description" , value = f"{description}")
                        
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.set_image(url=thumbnail)
                        message= await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                    
                    else:
                        embed = discord.Embed(
                            colour = 0x983925,
                            title =f"NSFW",
                            description = f"you are not allow to search for 18+ content in this text channel please use this in NSFW channel"
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.timestamp = datetime.datetime.utcnow()

                        message= await ctx.send(embed=embed)
                        await message.add_reaction('✨')
                
                else:
                    embed = discord.Embed(
                            title = video_title,
                            colour = 0x00FFFF , 
                            description = f"[click here]({clip_url})"
                        )
                    embed.add_field(name ="Channel" , value = f"{channel_title}")
                    embed.add_field(name ="View" , value = f"{view}")
                    embed.add_field(name ="Comment" , value = f"{comment}")
                    embed.add_field(name ="Like" , value = f"{like}")
                    embed.add_field(name ="Dislike" , value = f"{dislike}")
                    embed.add_field(name ="Description" , value = f"{description}")
                    
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_image(url=thumbnail)
                    message= await ctx.send(embed=embed)
                    await message.add_reaction('✅')
          
    @youtube.error
    async def youtube_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{settings.COMMAND_PREFIX}youtube [ชื่อคลิป]``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` need to specify what video to search on Youtube ``{settings.COMMAND_PREFIX}youtube [video name]``"
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def ytsearch(self,ctx, *, keywords):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            apikey = settings.youtubeapi
            youtube = build('youtube', 'v3', developerKey=apikey)
            snippet = youtube.search().list(part='snippet', q=keywords,type='video',maxResults=50).execute()
            i = 1
            if server_language == "Thai":
                embed = discord.Embed(
                        title = "ค้นหาวิดีโอจาก YouTube",
                        colour = 0x00FFFF , 
                        description = f"ค้นหา: {keywords}"
                    )
                while i != 6:
                    req = (snippet["items"][i])
                    video_title = req["snippet"]["title"]
                    video_id = req["id"]["videoId"]
                    clip_url = "http://www.youtube.com/watch?v="+ video_id
                    embed.add_field(name=f"{i}. {video_title}",value=f"{clip_url}", inline=False)
                    i = i+1

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message= await ctx.send(embed=embed)
                await message.add_reaction('✅')
            
            if server_language == "English":
                embed = discord.Embed(
                        title = "Video from YouTube",
                        colour = 0x00FFFF , 
                        description = f"search: {keywords}"
                    )
                while i != 6:
                    req = (snippet["items"][i])
                    video_title = req["snippet"]["title"]
                    video_id = req["id"]["videoId"]
                    clip_url = "http://www.youtube.com/watch?v="+ video_id
                    embed.add_field(name=f"{i}. {video_title}",value=f"{clip_url}", inline=False)
                    i = i+1

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message= await ctx.send(embed=embed)
                await message.add_reaction('✅')
                                
    @ytsearch.error
    async def ytsearch_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{settings.COMMAND_PREFIX}ytsearch [keywords]``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what video to search ``{settings.COMMAND_PREFIX}ytsearch [keywords]``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def country(self,ctx, *, country):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://restcountries.eu/rest/v2/name/{country}?fullText=true") as r:
                    r = await r.json()

            name = r[0]['name']
            population = r[0]['population']
            area = r[0]['area']
            capital = r[0]['capital']
            subregion = r[0]['subregion']
            nativename = r[0]['nativeName']
            timezone = r[0]['timezones'][0]
            currency = r[0]['currencies'][0]['name']
            symbol = r[0]['currencies'][0]['symbol']
            language = r[0]['languages'][0]['name']
            code = r[0]['alpha2Code']
            codephone = r[0]['callingCodes'][0]

            population = humanize.intcomma(population)
            area =humanize.intcomma(area)

            codelower = code.lower()

            flag = (f"https://flagcdn.com/256x192/{codelower}.png")

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"{name}",
                    description = f"""```

ชื่อพื้นเมือง : {nativename}
โค้ดประเทศ : {code}
รหัสโทร : {codephone}
ภูมิภาค : {subregion}
ประชากร : {population} คน
เมืองหลวง : {capital}
พื้นที่ : {area} km²
เขตเวลา : {timezone}
สกุลเงิน : {currency} สัญลักษณ์ : ({symbol})
ภาษา : {language}```""")

                embed.set_thumbnail(url=flag)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                await message.add_reaction('😊')

            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"{name}",
                    description = f"""```

Native name : {nativename}
country code : {code}
calling code : {codephone}
subregion : {subregion}
population : {population} peoples
capital city : {capital}
area : {area} km²
timezone : {timezone}
currency : {currency} symbol : ({symbol})
language : {language}```""")

                embed.set_thumbnail(url=flag)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)

                await message.add_reaction('😊')

    @country.error
    async def country_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อประเทศที่จะดู ``{settings.COMMAND_PREFIX}country (country)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a country to search ``{settings.COMMAND_PREFIX}country (country)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def pingweb(self,ctx, website = None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai": 
                if website is None: 
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมเว็บที่จะดู ``{settings.COMMAND_PREFIX}pingweb (website)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                else:
                    try:
                        r = requests.get(website).status_code
                        if r == 404:
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = f"สถานะของเว็บไซต์ {website}",
                                description = f" ⚠️`` เว็บไซต์ไม่ออนไลน์```")
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed ) 
                            await message.add_reaction('⚠️') 

                        else:
                            embed = discord.Embed(
                                colour = 0x75ff9f,
                                title = f"สถานะของเว็บไซต์ {website}",
                                description = f"```เว็บไซต์ออนไลน์ปกติ```"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed=embed )

                    except requests.exceptions.MissingSchema:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` เว็บอาจไม่ถูกต้อง ``{settings.COMMAND_PREFIX}pingweb (website)``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
                    
                    except requests.exceptions.ConnectionError:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` เว็บอาจไม่ถูกต้อง ``{settings.COMMAND_PREFIX}pingweb (website)``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
                        
            
            if server_language == "English": 
                if website is None: 
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a website to search ``{settings.COMMAND_PREFIX}pingweb (website)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                else:
                    try:
                        r = requests.get(website).status_code
                        if r == 404:
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = f"Status of {website}",
                                description = f" ⚠️`` Website is offline```")
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed ) 
                            await message.add_reaction('⚠️') 

                        else:
                            embed = discord.Embed(
                                colour = 0x75ff9f,
                                title = f"Status of {website}",
                                description = f"``` Website is online```"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed=embed )

                    except requests.exceptions.MissingSchema:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` Unable to find the website ``{settings.COMMAND_PREFIX}pingweb (website)``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
                    
                    except requests.exceptions.ConnectionError:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️``{ctx.author}`` Unable to find the website ``{settings.COMMAND_PREFIX}pingweb (website)``"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
                        
    @commands.command()
    async def weather(self,ctx, *, city):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.openweathermapAPI}') as r:
                        r = await r.json()
                        if not r["cod"] == "404":
                            temperature = (float(r['main']['temp']) -273.15)
                            feellike = (float(r['main']['feels_like']) -273.15)
                            highesttemp = (float(r['main']['temp_max']) -273.15)
                            lowesttemp = (float(r['main']['temp_min']) -273.15)
                            humidity = float(r['main']['humidity'])
                            windspeed = float(r['wind']['speed'])
                            
                            day = r['weather'][0]['description']

                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = f"สภาพอากาศในจังหวัด {city}",
                                description = f"""```
อุณหภูมิตอนนี้ : {round(temperature,1)}°C
อุณหภูมิสูงสุดของวัน : {round(highesttemp,1)}°C
อุณหภูมิตํ่าสุดของวัน : {round(lowesttemp,1)}°C
อุณหภูมิรู้สึกเหมือน : {round(feellike,1)}°C
ความชื้น : {round(humidity)}%
ความเร็วลม : {round(windspeed,2)}mph
สภาพอากาศ : {day}```
                            """
                            
                        )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            await ctx.send(embed=embed)

                        else:
                            embed = discord.Embed(
                                colour = 0x983925,
                                description = f" ⚠️``{ctx.author}`` ไม่มีจังหวัดนี้กรุณาตรวจสอบตัวสะกด ``{settings.COMMAND_PREFIX}weather (city)``"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed ) 
                            await message.add_reaction('⚠️')
            
            if server_language == "English":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.openweathermapAPI}') as r:
                        r = await r.json()
                        if not r["cod"] == "404":
                            temperature = (float(r['main']['temp']) -273.15)
                            feellike = (float(r['main']['feels_like']) -273.15)
                            highesttemp = (float(r['main']['temp_max']) -273.15)
                            lowesttemp = (float(r['main']['temp_min']) -273.15)
                            humidity = float(r['main']['humidity'])
                            windspeed = float(r['wind']['speed'])
                            
                            day = r['weather'][0]['description']

                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = f"weather in {city}",
                                description = f"""```
Temperature now : {round(temperature,1)}°C
Highest temperature today : {round(highesttemp,1)}°C
Lowest temperature today : {round(lowesttemp,1)}°C
Feel like : {round(feellike,1)}°C
Humidity : {round(humidity)}%
windspeed : {round(windspeed,2)}mph
Weather : {day}```
                    """
                        
                    )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            await ctx.send(embed=embed)

                        else:
                            embed = discord.Embed(
                                colour = 0x983925,
                                description = f" ⚠️``{ctx.author}`` Cannot find this city ``{settings.COMMAND_PREFIX}weather (city)``"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed ) 
                            await message.add_reaction('⚠️')

    @weather.error
    async def weather_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อจังหวัดที่จะดู ``{settings.COMMAND_PREFIX}weather (city)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อจังหวัดที่จะดู ``{settings.COMMAND_PREFIX}weather (city)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
    
    @commands.command()
    async def checklink(self,ctx, website):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://sitecheck.sucuri.net/api/v3/?scan={website}") as r:
                        response = await r.json()
                        certissuer = response["tls"]["cert_issuer"]
                        certexpire = response["tls"]["cert_expires"]
                        certauthority = response["tls"]["cert_authority"]
                        embed = discord.Embed(
                            title = "เช็คลิงค์",
                            description = f"**Certification**\n``Certification Issuer:`` {certissuer}\n``certification expire:`` {certexpire}\n``certificaiton authority:`` {certauthority}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✔️')

            if server_language == "English":
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://sitecheck.sucuri.net/api/v3/?scan={website}") as r:
                        response = await r.json()
                        certissuer = response["tls"]["cert_issuer"]
                        certexpire = response["tls"]["cert_expires"]
                        certauthority = response["tls"]["cert_authority"]
                        embed = discord.Embed(
                            title = "เช็คลิงค์",
                            description = f"**Certification**\n``Certification Issuer:`` {certissuer}\n``certification expire:`` {certexpire}\n``certificaiton authority:`` {certauthority}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✔️')

    @commands.command()
    async def gold(self, ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                url = "https://xn--42cah7d0cxcvbbb9x.com/"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        soupObject = BeautifulSoup(await response.text(), "html.parser")
                        table = soupObject.find_all('td', class_="em bg-em g-n")
                        date = soupObject.find('td',class_="span bg-span txtd al-r")
                        time = soupObject.find('td', class_ = "em bg-span txtd al-r")

                        gold_bar_buy = table[0]
                        gold_bar_sell = table[1]
                        gold_jewelry_buy = table[2]
                        gold_jewelry_sell = table[3]

                        date = date.contents[0]
                        time = time.contents[0]
                        gold_bar_buy = gold_bar_buy.contents[0]
                        gold_bar_sell = gold_bar_sell.contents[0]
                        gold_jewelry_buy = gold_jewelry_buy.contents[0]
                        gold_jewelry_sell = gold_jewelry_sell.contents[0]
                        date_and_time = (f"{date} {time}")

                embed = discord.Embed(
                    title = "ราคาทอง",
                    colour = 0xfed000,
                    description = f"""
**ทองเเท่งคําเเท่ง**                   
```xl
ราคาขายออก {gold_bar_sell} ฿
ราคารับซื้อ {gold_bar_buy} ฿
```
**ทองรูปพรรณ**
```xl
ราคาขายออก {gold_jewelry_sell} ฿
ราคารับซื้อ {gold_jewelry_buy} ฿
```
อัพเดทล่าสุด {date_and_time}
          
                    """
                )
                await ctx.send(embed=embed)
            
            else:
                pass

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
