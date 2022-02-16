from nextcord.ext.commands.core import command
from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands


class ServerStat(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def setnewserver(self, ctx):
        newserver = {
            "guild_id": ctx.guild.id,
            "status_system": "NO",
            "category_id": "None",
            "status_total_id": "None",
            "status_members_id": "None",
            "status_bots_id": "None",
        }
        return newserver

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setserverstat(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
        else:
            status = "YES"
            overwrites = {
                ctx.guild.default_role: nextcord.PermissionOverwrite(connect=False)
            }

            server = await settings.collectionstatus.find_one(
                {"guild_id": ctx.guild.id}
            )
            memberonly = len([member for member in ctx.guild.members if not member.bot])
            botonly = int(ctx.guild.member_count) - int(memberonly)

            if server is None:
                newserver = await ServerStat.setnewserver(self, ctx)
                await settings.collectionstatus.insert_one(newserver)
                category = await ctx.guild.create_category(
                    "📊 SERVER STATS 📊", position=0
                )
                totalvc = await ctx.guild.create_voice_channel(
                    f"︱👥 Total : {ctx.guild.member_count}",
                    overwrites=overwrites,
                    category=category,
                )
                membervc = await ctx.guild.create_voice_channel(
                    f"︱👥 Members : {memberonly}",
                    overwrites=overwrites,
                    category=category,
                )
                botvc = await ctx.guild.create_voice_channel(
                    f"︱👥 Bots : {botonly}", overwrites=overwrites, category=category
                )

                await settings.collectionstatus.update_one(
                    {"guild_id": ctx.guild.id},
                    {
                        "$set": {
                            "status_system": status,
                            "category_id": category.id,
                            "status_total_id": totalvc.id,
                            "status_members_id": membervc.id,
                            "status_bots_id": botvc.id,
                        }
                    },
                )

            else:
                server_language = languageserver["Language"]
                total = self.bot.get_channel(server["status_total_id"])
                members = self.bot.get_channel(server["status_members_id"])
                bots = self.bot.get_channel(server["status_bots_id"])
                category = self.bot.get_channel(server["category_id"])

                if category:
                    if total:
                        if total.category_id == server["category_id"]:
                            if total.position == 0:
                                pass

                            else:
                                await total.edit(position=0)

                        else:
                            await total.edit(
                                name=f"︱👥 Total : {ctx.guild.member_count}",
                                category=category,
                                position=0,
                            )

                    else:
                        totalvc = await ctx.guild.create_voice_channel(
                            f"︱👥 Total : {ctx.guild.member_count}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_total_id": totalvc.id}},
                        )

                    if members:
                        if members.category_id == server["status_members_id"]:
                            if members.position == 1:
                                pass

                            else:
                                await members.edit(position=1)

                        else:
                            await members.edit(
                                name=f"︱👥 Members : {memberonly}",
                                category=category,
                                position=1,
                            )

                    else:
                        membervc = await ctx.guild.create_voice_channel(
                            f"︱👥 Members : {memberonly}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_members_id": membervc.id}},
                        )

                    if bots:
                        if bots.category_id == server["category_id"]:
                            if bots.position == 2:
                                pass

                            else:
                                await bots.edit(position=2)

                        else:
                            await bots.edit(
                                name=f"︱👥 Bots : {botonly}",
                                category=category,
                                position=2,
                            )

                    else:
                        botvc = await ctx.guild.create_voice_channel(
                            f"︱👥 Bots : {botonly}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_bots_id": botvc.id}},
                        )

                else:
                    category = await ctx.guild.create_category(
                        "📊 SERVER STATS 📊", position=0
                    )
                    await settings.collectionstatus.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"category_id": category.id}},
                    )
                    if total:
                        if total.category_id == server["category_id"]:
                            if total.position == 0:
                                pass

                            else:
                                await total.edit(position=0)

                        else:
                            await total.edit(
                                name=f"︱👥 Total : {ctx.guild.member_count}",
                                category=category,
                                position=0,
                            )

                    else:
                        totalvc = await ctx.guild.create_voice_channel(
                            f"︱👥 Total : {ctx.guild.member_count}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_total_id": totalvc.id}},
                        )

                    if members:
                        if members.category_id == server["status_members_id"]:
                            if members.position == 1:
                                pass

                            else:
                                await members.edit(position=1)

                        else:
                            await members.edit(
                                name=f"︱👥 Members : {memberonly}",
                                category=category,
                                position=1,
                            )

                    else:
                        membervc = await ctx.guild.create_voice_channel(
                            f"︱👥 Members : {memberonly}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_members_id": membervc.id}},
                        )

                    if bots:
                        if bots.category_id == server["category_id"]:
                            if bots.position == 2:
                                pass

                            else:
                                await bots.edit(position=2)

                        else:
                            await bots.edit(
                                name=f"︱👥 Bots : {botonly}",
                                category=category,
                                position=2,
                            )

                    else:
                        botvc = await ctx.guild.create_voice_channel(
                            f"︱👥 Bots : {botonly}",
                            overwrites=overwrites,
                            category=category,
                        )
                        await settings.collectionstatus.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"status_bots_id": botvc.id}},
                        )

                if server_language == "Thai":
                    embed = nextcord.Embed(title="ตั้งค่าสําเร็จ", colour=0xFED000)
                    await ctx.send(embed=embed)

                if server_language == "English":
                    embed = nextcord.Embed(title="Setup complete", colour=0xFED000)
                    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ServerStat(bot))