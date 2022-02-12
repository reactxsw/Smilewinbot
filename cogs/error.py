import settings, os, logging, nextcord, traceback
from utils.languageembed import languageEmbed
from datetime import datetime, timedelta, timezone
from nextcord.ext import commands


class Error(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        current_time = datetime.now()
        # gmt_7 = timezone(timedelta(hours=7))
        thai_time = (str(current_time.astimezone(timezone(timedelta(hours=7))))).split(
            "."
        )[0]
        print(traceback.print_exc())
        errorlog = (
            f"\n{thai_time}: [{ctx.author} | {str(ctx.author.id)}] in [{str(ctx.guild.id)} | {ctx.guild.name}]"
            + "{Error:"
            + f"{traceback.format_exc().strip()},userinput: {ctx.message.content},command: {ctx.command}"
            + "}"
        )
        with open("logs/error.log", "a", encoding="UTF-8") as log:
            log.write(errorlog)

        log.close()
        channel = self.bot.get_channel(int(settings.supportchannel))
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            pass

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.CommandNotFound):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title=f"⚠️ | ไม่มีคําสั่งนี้กรุณาเช็คการสะกดคําว่าถูกหรือผิด",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                elif isinstance(error, commands.BotMissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title=f"⚠️บอทไม่มีสิทธิ คุณต้องให้สิทธิเเอดมินกับบอทก่อนใช้คําสั่งนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")
                else:
                    await channel.send(errorlog)
                    await channel.send(error)

            if server_language == "English":
                if isinstance(error, commands.CommandNotFound):
                    embed = nextcord.Embed(
                        colour=0x983925, title=f"⚠️ | Command not found"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                elif isinstance(error, commands.BotMissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title=f"⚠️ | Bot don't have enough permission to do that please give administrator permission to the bot",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                else:
                    await channel.send(errorlog)
                    await channel.send(error)


def setup(bot: commands.Bot):
    bot.add_cog(Error(bot))
