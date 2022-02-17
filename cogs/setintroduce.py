from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands

class Introduce(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    async def setnewserver(self, ctx: commands.Context):
        newserver = {
            "guild_id": ctx.guild.id,
            "welcome_id": "None",
            "leave_id": "None",
            "introduce_channel_id": "None",
            "introduce_frame": "None",
            "introduce_role_give_id": "None",
            "introduce_role_remove_id": "None",
            "introduce_status": "YES",
            "level_system": "NO",
            "economy_system": "NO",
            "currency": "$",
            "verification_system": "NO",
            "verification_time": 10,
            "verification_channel_id": "None",
            "verification_role_give_id": "None",
            "verification_role_remove_id": "None",
            "log_voice_system": "NO",
            "log_channel_id": "None",
            "scam": "warn",
            "Music_channel_id": "None",
            "Embed_message_id": "None",
            "Music_message_id": "None",
        }
        return newserver

    @commands.group(invoke_without_command=True,aliases=["setintroduce-role"])
    @commands.has_permissions(administrator=True)
    async def setintroducerole(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0xfed000, description="คุณต้องระบุ give / remove"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            else:
                embed = nextcord.Embed(
                    colour=0xfed000, description="you need to specify give / remove"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @setintroducerole.error
    async def setintroducerole_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @setintroducerole.command(aliases=["give"])
    @commands.has_permissions(administrator=True)
    async def introductiongive(self, ctx: commands.Context, role: nextcord.Role):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_role_give_id": role.id}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                        description=f"ยศที่ได้ถูกตั้งเป็น {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    give_role_id = server["introduce_role_give_id"]
                    if give_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                            description=f"ยศที่ได้ถูกตั้งเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                            description=f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_role_give_id": role.id}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="role to give",
                        description=f"role to give after member introduce themself have been set to {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    give_role_id = server["introduce_role_give_id"]
                    if give_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to give",
                            description=f"role to give after member introduce themself have been set to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to give",
                            description=f"role to give after member introduce themself have been updated to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @introductiongive.error
    async def introductiongive_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ระบุยศที่จะให้หลังจากเเนะนําตัว",
                        description=f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะให้หลังจากเเนะนําตัว ``{settings.COMMAND_PREFIX}setrole give @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Specify a role to give after a member introduce themself",
                        description=f" ⚠️``{ctx.author}`` need to specify a role to give after a member introduce themself ``{settings.COMMAND_PREFIX}setrole give @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @setintroducerole.command(aliases=["remove"])
    @commands.has_permissions(administrator=True)
    async def introductionremove(self, ctx: commands.Context, role: nextcord.Role):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_role_remove_id": role.id}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                        description=f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    remove_role_id = server["introduce_role_remove_id"]
                    if remove_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                            description=f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                            description=f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_role_remove_id": role.id}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="role to remove",
                        description=f"role to remove after member introduce themself have been set to {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    remove_role_id = server["introduce_role_remove_id"]
                    if remove_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to remove",
                            description=f"role to remove after member introduce themself have been set to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to remove",
                            description=f"role to remove after member introduce themself have been updated to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @introductionremove.error
    async def introductionremove_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ระบุยศที่จะลบหลังจากเเนะนําตัว",
                        description=f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะลบหลังจากเเนะนําตัว ``{settings.COMMAND_PREFIX}setrole remove @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Specify a role to remove after a member introduce themself",
                        description=f" ⚠️``{ctx.author}`` need to specify a role to give after a member introduce themself ``{settings.COMMAND_PREFIX}setrole give @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setintroduce(self, ctx: commands.Context, channel: nextcord.TextChannel):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "introduce_channel_id": channel.id,
                                "introduce_status": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าห้องเเนะนําตัว",
                        description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    introduce_channel = server["introduce_channel_id"]
                    if introduce_channel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "introduce_channel_id": channel.id,
                                    "introduce_status": "YES",
                                }
                            },
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเนะนําตัว",
                            description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "introduce_channel_id": channel.id,
                                    "introduce_status": "YES",
                                }
                            },
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเนะนําตัว",
                            description=f"ห้องได้ถูกอัพเดตเป็น {channel.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "introduce_channel_id": channel.id,
                                "introduce_status": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="channel for introduction",
                        description=f"Channel have been set to {channel.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    introduce_channel = server["introduce_channel_id"]
                    if introduce_channel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "introduce_channel_id": channel.id,
                                    "introduce_status": "YES",
                                }
                            },
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for introduction",
                            description=f"Channel have been set to {channel.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "introduce_channel_id": channel.id,
                                    "introduce_status": "YES",
                                }
                            },
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for introduction",
                            description=f"Channel have been updated to {channel.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @setintroduce.error
    async def setintroduce_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ระบุห้องที่จะตั้ง",
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเนะนําตัว ``{settings.COMMAND_PREFIX}setintroduce #channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Specify a channel",
                        description=f" ⚠️``{ctx.author}`` need to specify a channel ``{settings.COMMAND_PREFIX}setintroduce #channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setframe(self, ctx: commands.Context, *, frame):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"introduce_frame": frame}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ากรอบเเนะนําตัว",
                        description=f"กรอบได้ถูกตั้งเป็น {frame}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    frame = server["introduce_frame"]
                    if frame == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_frame": frame}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ากรอบเเนะนําตัว",
                            description=f"กรอบได้ถูกตั้งเป็น {frame}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_frame": frame}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ากรอบเเนะนําตัว",
                            description=f"กรอบได้ถูกอัพเดตเป็น {frame}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"introduce_frame": frame}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="set frame",
                        description=f"frame have been set to {frame}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    frame = server["introduce_frame"]
                    if frame == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_frame": frame}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="set frame",
                            description=f"frame have been set to {frame}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_frame": frame}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="set frame",
                            description=f"frame have been updated to {frame}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @setframe.error
    async def setframe_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="ระบุกรอบที่จะตั้ง",
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ระบุกรอบที่จะตั้ง ``{settings.COMMAND_PREFIX}setframe (frame)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Specify a frame",
                        description=f" ⚠️``{ctx.author}`` need to specify a frame ``{settings.COMMAND_PREFIX}setframe (frame)``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def introduce(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(
                    colour=0x00FFFF, description="คุณต้องระบุ ON / OFF"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF, description="you need to specify ON / OFF"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @introduce.command(aliases=["on"])
    @commands.has_permissions(administrator=True)
    async def introduce_on(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            if server_language == "Thai":
                status = "YES"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าเเนะนําตัว",
                        description=f"ได้ทําการเปิดใช้งานคําสั่งนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    intro_status = server["introduce_status"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเเนะนําตัว",
                            description=f"ได้ทําการเปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเเนะนําตัว",
                            description=f"ได้ทําการเปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "YES"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF, description=f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    intro_status = server["introduce_status"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @introduce_on.error
    async def introduce_on_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @introduce.command(aliases=["off"])
    @commands.has_permissions(administrator=True)
    async def introduce_off(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                status = "NO"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าห้องเเนะนําตัว",
                        description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    intro_status = server["introduce_status"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเนะนําตัว",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเนะนําตัว",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "NO"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await Introduce.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        description=f"The command have been deactivated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    intro_status = server["introduce_status"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"introduce_status": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @introduce_off.error
    async def introduce_off_error(self, ctx: commands.Context, error):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่า",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")
                    
def setup(bot: commands.Bot):
    bot.add_cog(Introduce(bot))
