import nextcord
from nextcord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def cockfight(self,ctx):
        pass

    @commands.command()
    async def roulette(self,ctx):
        pass

def setup(bot: commands.Bot):
    bot.add_cog(Gamble(bot))