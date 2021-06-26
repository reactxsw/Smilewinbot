import settings
import discord
import traceback
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        channel = self.bot.get_channel(id = int(settings.supportchannel))
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            pass

        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.CommandNotFound):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️ไม่มีคําสั่งนี้กรุณาเช็คการสะกดคําว่าถูกหรือผิด"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                elif isinstance(error, commands.BotMissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️บอทไม่มีสิทธิ คุณต้องให้สิทธิเเอดมินกับบอทก่อนใช้คําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")    
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                
                else:
                    await channel.send(traceback.format_exc())
                    await channel.send(error)

            
            if server_language == "English":
                if isinstance(error, commands.CommandNotFound):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️ Command not found"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                
                elif isinstance(error, commands.BotMissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️Bot don't have enough permission to do that please give administrator permission to the bot"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                
                else:
                    await channel.send(traceback.format_exc())
                    await channel.send(error)

def setup(bot: commands.Bot):
    bot.add_cog(Error(bot))