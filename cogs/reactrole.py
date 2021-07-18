import discord
import settings
from utils.languageembed import languageEmbed
from discord.ext import commands


class ReactRole(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreactrole(self,ctx , emoji , role: discord.Role , * , text):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            if "//" in text:
                text = text.replace('//','\n')

            embed = discord.Embed(
                    colour = 0x00FFFF,
                    description = text
                )
            message = await ctx.send(embed=embed)
            await message.add_reaction(emoji)

            newrole = {"guild_id":ctx.guild.id,
            "emoji":emoji,
            "message_id":message.id,
            "message":text,
            "role_give_id":role.id,
            }
            await settings.collectionrole.insert_one(newrole)

    @setreactrole.error
    async def setreactrole_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "คุณไม่มีสิทธิ์ตั้งค่า",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

            
            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "You don't have permission",
                        description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

def setup(bot: commands.Bot):
    bot.add_cog(ReactRole(bot))