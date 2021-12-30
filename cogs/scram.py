import discord
from discord.ext import commands
import aiohttp
import asyncio
import re
import requests
import settings
from utils.languageembed import languageEmbed




scram_link = requests.get("https://raw.githubusercontent.com/DevSpen/scam-links/master/src/links.txt").text.splitlines()
scram_link2 = requests.get("https://raw.githubusercontent.com/matomo-org/referrer-spam-list/master/spammers.txt").text.splitlines()

async def get_link_bypassing(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url,allow_redirects=True) as resp:
            return await resp.text()

async def message_handle(message):
    # mode_data = setting.collectionlsjflsjflsjfdb.find_one({"guild_id": message.guild.id})
    mode_data = get_mode_data(message.guild.id)
    mode = mode_data["mode"]
    if mode == "warn":
        await message.channel.send(f"{message.author.mention} Please do not send the scam links!")
    elif mode == "delete":
        await message.delete()
        await message.channel.send(f"{message.author.mention} Please do not send the scam links!")



async def check_scram_link(self,message):
    if message.author.bot:
        return
    
    link = re.search("(?P<url>https?://[^\s]+)",message.content)
    if link != None:
        #bypassing bit.ly and take a url out of it
        b_link = await get_link_bypassing(link.group("url"))
        domain = await get_domain_name_from_url(b_link)
        if domain in scram_link or domain in scram_link2:
            await message_handle(message)

    else:
        #if link not found in message
        #example https://www.youtube.com/ == Found
        #example www.youtube.com == Not Found    this block will  try www.youtube.com is in the list or not
        for content in message.content.split():
            if content in scram_link or content in scram_link2:
                await message_handle(message)

    
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
    async def mode(self,ctx,mode):
        _fetch_data = get_mode_data(ctx.guild.id) #This line will make sure that guild is in the database
        if mode == "warn":
            # await settings.sdfsdfsdfsdf.update_one({"guild_id":ctx.guild.id},{'$set':{"mode":"warn"}})
            await ctx.send(f"{ctx.author.mention} Set mode to warn")
        elif mode == "delete":
            # await settings.sdfsdfsdfs.update_one({"guild_id":ctx.guild.id},{'$set':{"mode":"delete"}})
            await ctx.send(f"{ctx.author.mention} Set mode to delete")

    @scram.command()
    async def add(self,ctx,link):
        pass
    
    @scram.command()
    async def remove(self,ctx,link):
        pass

async def get_mode_data(guild_id):
    # data = settings.clsjflsjflsjflsjfdb.find_one({"guild_id": guild_id})
    # if data == None:
    #     settings.clsjflsjflsjflsjfdb.insert_one({"guild_id": guild_id, "mode": "warn"})
    #     return settings.clsjflsjflsjflsjfdb.find_one({"guild_id": guild_id})
    # else:
    #     return data
    data = {"_id":"293874293423","guild_id": "293874293423","mode": "warn"}
    return data

async def get_domain_name_from_url(url):
    return url.split("//")[-1].split("/")[0]



def setup(bot):
    bot.add_cog(Scram(bot))