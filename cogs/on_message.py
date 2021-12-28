from importlib import reload
import discord
from discord.ext import commands
from cogs.level import update_level
from cogs.utils.scram import check_scram_link
import cogs.utils.scram as scram

class Test_on_message_event(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        await self.bot.wait_until_ready()
        await update_level(self,message)
        await check_scram_link(self,message)


def setup(bot):
    reload(scram)
    bot.add_cog(Test_on_message_event(bot))