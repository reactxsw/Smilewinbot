import settings
import discord
from discord.ext import commands


class SetLanguage(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def setlanguage(self,ctx):
        embed = discord.Embed(
            colour = 0xFED000,
            description = "specify language / ต้องระบุภาษา : thai / english"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    @setlanguage.error
    async def setlanguage_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "You don't have permission \ คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"""
⚠️ ``{ctx.author.mention}``

English : You must have ``Administrator`` to be able to use this command
ไทย : ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"""
        )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    @setlanguage.command()
    @commands.has_permissions(administrator=True)
    async def thai(self,ctx):
        server = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if server is None:
            newserver = {"guild_id":ctx.guild.id,
            "Language":"Thai"
            }
            await settings.collectionlanguage.insert_one(newserver)
            embed = discord.Embed(
                colour= 0xFED000,
                title = "ตั้งค่าภาษา",
                description= f"ภาษาได้ถูกตั้งเป็น Thai"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        else:
            await settings.collectionlanguage.update_one({"guild_id":ctx.guild.id},{"$set":{"Language":"Thai"}})
            embed = discord.Embed(
                colour= 0xFED000,
                title = "ตั้งค่าภาษา",
                description= f"ภาษาได้ถูกอัพเดตเป็น Thai"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

    @thai.error
    async def thai_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "You don't have permission \ คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"""
⚠️ ``{ctx.author.mention}``

English : You must have ``Administrator`` to be able to use this command
ไทย : ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"""
        )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    @setlanguage.command()
    @commands.has_permissions(administrator=True)
    async def english(self,ctx):
        server = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if server is None:
            newserver = {"guild_id":ctx.guild.id,
            "Language":"English"
            }

            await settings.collectionlanguage.insert_one(newserver)
            embed = discord.Embed(
                colour= 0xFED000,
                title = "Language setting",
                description= f"Language have been set to English"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        else:
            await settings.collectionlanguage.update_one({"guild_id":ctx.guild.id},{"$set":{"Language":"English"}})
            embed = discord.Embed(
                colour= 0xFED000,
                title = "Language setting",
                description= f"Language have been set to English"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

    @english.error
    async def english_error(self,ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "You don't have permission \ คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"""
⚠️ ``{ctx.author.mention}``

English : You must have ``Administrator`` to be able to use this command
ไทย : ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"""
        )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')


def setup(bot: commands.Bot):
    bot.add_cog(SetLanguage(bot))
