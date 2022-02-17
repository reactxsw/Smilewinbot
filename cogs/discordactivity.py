import nextcord
import settings
from utils.languageembed import languageEmbed
from nextcord.ext import commands
from discord_together import DiscordTogether


class DiscordActivity(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        bot.loop.create_task(self.start_dtg())

    async def start_dtg(self):
        await self.bot.wait_until_ready()
        self.togetherControl = await DiscordTogether(settings.TOKEN)

    @commands.command()
    async def watchyt(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} ต้องเข้าห้องพูดคุยก่อน",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "youtube"
                        )
                        await ctx.send(f"คลิกที่ลิงก์เพื่อเริ่ม:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="บอทไม่มีสิทธิ์ ``สร้างลิงค์เชิญ``",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

            if server_language == "English":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} need to join voice channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "youtube"
                        )
                        await ctx.send(f"Click on the link to start:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="Bot don't have ``CREATE_INVITE`` permission",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

    @commands.command()
    async def poker(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} ต้องเข้าห้องพูดคุยก่อน",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "poker"
                        )
                        await ctx.send(f"คลิกที่ลิงก์เพื่อเริ่ม:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="บอทไม่มีสิทธิ์ ``สร้างลิงค์เชิญ``",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

            if server_language == "English":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} need to join voice channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "poker"
                        )
                        await ctx.send(f"Click on the link to start:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="Bot don't have ``CREATE_INVITE`` permission",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

    @commands.command()
    async def chess(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} ต้องเข้าห้องพูดคุยก่อน",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "chess"
                        )
                        await ctx.send(f"คลิกที่ลิงก์เพื่อเริ่ม:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="บอทไม่มีสิทธิ์ ``สร้างลิงค์เชิญ``",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

            if server_language == "English":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} need to join voice channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "chess"
                        )
                        await ctx.send(f"Click on the link to start:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="Bot don't have ``CREATE_INVITE`` permission",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

    @commands.command()
    async def betrayal(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} ต้องเข้าห้องพูดคุยก่อน",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "betrayal"
                        )
                        await ctx.send(f"คลิกที่ลิงก์เพื่อเริ่ม:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="บอทไม่มีสิทธิ์ ``สร้างลิงค์เชิญ``",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

            if server_language == "English":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} need to join voice channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "betrayal"
                        )
                        await ctx.send(f"Click on the link to start:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="Bot don't have ``CREATE_INVITE`` permission",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

    @commands.command()
    async def fishing(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} ต้องเข้าห้องพูดคุยก่อน",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "fishing"
                        )
                        await ctx.send(f"คลิกที่ลิงก์เพื่อเริ่ม:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="บอทไม่มีสิทธิ์ ``สร้างลิงค์เชิญ``",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)

            if server_language == "English":
                voice_state = ctx.author.voice
                if voice_state is None:
                    embed = nextcord.Embed(
                        description=f"{ctx.author.mention} need to join voice channel",
                        colour=0x983925,
                    )
                    await ctx.send(embed=embed)

                else:
                    try:
                        link = await self.togetherControl.create_link(
                            ctx.author.voice.channel.id, "poker"
                        )
                        await ctx.send(f"Click on the link to start:\n{link}")

                    except nextcord.ext.commands.errors.BotMissingPermissions:
                        embed = nextcord.Embed(
                            description="Bot don't have ``CREATE_INVITE`` permission",
                            colour=0x983925,
                        )
                        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DiscordActivity(bot))
