from aiohttp.helpers import ProxyInfo
import discord
from discord.ext import commands
import aiohttp
import asyncio
import re
import requests
import settings
from utils.languageembed import languageEmbed

async def get_domain_name_from_url(url):
    return url.split("//")[-1].split("/")[0]

with open("data/phishing.txt") as f:
    phishing = [x.strip() for x in f.readlines()] 

async def get_link_bypassing(url):
    return requests.Session().head(url,allow_redirects=True).url

async def check_scam_link(message):
    link = re.search("(?P<url>https?://[^\s]+)", message.content)

    if link != None:
        link = link.group("url")
        if "bit.ly" in link:
            url = await get_link_bypassing(link)
        domain = await get_domain_name_from_url(url)
        if domain in phishing:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
            
    else:
        pass

class Scam(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def scam(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            if languageserver == "Thai":
                embed = discord.Embed(
                    title = "Scram command information",
                    colour = 0xFED000,
                )
                embed.add_field(name="Add",value="`scam add [link]`")
                embed.add_field(name="Remove",value="`scam remove [link]`")
                embed.add_field(name="📢หมายเหตุ",value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""", Inline=False)
            elif languageserver == "English":
                embed = discord.Embed(
                    title = "Scram command information",
                    colour = 0xFED000,
                )
                embed.add_field(name="Add",value="`scam add [link]`")
                embed.add_field(name="Remove",value="`scam remove [link]`")
                embed.add_field(name="📢Note",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""", Inline=False)


    @scam.command()
    async def mode(self,ctx,mode):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            if languageserver == "Thai":
                if mode == "warn":
                    await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"warn"}})
                    await ctx.send(f"{ctx.author.mention} Set mode to warn")
                elif mode == "delete":
                    await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"delete"}})
                    await ctx.send(f"{ctx.author.mention} Set mode to delete")
                
                else:
                    pass
                    #raise eror บอกว่ามีเเค่ warn / delete
            
            if languageserver == "English":
                if mode == "warn":
                    await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"warn"}})
                    await ctx.send(f"{ctx.author.mention} Set mode to warn")
                elif mode == "delete":
                    await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"delete"}})
                    await ctx.send(f"{ctx.author.mention} Set mode to delete")

                else:
                    pass
                    #raise eror บอกว่ามีเเค่ warn / delete

    @scam.command()
    async def add(self,ctx,link):
        pass


    @scam.command()
    async def remove(self,ctx,link):
        pass



def setup(bot):
    bot.add_cog(Scam(bot))