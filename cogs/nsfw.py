from nextcord.ext import commands
from utils.languageembed import languageEmbed
from utils.language.translate import translate_nsfw
import aiohttp
import nextcord
import settings
import datetime
import requests
import random

class Nsfw(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.language = translate_nsfw.call()
        
    @commands.command()
    async def anal(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed= languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/anal") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "Anal"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def porn(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]            
            if ctx.channel.is_nsfw():
                tag = random.randint(1,39235)
                url = f"https://cdn.porngifs.com/img/{tag}"
                response = requests.get(url)
                file = open(f"download/pg{tag}.gif", "wb")
                file.write(response.content)
                file.close()
                file = nextcord.File(f"download/pg{tag}.gif", filename=f"pg{tag}.gif")
                embed = nextcord.Embed(
                    colour = 0xFC7EF5,
                )   
                embed.set_image(url=f"attachment://pg{tag}.gif")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed , file=file)   
                await message.add_reaction('❤️')
                
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def gsolo(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/solog") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "Girl solo"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')


    @commands.command()
    async def erofeet(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/erofeet") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "erofeet"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')
    
    @commands.command()
    async def feet(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/feetg") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "feet"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def pussy(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/pussy_jpg") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "pussy"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def hentai(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/Random_hentai_gif") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "hentai"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')
                
    @commands.command()
    async def eroyuri(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/eroyuri") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "eroyuri"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def yuri(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/yuri") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "yuri"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def solo(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/solo") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "solo"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def classic(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw(): 
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/classic") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "classic"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
            
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def boobs(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/boobs") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "boobs"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')
        
            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def tits(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/tits") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "tits"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')
                    
    @commands.command()
    async def blowjob(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/blowjob") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "tits"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')

    @commands.command()
    async def lewd(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/nsfw_neko_gif") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "lewd"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')


    @commands.command()
    async def lesbian(self,ctx):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            if ctx.channel.is_nsfw():
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://nekos.life/api/v2/img/les") as r:
                        r = await r.json()
                        embed = nextcord.Embed(
                            colour = 0xFC7EF5,
                            title = "lesbian"

                        )   
                        url = r['url']
                        embed.set_image(url=url)
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)   
                        await message.add_reaction('❤️')

            else:
                embed = nextcord.Embed(
                    colour = 0x983925,
                    title ="NSFW",
                    description = self.language[server_language]["Error"]["is_nsfw"]
                    )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                embed.timestamp = datetime.datetime.utcnow()

                message= await ctx.send(embed=embed)
                await message.add_reaction('✨')
            
def setup(bot: commands.Bot):
    bot.add_cog(Nsfw(bot))
