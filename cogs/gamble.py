import imp
import nextcord
import random
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
    @commands.command()
    async def horse(self,ctx):
        race = []
        for i in range(1, 5):
            space = "-"*random.randint(3,5)
            dic = {f"horse{i}":f"{space}🏇"}
            dic.append(race)
def setup(bot: commands.Bot):
    bot.add_cog(Gamble(bot))