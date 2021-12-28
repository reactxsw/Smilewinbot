import discord
from discord.ext import commands
import aiohttp
import asyncio
import re
import requests
from urllib.parse import urlparse



scram_link = requests.get("https://raw.githubusercontent.com/DevSpen/scam-links/master/src/links.txt").text.splitlines()

async def check_scram_link(self,message):
    if message.author.bot:
        return
    
    link = re.search("(?P<url>https?://[^\s]+)",message.content)
    if link != None:
        s_link = requests.Session().head(link.group("url"), allow_redirects=True).url
        domain = urlparse(s_link).netloc
        print(domain)
        if domain in scram_link:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please do not send the scam links!")
    else:
        for content in message.content.split():
            if content in scram_link:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Please do not send the scam links!")

    
    print("run link")