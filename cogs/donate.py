import os
import nextcord
from nextcord.colour import Color
import settings
import datetime
import aiohttp
import validators
import requests
from nextcord.ext import commands
from utils.languageembed import languageEmbed


class Invite(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def donate(self, ctx, GIFT_URL):
        if "https://gift.truemoney.com/campaign/?v=" in GIFT_URL:
            async with aiohttp.ClientSession() as session:
                async with session.get(GIFT_URL) as response:
                    if response.status == 200:
                        VOUCHER_CODE = str(
                            GIFT_URL.split("https://gift.truemoney.com/campaign/?v=")[1]
                        )
                        async with session.get(
                            f"https://gift.truemoney.com/campaign/vouchers/{VOUCHER_CODE}/verify?mobile={settings.phonenumber}"
                        ) as check:
                            resp = await check.json()
                            gift_code = resp["status"]["code"]
                            gift_status = resp["data"]["voucher"]["status"]
                            if gift_status == "active":
                                if gift_code != "CANNOT_GET_OWN_VOUCHER":
                                    async with session.post(
                                        f"https://gift.truemoney.com/campaign/vouchers/{VOUCHER_CODE}/redeem",
                                        json={
                                            "mobile": f"{settings.phonenumber}",
                                            "voucher_hash": f"{VOUCHER_CODE}",
                                        },
                                        headers={
                                            "Accept": "application/json",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                                            "Content-Type": "application/json",
                                            "Origin": "https://gift.truemoney.com",
                                            "Accept-Language": "en-US,en;q=0.9",
                                            "Connection": "keep-alive",
                                        },
                                    ) as redeem:
                                        if redeem.status == 200:
                                            data = await redeem.json()
                                            gift_owner = data["data"]["owner_profile"][
                                                "full_name"
                                            ]
                                            amount_redeem = float(
                                                data["data"]["amount_baht"]
                                            )
                                            embed = nextcord.Embed(
                                                title="ขอบคุณครับ",
                                                description=f"บริจาคเงินจํานวน {amount_redeem} ให้บอท smilewin",
                                                Color=0xFED000,
                                            )
                                            await ctx.send(embed=embed)
                                            print(
                                                f"รับเงินสําเร็จจาก {gift_owner} จํานวน {amount_redeem}"
                                            )

                                        else:
                                            embed = nextcord.Embed(
                                                title="", description="", Color=0xFED000
                                            )
                                            await ctx.send(embed=embed)
                            else:
                                embed = nextcord.Embed(
                                    title="", description="", Color=0xFED000
                                )
                                await ctx.send(embed=embed)
                                print("ไม่พบอั่งเปา")
        else:
            embed = nextcord.Embed(title="", description="", Color=0xFED000)
            await ctx.send(embed=embed)
            print("ลิงค์อั่งเปาไม่ถูกต้อง")

    @donate.error
    async def donate_error(self, ctx, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ลิงค์อั่งเปาที่จะบริจาค ``{settings.COMMAND_PREFIX}donate [link]``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ลิงค์อั่งเปาที่จะบริจาค ``{settings.COMMAND_PREFIX}donate [link]``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")


def setup(bot: commands.Bot):
    bot.add_cog(Invite(bot))
