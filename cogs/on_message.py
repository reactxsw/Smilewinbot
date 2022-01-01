from importlib import reload
import discord
from discord.ext import commands
import settings
from cogs.scam import check_scam_link

class on_message_event(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        await self.bot.wait_until_ready()
        await check_scam_link(message)
        if message.guild:
            if message.author.bot:
                return
            
            else:
                if not message.content.startswith('!r'):
                    guild_id = message.guild.id
                    user_id = message.author.id
                    channel = message.channel
                    data = await settings.collection.find_one({"guild_id":guild_id})
                    if not data is None:
                        if not message.author.bot:
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
