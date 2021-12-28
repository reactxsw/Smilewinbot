import discord
from discord.ext import commands
import requests

response = requests.get("https://raw.githubusercontent.com/DevSpen/scam-links/master/src/links.txt").content
scram_link = response.decode("utf-8").splitlines()

class Scam(commands.Cog):
    def __init__(self, bot) :
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        msg_content = message.content
        if message.author.bot:
            return
        
        msg_split = msg_content.split()
        for msg in msg_split:
            if msg in scram_link:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Don't send scam links here!")
                return


def setup(bot):
    bot.add_cog(Scam(bot))