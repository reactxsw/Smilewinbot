import nextcord
from nextcord.embeds import Embed
import settings
from utils.languageembed import languageEmbed
from nextcord.ext import commands


class ReactRole(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreactrole(self,ctx , emoji , role: nextcord.Role , * , text):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:

            if role >= ctx.guild.me.top_role:
                embed = nextcord.Embed(
                    title = "ไม่มีสิทธ์",
                    description = "ยศของบอทจะต้องสูงกว่ายศที่จะให้สมาชิก ตัวอย่างตามรูปด้านล่าง",
                    colour =  0x983925,
                )
                embed.set_footer(text="ข้อความนี้จะถูกลบอัตโนมัติภายใน 15วินาที")
                embed.set_image(url="https://i.imgur.com/4Nmh9Ml.png")
                await ctx.send(embed = embed , delete_after=15)
            else:
                if "//" in text:
                    text = text.replace('//','\n')

                embed = nextcord.Embed(
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
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "คุณไม่มีสิทธิ์ตั้งค่า",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

            
            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "You don't have permission",
                        description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

def setup(bot: commands.Bot):
    bot.add_cog(ReactRole(bot))
