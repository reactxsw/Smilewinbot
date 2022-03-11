from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands


class SetVerify(commands.Cog):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setverify(self, ctx: commands.Context, channel: nextcord.TextChannel):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_channel_id": channel.id,
                                "verification_system": "YES",
                            }
                        },
                    )

                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่าห้องยืนยันตัวตน",
                        description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verifychannel = server["verification_channel_id"]
                    if verifychannel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "verification_channel_id": channel.id,
                                    "verification_system": "YES",
                                }
                            },
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องยืนยันตัวตน",
                            description=f"ห้องได้ถูกตั้งเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "verification_channel_id": channel.id,
                                    "verification_system": "YES",
                                }
                            },
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่าห้องยืนยันตัวตน",
                            description=f"ห้องได้ถูกอัพเดตเป็น {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_channel_id": channel.id,
                                "verification_system": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Verification channel",
                        description=f"channel have been set to {channel.mention}",
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verifychannel = server["verification_channel_id"]
                    if verifychannel == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "verification_channel_id": channel.id,
                                    "verification_system": "YES",
                                }
                            },
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification channel",
                            description=f"channel have been set to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "verification_channel_id": channel.id,
                                    "verification_system": "YES",
                                }
                            },
                        )

                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification channel",
                            description=f"channel have been updated to {channel.mention}",
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @setverify.error
    async def setverify_error(self, ctx: commands.Context, error):
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
                        title="ระบุห้องที่จะตั้ง",
                        description=f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องยืนยันตัวตน ``{settings.COMMAND_PREFIX}setverify #text-channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="คุณไม่มีสิทธิ์ตั้งค่าห้อง",
                        description=f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="Specify a channel",
                        description=f" ⚠️``{ctx.author}`` need to specify a channel ``{settings.COMMAND_PREFIX}setverify #text-channel``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="   You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def verification(self, ctx: commands.Context):
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

    @verification.error
    async def verification_error(self, ctx: commands.Context, error):
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

    @verification.command(aliases=["on"])
    @commands.has_permissions(administrator=True)
    async def verification_on(self, ctx: commands.Context):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"verification_system": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายืนยันตัวตน",
                        description=f"ได้ทําการเปิดใช้งานระบบนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verification_status = server["verification_system"]
                    if verification_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายืนยันตัวตน",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายืนยันตัวตน",
                            description=f"ได้ทําการเปิดใช้งานระบบนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "YES"

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"verification_system": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Verification system",
                        description=f"The level system have been activated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verification_status = server["verification_system"]
                    if verification_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification system",
                            description=f"The level system have been activated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @verification_on.error
    async def verification_on_error(self, ctx: commands.Context, error):
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

    @verification.command(aliases=["off"])
    @commands.has_permissions(administrator=True)
    async def verification_off(self, ctx: commands.Context):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"verification_system": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายืนยันตัวตน",
                        description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verification_status = server["verification_system"]
                    if verification_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายืนยันตัวตน",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายืนยันตัวตน",
                            description=f"ได้ทําการปิดใช้งานคําสั่งนี้",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                status = "NO"

                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {"$set": {"verification_system": status}},
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="Verification system",
                        description=f"The Verification system have been deactivated",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    verification_status = server["verification_system"]
                    if verification_status == "NO":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification system",
                            description=f"The Verification system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_system": status}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="Verification system",
                            description=f"The Verification system have been deactivated",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @verification_off.error
    async def verification_off_error(self, ctx: commands.Context, error):
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
    async def setverifytime(self, ctx: commands.Context, time: int):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                        colour=0x983925,
                    )

                    await ctx.send(embed=embed)

                else:
                    if 1 > time >= 120:
                        embed = nextcord.Embed(
                            colour=0x983925,
                            title=f"ตั้งค่าเวลา {time}",
                            description=f"⚠️ ``{ctx.author}`` คุณไม่สามารถตั้งเวลาเกิน 120 หรือน้อยกว่า 1 วินาทีได้ ",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("⚠️")

                    else:
                        verifychannel = server["verification_channel_id"]
                        status = server["verification_system"]
                        if verifychannel == "None" and status == "NO":
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                                colour=0x983925,
                            )

                            await ctx.send(embed=embed)

                        elif status == "NO":
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์นี้ปิดใช้งาน verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX} #channel",
                                colour=0x983925,
                            )

                            await ctx.send(embed=embed)

                        else:
                            await settings.collection.update_one(
                                {"guild_id": ctx.guild.id},
                                {"$set": {"verification_time": time}},
                            )

                            embed = nextcord.Embed(
                                colour=0x00FFFF,
                                title="ตั้งค่าเวลายืนยันตัวตน",
                                description=f"เวลายืนยันตัวตน {time}",
                            )

                            message = await ctx.send(embed=embed)
                            await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    embed = nextcord.Embed(
                        title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                        colour=0x983925,
                    )

                    await ctx.send(embed=embed)

                else:
                    if 1 > time >= 120:
                        embed = nextcord.Embed(
                            colour=0x983925,
                            title=f"ตั้งค่าเวลา {time}",
                            description=f"⚠️ ``{ctx.author}`` คุณไม่สามารถตั้งเวลาเกิน 120 หรือน้อยกว่า 1 วินาทีได้ ",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("⚠️")

                    else:
                        verifychannel = server["verification_channel_id"]
                        status = server["verification_system"]
                        if verifychannel == "None" and status == "NO":
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}setverify #channel",
                                colour=0x983925,
                            )

                            await ctx.send(embed=embed)

                        elif status == "NO":
                            embed = nextcord.Embed(
                                title=f"เซิฟเวอร์นี้ปิดใช้งาน verify",
                                description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX} #channel",
                                colour=0x983925,
                            )

                            await ctx.send(embed=embed)

                        else:
                            await settings.collection.update_one(
                                {"guild_id": ctx.guild.id},
                                {"$set": {"verification_time": time}},
                            )

                            embed = nextcord.Embed(
                                colour=0x00FFFF,
                                title="ตั้งค่าเวลายืนยันตัวตน",
                                description=f"เวลายืนยันตัวตน {time}",
                            )

                            message = await ctx.send(embed=embed)
                            await message.add_reaction("✅")

    @commands.group(invoke_without_command=True)
    async def verifyrole(self, ctx: commands.Context):
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
                    colour=0x00FFFF, description="คุณต้องระบุ give / remove"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

            else:
                embed = nextcord.Embed(
                    colour=0x00FFFF, description="you need to specify give / remove"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")

    @verifyrole.error
    async def verifyrole_error(self, ctx: commands.Context, error):
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

    @verifyrole.command(aliases=["give"])
    @commands.has_permissions(administrator=True)
    async def _give(self, ctx: commands.Context, role: nextcord.Role):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_role_give_id": role.id,
                                "verification_system": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                        description=f"ยศที่ได้ถูกตั้งเป็น {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    give_role_id = server["verification_role_give_id"]
                    if give_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                            description=f"ยศที่ได้ถูกตั้งเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                            description=f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_role_give_id": role.id,
                                "verification_system": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="role to give",
                        description=f"role to give after member verify have been set to {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    give_role_id = server["verification_role_give_id"]
                    if give_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to give",
                            description=f"role to give after member verify have been set to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_give_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to give",
                            description=f"role to give after member verify have been updated to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @_give.error
    async def verifygive_error(self, ctx: commands.Context, error):
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
                        title="ระบุยศที่จะให้หลังจากยืนยันตัวตน",
                        description=f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะให้หลังจากยืนยันตัวตน ``{settings.COMMAND_PREFIX}setrole give @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``admin`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="specify what role to remove",
                        description=f" ⚠️``{ctx.author}`` need to specify what role to give after verification``{settings.COMMAND_PREFIX}setrole give @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

    @verifyrole.command(aliases=["remove"])
    @commands.has_permissions(administrator=True)
    async def _remove(self, ctx: commands.Context, role: nextcord.Role):
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
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_role_remove_id": role.id,
                                "verification_system": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                        description=f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    remove_role_id = server["verification_role_remove_id"]
                    if remove_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                            description=f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                            description=f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

            if server_language == "English":
                server = await settings.collection.find_one({"guild_id": ctx.guild.id})
                if server is None:
                    newserver = await SetVerify.setnewserver(self, ctx)
                    await settings.collection.insert_one(newserver)
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "verification_role_remove_id": role.id,
                                "verification_system": "YES",
                            }
                        },
                    )
                    embed = nextcord.Embed(
                        colour=0x00FFFF,
                        title="role to remove",
                        description=f"role to remove after member verify have been set to {role.mention}",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")

                else:
                    remove_role_id = server["verification_role_remove_id"]
                    if remove_role_id == "None":
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to remove",
                            description=f"role to remove after member verify have been set to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                    else:
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {"$set": {"verification_role_remove_id": role.id}},
                        )
                        embed = nextcord.Embed(
                            colour=0x00FFFF,
                            title="role to remove",
                            description=f"role to remove after member verify have been updated to {role.mention}",
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

    @_remove.error
    async def verifyremove_error(self, ctx: commands.Context, error):
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
                        title="ระบุยศที่จะลบหลังจากยืนยันตัวตน",
                        description=f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะลบหลังจากยืนยันตัวตน ``{settings.COMMAND_PREFIX}setrole remove @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="You don't have permission",
                        description=f"⚠️ ``{ctx.author}`` You must have ``admin`` to be able to use this command",
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")

                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour=0x983925,
                        title="specify what role to remove",
                        description=f" ⚠️``{ctx.author}`` need to specify what role to remove after verification``{settings.COMMAND_PREFIX}setrole remove @role``",
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("⚠️")


def setup(bot: commands.Bot):
    bot.add_cog(SetVerify(bot))
