from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands


class BotSetup(commands.Cog):
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

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def level(self, ctx: commands.Context):
        language = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = language["Language"]
            if server_language == "Thai":
                embed = nextcord.Embed(colour=0x00FFFF, description="ต้องระบุ ON / OFF")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF, description="you need to specify on / off"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @level.error
    async def level_error(self, ctx: commands.Context, error):
        language = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = language["Language"]
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

    @level.command(aliases=["on"])
    @commands.has_permissions(administrator=True)
    async def levelon(self, ctx: commands.Context):
        language = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = language["Language"]
            if server_language == "Thai":
                status = "YES"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"level_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าเลเวล",
                        description=f"ได้ทําการเปิดใช้งานระบบนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    level_status = server["level_system"]
                    if level_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเลเวล",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเลเวล",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "YES"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"level_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Level system",
                        description=f"The level system have been activated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    level_status = server["level_system"]
                    if level_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Level system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Level system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @levelon.error
    async def levelon_error(self, ctx: commands.Context, error):
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

    @level.command(aliases=["off"])
    @commands.has_permissions(administrator=True)
    async def leveloff(self, ctx: commands.Context):
        language = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = language["Language"]
            if server_language == "Thai":
                status = "NO"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าเลเวล",
                        description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    level_status = server["level_system"]
                    if level_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเลเวล",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าเลเวล",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "NO"
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"introduce_status": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Level system",
                        description=f"The level system have been deactivated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    level_status = server["level_system"]
                    if level_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Level system",
                            description=f"The level system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"level_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Level system",
                            description=f"The level system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @leveloff.error
    async def leveloff_error(self, ctx: commands.Context, error):
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

    @commands.group(invoke_without_command=True)
    async def logvoice(self, ctx: commands.Context):
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

    @logvoice.command(aliases=["on"])
    @commands.has_permissions(administrator=True)
    async def logvoiceon(self, ctx: commands.Context):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"log_voice_system": status}},
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
                            {"$set": {"log_voice_system": status}},
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
                            {"$set": {"log_voice_system": status}},
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
                    newserver = await BotSetup.setnewserver(self, ctx)
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
                            {"$set": {"log_voice_system": status}},
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
                            {"$set": {"log_voice_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @logvoiceon.error
    async def logvoiceon_error(self, ctx: commands.Context, error):
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

    @logvoice.command(aliases=["off"])
    @commands.has_permissions(administrator=True)
    async def logvoiceoff(self, ctx: commands.Context):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"log_voice_system": status}},
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
                    intro_status = server["log_voice_system"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"log_voice_system": status}},
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
                            {"$set": {"log_voice_system": status}},
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"log_voice_system": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        description=f"The command have been deactivated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    intro_status = server["log_voice_system"]
                    if intro_status == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"log_voice_system": status}},
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
                            {"$set": {"log_voice_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            description=f"The command have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @logvoiceoff.error
    async def logvoiceoff_error(self, ctx: commands.Context, error):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx: commands.Context, channel: nextcord.TextChannel):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            embed = nextcord.Embed(
                title="Language setting / ตั้งค่าภาษา",
                description="```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```"
                + "\n"
                + "/r setlanguage thai : เพื่อตั้งภาษาไทย"
                + "\n"
                + "/r setlanguage english : To set English language",
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "log_channel_id": channel.id,
                                "log_voice_system": "YES",
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
                    introduce_channel = server["log_channel_id"]
                    if introduce_channel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "log_channel_id": channel.id,
                                    "log_voice_system": "YES",
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
                                    "log_channel_id": channel.id,
                                    "log_voice_system": "YES",
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "log_channel_id": channel.id,
                                "log_voice_system": "YES",
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
                    introduce_channel = server["log_channel_id"]
                    if introduce_channel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "log_channel_id": channel.id,
                                    "log_voice_system": "YES",
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
                                    "log_channel_id": channel.id,
                                    "log_voice_system": "YES",
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

    @setlog.error
    async def setlog_error(self, ctx: commands.Context, error):
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
    async def setup(self, ctx: commands.Context):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    embed = nextcord.Embed(
                        title="ตั้งค่าสําเร็จ",
                        colour=0x00FFFF,
                        description=f"ลงทะเบือนเซิฟเวอร์ในฐานข้อมูลสําเร็จ",
                    )
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    sid = server["_id"]
                    embed = nextcord.Embed(
                        title="มีข้อมูลของเซิฟเวอร์ในฐานข้อมูลเเล้ว",
                        colour=0x00FFFF,
                        description=f"ไอดีของเซิฟเวอร์ในฐานข้อมูลคือ {sid}",
                    )
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

            if server_language == "English":

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    embed = nextcord.Embed(
                        title="Setup complete",
                        colour=0x00FFFF,
                        description=f"Your server is now registered on the database",
                    )
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    sid = server["_id"]
                    embed = nextcord.Embed(
                        title="Server data already exist",
                        colour=0x00FFFF,
                        description=f"ID of your server in database {sid}",
                    )
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

    @setup.error
    async def setup_error(self, ctx: commands.Context, error):
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

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def economy(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = nextcord.Embed(colour=0x00FFFF, description="ต้องระบุ ON / OFF")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            if server_language == "English":
                embed = nextcord.Embed(
                    colour=0x00FFFF, description="you need to specify on / off"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @economy.command(aliases=["on"])
    @commands.has_permissions(administrator=True)
    async def ____on(self, ctx: commands.Context):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"economy_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งระบบเศรษฐกิจ",
                        description=f"ได้ทําการเปิดใช้งานระบบนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    economy_status = server["economy_system"]
                    if economy_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งระบบเศรษฐกิจ",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งระบบเศรษฐกิจ",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "YES"

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"economy_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Economy system",
                        description=f"The level system have been activated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    economy_status = server["economy_system"]
                    if economy_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Economy system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Economy system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @____on.error
    async def economyon_error(self, ctx: commands.Context, error):
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

    @economy.command(aliases=["off"])
    @commands.has_permissions(administrator=True)
    async def ____off(self, ctx: commands.Context):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"economy_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งระบบเศรษฐกิจ",
                        description=f"ได้ทําการปิดใช้งานระบบนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    economy_status = server["economy_system"]
                    if economy_status == "YES":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งระบบเศรษฐกิจ",
                            description=f"ได้ทําการปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งระบบเศรษฐกิจ",
                            description=f"ได้ทําการปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "NO"

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"economy_system": status}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Economy system",
                        description=f"The level system have been deactivated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    economy_status = server["economy_system"]
                    if economy_status == "YES":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Economy system",
                            description=f"The level system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"economy_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Economy system",
                            description=f"The level system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @____off.error
    async def economyoff_error(self, ctx: commands.Context, error):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setwelcome(self, ctx: commands.Context, channel: nextcord.TextChannel):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"welcome_id": channel.id}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                        description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    welcome = server["welcome_id"]
                    if welcome == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"welcome_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"welcome_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description=f"ห้องได้ถูกอัพเดตเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"welcome_id": channel.id}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="channel for welcome",
                        description=f"Channel have been set to {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    welcome = server["welcome_id"]
                    if welcome == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"welcome_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for welcome",
                            description=f"Channel have been set to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"welcome_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for welcome",
                            description=f"Channel have been set to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @setwelcome.error
    async def setwelcome_error(self, ctx: commands.Context, error):
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
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนเข้าเซิฟเวอร์``{settings.COMMAND_PREFIX}setwelcome #channel``",
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
                        description=f" ⚠️``{ctx.author}`` need to specify a channel ``{settings.COMMAND_PREFIX}setwelcome #channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setleave(self, ctx: commands.Context, channel: nextcord.TextChannel):
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
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"leave_id": channel.id}}
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                        description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    leave = server["leave_id"]
                    if leave == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"leave_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"leave_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description=f"ห้องได้ถูกอัพเดตเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await BotSetup.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id}, {"$set": {"leave_id": channel.id}}
                    )

                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="channel for leave",
                        description=f"Channel have been set to {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    leave = server["leave_id"]
                    if leave == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"leave_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for leave",
                            description=f"Channel have been set to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"leave_id": channel.id}},
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="channel for leave",
                            description=f"Channel have been set to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @setleave.error
    async def setleave_error(self, ctx: commands.Context, error):
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
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนออกเซิฟเวอร์``{settings.COMMAND_PREFIX}setleave #channel``",
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
                        description=f" ⚠️``{ctx.author}`` need to specify a channel ``{settings.COMMAND_PREFIX}setleave #channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

def setup(bot: commands.Bot):
    bot.add_cog(BotSetup(bot))
