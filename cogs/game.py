import nextcord
import random
import asyncio

from requests.models import Response
import settings
from utils.languageembed import languageEmbed
from nextcord.ext import commands


class Game(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def rps(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(colour=0xFED000, title="เกมเป่ายิ้งฉุบ")

                embed.set_image(
                    url="https://smilewinbot.web.app/assets/image/host/rps.gif"
                )
                embed.set_footer(text=f"⏳ กดที่ emoji ภายใน10วินาที")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✊")
                await message.add_reaction("✋")
                await message.add_reaction("✌️")

                answer = "none"
                try:
                    reaction,user = await self.bot.wait_for(
                        "reaction_add",
                        timeout=10,
                        check=lambda reaction , user: user.id == ctx.author.id,
                    )

                    if str(reaction.emoji) == "✊":
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        answer = "scissor"

                    rps = [
                        "https://smilewinbot.web.app/assets/image/host/rock.png",
                        "https://smilewinbot.web.app/assets/image/host/paper.png",
                        "https://smilewinbot.web.app/assets/image/host/scissor.png",
                    ]
                    responses = {
                        "https://smilewinbot.web.app/assets/image/host/rock.png": {
                            "rock": "😮 เสมอ",
                            "paper": "😄 คุณชนะ",
                            "scissor": "😭 คุณเเพ้",
                        },
                        "https://smilewinbot.web.app/assets/image/host/paper.png": {
                            "rock": "😭 คุณเเพ้",
                            "paper": "😮 คุณเสมอ",
                            "scissor": "😄 คุณชนะ",
                        },
                        "https://smilewinbot.web.app/assets/image/host/scissor.png": {
                            "rock": "😄 คุณชนะ",
                            "paper": "😭 คุณเเพ้",
                            "scissor": "😮 คุณเสมอ",
                        },
                    }
                    botresponse = random.choice(rps)
                    embed = nextcord.Embed(
                        colour=0xFED000,
                        title="Rock paper scissor",
                        description=responses[botresponse][answer],
                    )
                    embed.set_image(url=botresponse)
                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="🕑 หมดเวลา",
                    )

                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/gameover.jpg"
                    )

                    await message.edit(embed=embed)

            if server_language == "English":
                embed = nextcord.Embed(colour=0xFED000, title="เกมเป่ายิ้งฉุบ")

                embed.set_image(
                    url="https://smilewinbot.web.app/assets/image/host/rps.gif"
                )
                embed.set_footer(text=f"⏳ click on emoji in 10 seconds")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✊")
                await message.add_reaction("✋")
                await message.add_reaction("✌️")
                answer = "none"
                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add",
                        timeout=10,
                        check=lambda reaction, user: user.id == ctx.author.id,
                    )

                    if str(reaction.emoji) == "✊":
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        answer = "scissor"

                    rps = [
                        "https://smilewinbot.web.app/assets/image/host/rock.png",
                        "https://smilewinbot.web.app/assets/image/host/paper.png",
                        "https://smilewinbot.web.app/assets/image/host/scissor.png",
                    ]
                    responses = {
                        "https://smilewinbot.web.app/assets/image/host/rock.png": {
                            "rock": "😮 Draw",
                            "paper": "😄 You won",
                            "scissor": "😭 You lose",
                        },
                        "https://smilewinbot.web.app/assets/image/host/paper.png": {
                            "rock": "😭 You lose",
                            "paper": "😮 Draw",
                            "scissor": "😄 You won",
                        },
                        "https://smilewinbot.web.app/assets/image/host/scissor.png": {
                            "rock": "😄 You won",
                            "paper": "😭 You lose",
                            "scissor": "😮 Draw",
                        },
                    }
                    botresponse = random.choice(rps)
                    embed = nextcord.Embed(
                        colour=0xFED000,
                        title="Rock paper scissor",
                        description=responses[botresponse][answer],
                    )
                    embed.set_image(url=botresponse)
                    await message.edit(embed=embed)

                except asyncio.TimeoutError:

                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="🕑 Out of time",
                    )

                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/gameover.jpg"
                    )

                    await message.edit(embed=embed)

    @commands.command(aliases=["coin", "flipcoin"])
    async def coinflip(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            num = random.randint(0, 100)
            if num > 50:
                flip = "https://smilewinbot.web.app/assets/image/host/tail.png"

            else:
                flip = "https://smilewinbot.web.app/assets/image/host/head.png"
            responses = {
                "https://smilewinbot.web.app/assets/image/host/tail.png": [
                    "ก้อย",
                    "tail",
                ],
                "https://smilewinbot.web.app/assets/image/host/head.png": [
                    "หัว",
                    "head",
                ],
            }

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0xFED000,
                    title="ทอยเหรียญ",
                    description=f"คุณ ``{ctx.author}`` ทอยได้{responses[flip][0]}",
                )
                embed.set_image(url=flip)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await ctx.send(embed=embed)

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0xFED000,
                    title="Coin flip",
                    description=f"``{ctx.author}`` got {responses[flip][1]}",
                )
                embed.set_image(url=flip)
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))
