from discord.ext import commands
import aiohttp
import settings
import discord


class Image(commands.Cog): 
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    async def bird(self,ctx):
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

            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/birb") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพนก"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐦')
            
            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="Bird"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐦')

    @commands.command()
    async def panda(self,ctx):
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

            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/panda") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพเเพนด้า"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐼')
            
            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="Panda"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐼')

    @commands.command()
    async def cat(self,ctx):
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

            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/cat") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพเเมว"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐱')
            
            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพเเมว"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐱')

    @commands.command()
    async def dog(self,ctx):
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

            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/dog") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพหมา"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐶')
            
            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="Dog"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐶')

    @commands.command()
    async def fox(self,ctx):
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

            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/fox") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพสุนัขจิ้งจอก"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🦊')
            
            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="Fox"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🦊')

    @commands.command()
    async def koala(self,ctx):
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
            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/img/koala") as r:
                    r = await r.json()
                    url = r['link']

            if server_language == "Thai":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="ภาพหมีโคอาล่า"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐨')

            if server_language == "English":
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title="Koala"

                )
                embed.set_image(url=url)
                message = await ctx.send(embed= embed)
                await message.add_reaction('🐨')

    @commands.command()
    async def wasted(self,ctx, member: discord.Member=None):
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
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "💀 Wasted!",
                    description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💀')
            
            if server_language == "English":
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "💀 Wasted!",
                    description = f"link: [click here](https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})")
                message =await ctx.send(embed=embed)
                await message.add_reaction('💀')

    @commands.command()
    async def gay(self,ctx, member: discord.Member=None):
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
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "🏳️‍🌈 Gay!" , 
                    description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/gay/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/gay/?avatar={avatar_url}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('🏳️‍🌈')
            
            if server_language == "English":
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "🏳️‍🌈 Gay!" , 
                    description = f"link: [click here](https://some-random-api.ml/canvas/gay/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/gay/?avatar={avatar_url}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('🏳️‍🌈')

    @commands.command()
    async def iphonex(self,ctx , image=None):
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

            if image is None:
                image = ctx.author.avatar_url
            
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={image}") as r:
                    r = await r.json()

            url = r['message']

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "Iphone X"

            )
            embed.set_image(url=url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('📱')

    @commands.command()
    async def phcomment(self,ctx , * ,text):
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

            image = ctx.author.avatar_url
            username = ctx.author

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={image}&text={text}&username={username}") as r:
                    r = await r.json()

            url = r['message']

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "Pornhub"

            )
            embed.set_image(url=url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('📱')

    @phcomment.error
    async def phcomment_error(self,ctx,error):
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
                        description = f" ⚠️``{ctx.author}`` จะต้อง text ที่จะใส่ใน comment``{settings.COMMAND_PREFIX}phcomment (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a text to put as comment ``{settings.COMMAND_PREFIX}phcomment (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def trigger(self,ctx, member: discord.Member=None):
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
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "😠 Triggered",
                    description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/triggered/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/triggered/?avatar={avatar_url}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('😠')

            if server_language == "English":
                if member is None:
                    member = ctx.author

                avatar_url = member.avatar_url_as(format="png")

                embed = discord.Embed(
                    colour=0x00FFFF,
                    title= "😠 Triggered",
                    description = f"link: [click here](https://some-random-api.ml/canvas/triggered/?avatar={avatar_url})"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.set_image(url=f"https://some-random-api.ml/canvas/triggered/?avatar={avatar_url}")
                message =await ctx.send(embed=embed)
                await message.add_reaction('😠')

    @commands.command()
    async def tweet(self,ctx, username: str, *, message: str): 
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
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
                    response = await r.json()
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = "🕊️ Twitter generator"


                    )
                    embed.set_image(url=response["message"])
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('👍')

    @tweet.error
    async def tweet_error(self,ctx,error):
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
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ username เเละ text  ที่จะใส่ในสเตตัส twitter``{settings.COMMAND_PREFIX}tweet (username) (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a text and to put as status``{settings.COMMAND_PREFIX}tweet (username) (text)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

def setup(bot: commands.Bot):
    bot.add_cog(Image(bot))