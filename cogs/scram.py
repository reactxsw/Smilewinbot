import discord
from discord.ext import commands
import aiohttp
import asyncio
import re
import requests
from bs4 import BeautifulSoup
import settings
from utils.languageembed import languageEmbed




scram_link = requests.get("https://raw.githubusercontent.com/DevSpen/scam-links/master/src/links.txt").text.splitlines()

async def check_scram_link(self,message):
    if message.author.bot:
        return
    
    link = re.search("(?P<url>https?://[^\s]+)",message.content)
    if link != None:
        #bypassing bit.ly and take a url out of it
        b_link = requests.Session().get(link.group("url"),allow_redirects=True).url
        domain = get_domain_name_from_url(b_link)
        if domain in scram_link:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")

        print(domain)
        if domain in scram_link:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
    else:
        for content in message.content.split():
            if content in scram_link:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Please do not send the scam links!")

    
    print("run link")


class Scram(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def scram(self,ctx):
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
                embed.add_field(name="Add",value="`scram add [link]`")
                embed.add_field(name="Remove",value="`scram remove [link]`")
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
                embed.add_field(name="Add",value="`scram add [link]`")
                embed.add_field(name="Remove",value="`scram remove [link]`")
                embed.add_field(name="📢Note",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""", Inline=False)


    @scram.command()
    async def add(self,ctx,link):
        pass


    @scram.command()
    async def remove(self,ctx,link):
        pass
        


def get_domain_name_from_url(url):
    return url.split("//")[-1].split("/")[0]



def setup(bot):
    bot.add_cog(Scram(bot))