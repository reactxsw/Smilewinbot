from importlib import reload
import discord
from discord.ext import commands
import settings
from cogs.scam import check_scam_link
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)

class on_message_event(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        await self.bot.wait_until_ready()
        data = await settings.collection.find_one({"guild_id":message.guild.id})
        if message.guild:
            if message.channel.id == data["Music_channel_id"]:
                embed_message = await self.bot.get_channel(data["Music_channel_id"]).fetch_message(data["Embed_message_id"])
                embed=discord.Embed(description="[❯ Invite](https://smilewindiscord-th.web.app/invitebot.html) | [❯ Website](https://smilewindiscord-th.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                    colour = 0xffff00)
                embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar_url)
                embed.set_image(url ="https://i.imgur.com/XwFF4l6.png")
                embed.set_footer(text=f"server : {message.guild.name}")
                await embed_message.edit(embed=embed, components=[
                [
                    Button(label="⏯",style=ButtonStyle.green,custom_id="pause_stop"),
                    Button(label="⏭",style=ButtonStyle.gray,custom_id="skip"),
                    Button(label="⏹",style=ButtonStyle.red ,custom_id="stop"),
                    Button(label="🔂",style=ButtonStyle.gray ,custom_id="repeat"),
                    Button(label="🔁",style=ButtonStyle.gray ,custom_id="loop"),
                    ],

                [
                    Button(label="🔊 เพิ่มเสียง",style=ButtonStyle.blue ,custom_id="decrease_volume"),
                    Button(label="🔈 ลดเสียง",style=ButtonStyle.blue ,custom_id="increase_volume"),
                    Button(label="🔇 เปิด/ปิดเสียง",style=ButtonStyle.blue ,custom_id="mute_volume")    
                    ]
                ])

            if message.content.startswith('!r'):
                return
            
            else:
                await check_scam_link(message)
                if not message.author.bot:
                    guild_id = message.guild.id
                    user_id = message.author.id
                    channel = message.channel
                    data = await settings.collection.find_one({"guild_id":guild_id})
                    if not data is None:
                        status = data["level_system"]
                        if status == "YES":
                            user = await settings.collectionlevel.find_one({"user_id":user_id, "guild_id":guild_id})
                            if user is None:
                                new_user = {"guild_id": message.guild.id, "user_id":user_id,"xp":0 , "level":1}
                                await settings.collectionlevel.insert_one(new_user)

                            else:
                                user = await settings.collectionlevel.find_one({"user_id":user_id, "guild_id":guild_id})
                                current_xp = user["xp"]
                                current_level = user["level"]
                                new_xp = user["xp"] + 10
                                need_xp = ((50*(current_level**2))+(50*current_level))
                                if new_xp > need_xp:
                                    current_level = current_level + 1
                                    current_xp = current_xp - need_xp
                                    await settings.collectionlevel.update_one({"guild_id":guild_id , "user_id":user_id},{"$set":{"xp":current_xp, "level":current_level}})
                                    await channel.send(f"{message.author.mention} ได้เลเวลอัพเป็น เลเวล {current_level}")
                                
                                else:
                                    pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

def setup(bot):
    bot.add_cog(on_message_event(bot))
