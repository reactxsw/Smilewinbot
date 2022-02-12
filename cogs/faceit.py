from aiohttp.client import ClientSession, request
import nextcord
from utils.languageembed import languageEmbed
from nextcord import embeds
from nextcord.client import Client
from nextcord.ext.commands.core import command
import humanize
import settings
import math
import aiohttp
import flag
from nextcord.ext import commands


class Faceit(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.base_url = "https://open.faceit.com/data/v4"

        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {settings.faceitapi}",
        }

    def distance(self, a, b):
        if a == b:
            return 0
        if a < 0 and b < 0 or a > 0 and b > 0:
            return (abs(abs(a) - abs(b))) if a < b else -(abs(abs(a) - abs(b)))

        return math.copysign((abs(a) + abs(b)), b)

    @commands.command()
    async def faceitcsgo(self, ctx, nickname=None):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            if not nickname is None:
                urlnick = f"{self.base_url}/players?nickname={nickname}"
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(urlnick) as rnick:
                        rnick = await rnick.json()

                game_id = "csgo"
                player_id = rnick["player_id"]
                nick = rnick["nickname"]
                avatarurl = rnick["avatar"]
                country = rnick["country"]
                region = rnick["games"]["csgo"]["region"]
                csgolvl = rnick["games"]["csgo"]["skill_level"]
                csgoelo = rnick["games"]["csgo"]["faceit_elo"]
                csgoelocom = humanize.intcomma(csgoelo)

                cflag = flag.flag(country.upper())
                urlrankregion = f"{self.base_url}/rankings/games/{game_id}/regions/{region}/players/{player_id}"
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(urlrankregion) as rankregion:
                        rankregion = await rankregion.json()
                        regionpos = rankregion["position"]
                        regionpos = humanize.intcomma(regionpos)

                urlrankcountry = f"{self.base_url}/rankings/games/{game_id}/regions/{region}/players/{player_id}?country={country}&limit=1"
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(urlrankcountry) as rankcountry:
                        rankcountry = await rankcountry.json()
                        countrypos = rankcountry["position"]
                        countrypos = humanize.intcomma(countrypos)

                urlstat = f"{self.base_url}/players/{player_id}/stats/{game_id}"
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(urlstat) as stat:
                        stat = await stat.json()

                longestwinstreak = stat["lifetime"]["Longest Win Streak"]
                totalmatch = stat["lifetime"]["Matches"]
                kdratio = stat["lifetime"]["Average K/D Ratio"]
                avgheadshot = stat["lifetime"]["Average Headshots %"]
                totalwin = stat["lifetime"]["Wins"]
                winrate = stat["lifetime"]["Win Rate %"]
                totalhs = stat["lifetime"]["Total Headshots %"]
                rcmatch = stat["lifetime"]["Recent Results"]
                rcmatch = ["W" if m == "1" else "L" for m in rcmatch]
                totallose = int(totalmatch) - int(totalwin)

                faceitdict = {
                    1: {
                        "downlevelicon": "",
                        "levelicon": f"<:faceitlvl1:{settings.faceitlvl1}>",
                        "uplevelicon": f"<:faceitlvl2:{settings.faceitlvl2}>",
                        "upelo": 801 - csgoelo,
                        "downelo": "",
                    },
                    2: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl1}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl2}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl3}>",
                        "upelo": 951 - csgoelo,
                        "downelo": self.distance(800, csgoelo),
                    },
                    3: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl2}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl3}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl4}>",
                        "upelo": 1101 - csgoelo,
                        "downelo": self.distance(950, csgoelo),
                    },
                    4: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl3}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl4}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl5}>",
                        "upelo": 1251 - csgoelo,
                        "downelo": self.distance(1100, csgoelo),
                    },
                    5: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl4}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl5}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl6}>",
                        "upelo": 1401 - csgoelo,
                        "downelo": self.distance(1250, csgoelo),
                    },
                    6: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl5}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl6}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl7}>",
                        "upelo": 1551 - csgoelo,
                        "downelo": self.distance(1400, csgoelo),
                    },
                    7: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl6}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl7}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl8}>",
                        "upelo": 1701 - csgoelo,
                        "downelo": self.distance(1550, csgoelo),
                    },
                    8: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl7}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl8}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl9}>",
                        "upelo": 1851 - csgoelo,
                        "downelo": self.distance(1700, csgoelo),
                    },
                    9: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl8}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl9}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl10}>",
                        "upelo": 2001 - csgoelo,
                        "downelo": self.distance(1850, csgoelo),
                    },
                    10: {
                        "downlevelicon": f"<:faceitlvl1:{settings.faceitlvl9}>",
                        "levelicon": f"<:faceitlvl2:{settings.faceitlvl10}>",
                        "uplevelicon": f"<:faceitlvl3:{settings.faceitlvl4}>",
                        "upelo": "∞",
                        "downelo": self.distance(2000, csgoelo),
                    },
                }
                downelo = faceitdict[csgolvl]["downelo"]
                upelo = faceitdict[csgolvl]["upelo"]
                levelicon = faceitdict[csgolvl]["levelicon"]
                downlevelicon = faceitdict[csgolvl]["downlevelicon"]
                uplevelicon = faceitdict[csgolvl]["uplevelicon"]

                if region.lower() == "us":
                    regionicon = f"<:faceitus:{settings.faceitus}>"

                elif region.lower() == "as":
                    regionicon = f"<:faceitsea:{settings.faceitas}>"

                elif region.lower() == "eu":
                    regionicon = f"<:faceiteu:{settings.faceiteu}>"

                else:
                    regionicon = f"<:faceitsea:{settings.faceitsea}>"

                downelo = humanize.intcomma(downelo)
                rcmatch = " ".join([str(elem) for elem in rcmatch])
                embed = nextcord.Embed(
                    title=f"**CSGO FACEIT** <:faceitlogo:{settings.faceitlogo}>",
                    description=f"""
**Username** : **{nick}**

> {regionicon}  **{regionpos}**
> {cflag}  **{countrypos}**
> {levelicon}  **{csgoelocom}**
> {downlevelicon}  **-{downelo}** | **+{upelo}** {uplevelicon}

**Stats**:
```
Total match : {totalmatch}
K/D : {kdratio}
Total win : {totalwin}
Total loses : {totallose}
Winrate : {winrate} %   
Total Headshots : {totalhs}
Average Headshots %: {avgheadshot} %
Longest win streak : {longestwinstreak}```
**Recent Results**:
```{rcmatch}```
""",
                    colour=0xFD5A00,
                )
                embed.set_thumbnail(url=avatarurl)
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Faceit(bot))
