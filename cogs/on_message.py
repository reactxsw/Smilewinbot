from async_timeout import asyncio
import nextcord
from nextcord.ext import commands
from numpy import array
import settings
from cogs.scam import check_scam_link
from cogs.music import Music


class on_message_event(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        await self.bot.wait_until_ready()
        if message.guild:
            data = await settings.collection.find_one({"guild_id": message.guild.id})
            if data != None:
                if message.guild and not message.author.bot:
                    if message.channel.id == data["Music_channel_id"]:

                        ctx: commands.Context = await self.bot.get_context(message)
                        bot_voice_client : nextcord.VoiceClient = nextcord.utils.get(
                            self.bot.voice_clients, guild=ctx.guild
                        )
                        if (bot_voice_client is None or (bot_voice_client is not None and ctx.author.voice.channel.id == bot_voice_client.channel.id)):
                            if message.attachments != []:
                                files = []
                                for items in range (len(message.attachments)):
                                    print(message.attachments[items].url)
                                    files.append(message.attachments[items].url)
                                
                                print(files)
                                for file in files:
                                    await ctx.invoke(self.bot.get_command("play"), search=file)
                            
                            else:
                                if settings.COMMAND_PREFIX in message.content:
                                    song = message.content.split(settings.COMMAND_PREFIX)[1]

                                else:
                                    song = message.content
                                
                                await ctx.invoke(self.bot.get_command("play"), search=song)

                            await asyncio.sleep(1)
                            await message.delete()

                        else:
                            await asyncio.sleep(1)
                            await message.delete()
                            embed = nextcord.Embed(
                                title="คุณจะต้องอยู่ในห้องเดียวกับบอทถึงจะสามรถสั่งเพลงได้",
                                description=f"{message.author.mention} บอทเล่นเพลงอยู่ที่ {bot_voice_client.channel.mention}",
                                color=0xFED000,
                            )
                            await message.channel.send(embed=embed, delete_after=5)

                if message.content.startswith("!r"):
                    return

                else:
                    await check_scam_link(message)
                    if not message.author.bot:
                        guild_id = message.guild.id
                        user_id = message.author.id
                        channel = message.channel
                        data = await settings.collection.find_one(
                            {"guild_id": guild_id}
                        )
                        if not data is None:
                            status = data["level_system"]
                            if status == "YES":
                                user = await settings.collectionlevel.find_one(
                                    {"user_id": user_id, "guild_id": guild_id}
                                )
                                if user is None:
                                    new_user = {
                                        "guild_id": message.guild.id,
                                        "user_id": user_id,
                                        "xp": 0,
                                        "level": 1,
                                    }
                                    await settings.collectionlevel.insert_one(new_user)

                                else:
                                    user = await settings.collectionlevel.find_one(
                                        {"user_id": user_id, "guild_id": guild_id}
                                    )
                                    current_xp = user["xp"]
                                    current_level = user["level"]
                                    new_xp = user["xp"] + 10
                                    need_xp = (50 * (current_level**2)) + (
                                        50 * current_level
                                    )
                                    if new_xp > need_xp:
                                        current_level = current_level + 1
                                        current_xp = current_xp - need_xp
                                        await settings.collectionlevel.update_one(
                                            {"guild_id": guild_id, "user_id": user_id},
                                            {
                                                "$set": {
                                                    "xp": current_xp,
                                                    "level": current_level,
                                                }
                                            },
                                        )
                                        await channel.send(
                                            f"{message.author.mention} ได้เลเวลอัพเป็น เลเวล {current_level}"
                                        )
def setup(bot):
    bot.add_cog(on_message_event(bot))
