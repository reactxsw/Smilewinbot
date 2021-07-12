import discord
from discord.ext import commands
import settings

class Level(commands.Cog): 

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self , message):
        await self.bot.wait_until_ready()
        if message.guild:
            if not message.content.startswith('/r'):
                guild_id = message.guild.id
                user_id = message.author.id
                channel = message.channel
                data = await settings.collection.find_one({"guild_id":guild_id})
                if data is None:
                    return
                
                else:
                    if message.author.bot:
                        return

                    else:
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
    
    @commands.command()
    async def rank(self , ctx , member : discord.Member=None):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]
            
            if server_language == "Thai":
                if member is None:
                    member = ctx.author

                data = await settings.collection.find_one( {"guild_id":ctx.guild.id})
                status = data["level_system"]
                if status != "NO":
                    user = await settings.collectionlevel.find_one({"user_id":ctx.author.id})
                    if user is None:
                        await ctx.send(f"เลเวลของ {member.mention} คือ 0")
                
                    else:
                        user_level = await settings.collectionlevel.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                        current_xp = user_level["xp"]
                        current_level = user_level["level"]
                        boxes = int((current_xp/(200*((1/2)*current_level)))*20)

                        rank = 0

                        level_ranking = settings.collectionlevel.find({"guild_id":member.guild.id}).sort("level",-1)
                        for ranking in await level_ranking.to_list(length =500000):
                            rank += 1
                            if ranking["user_id"] == member.id:
                                break

                        embed = discord.Embed(
                            title = f"เลเวลของ {member}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{member.name}",inline=True)
                        embed.add_field(name = "xp",value= f"{current_xp}/{int(200*((1/2)*current_level))}",inline=True)
                        embed.add_field(name = "เลเวล",value= f"{current_level}",inline=True)
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "ความคืบหน้า",value= boxes *":blue_square:"+(20-boxes)*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}level on เพื่อเปิดใช้",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

            if server_language == "English":
                if member is None:
                    member = ctx.author

                data = await settings.collection.find_one( {"guild_id":ctx.guild.id})
                status = data["level_system"]
                if status != "NO":
                    user = await settings.collectionlevel.find_one({"user_id":ctx.author.id})
                    if user is None:
                        await ctx.send(f"เลเวลของ {member.mention} คือ 0")
                
                    else:
                        user_level = await settings.collectionlevel.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                        current_xp = user_level["xp"]
                        current_level = user_level["level"]
                        boxes = int((current_xp/(200*((1/2)*current_level)))*20)

                        rank = 0

                        level_ranking = settings.collectionlevel.find({"guild_id":member.guild.id}).sort("level",-1)
                        for ranking in await level_ranking.to_list(length =500000):
                            rank += 1
                            if ranking["user_id"] == member.id:
                                break

                        embed = discord.Embed(
                            title = f"เลเวลของ {member}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{member.name}",inline=True)
                        embed.add_field(name = "xp",value= f"{current_xp}/{int(200*((1/2)*current_level))}",inline=True)
                        embed.add_field(name = "เลเวล",value= f"{current_level}",inline=True)
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "ความคืบหน้า",value= boxes *":blue_square:"+(20-boxes)*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}level on เพื่อเปิดใช้",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @commands.command()
    async def leaderboard(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            embed = discord.Embed(
                title = "Language setting / ตั้งค่าภาษา",
                description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            server = await settings.collection.find_one({"guild_id":ctx.guild.id})

            first = ["1"," - "," - "]
            second = ["2"," - "," - "]
            third = ["3"," - "," - "]
            fourth = ["4"," - "," - "]
            fifth = ["5"," - "," - "]
            sixth = ["6"," - "," - "]
            seventh = ["7"," - "," - "]
            eighth = ["8"," - "," - "]
            ninth = ["9"," - "," - "]
            tenth = ["10"," - "," - "]

            if server_language == "Thai":
                status = server["level_system"]
                if status != "NO":
                    ranking = settings.collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)

                    i = 1
                    for data in await ranking.to_list(length=500000):
                        try:
                            member =ctx.guild.get_member(data["user_id"])
                            member_lvl = data["level"]
                            if i == 1:
                                first[0] = (i)
                                first[1] = (member)
                                first[2] = (member_lvl)
                            
                            if i == 2:
                                second[0] = (i)
                                second[1] = (member)
                                second[2] = (member_lvl)
                            
                            if i == 3:
                                third[0] = (i)
                                third[1] = (member)
                                third[2] = (member_lvl)
                            
                            if i == 4:
                                fourth[0] = (i)
                                fourth[1] = (member)
                                fourth[2] = (member_lvl)
                            
                            if i == 5:
                                fifth[0] = (i)
                                fifth[1] = (member)
                                fifth[2] = (member_lvl)
                            
                            if i == 6:
                                sixth[0] = (i)
                                sixth[1] = (member)
                                sixth[2] = (member_lvl)
                            
                            if i == 7:
                                seventh[0] = (i)
                                seventh[1] = (member)
                                seventh[2] = (member_lvl)

                            if i == 8:
                                eighth[0] = (i)
                                eighth[1] = (member)
                                eighth[2] = (member_lvl)
                            
                            if i == 9:
                                ninth[0] = (i)
                                ninth[1] = (member)
                                ninth[2] = (member_lvl)
                            
                            if i == 10:
                                tenth[0] = (i)
                                tenth[1] = (member)
                                tenth[2] = (member_lvl)
                            
                            i = i + 1 

                        except IndexError:
                            break

                        if i == 11:
                            break
                    
                    description = f"""
> อันดับ {first[0]} : {first[1]} เลเวล :{first[2]}
> อันดับ {second[0]} : {second[1]} เลเวล :{second[2]}
> อันดับ {third[0]} : {third[1]} เลเวล :{third[2]}
> อันดับ {fourth[0]} : {fourth[1]} เลเวล :{fourth[2]}
> อันดับ {fifth[0]} : {fifth[1]} เลเวล :{fifth[2]}
> อันดับ {sixth[0]} : {sixth[1]} เลเวล :{sixth[2]}
> อันดับ {seventh[0]} : {seventh[1]} เลเวล :{seventh[2]}
> อันดับ {eighth[0]} : {eighth[1]} เลเวล :{eighth[2]}
> อันดับ {ninth[0]} : {ninth[1]} เลเวล :{ninth[2]}
> อันดับ {tenth[0]} : {tenth[1]} เลเวล :{tenth[2]}
"""
                    
                    embed = discord.Embed(
                        title="เเรงค์เลเวลในเซิฟเวอร์",
                        colour=0x00FFFF,
                        description = description
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                
                else:
                    embed = discord.Embed(
                            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}level on เพื่อเปิดใช้",
                            colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('❌')

        if server_language == "English":
                status = server["level_system"]
                if status != "NO":
                    ranking = settings.collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)

                    i = 1
                    for data in await ranking.to_list(length=500000):
                        try:
                            member =ctx.guild.get_member(data["user_id"])
                            member_lvl = data["level"]
                            if i == 1:
                                first[0] = (i)
                                first[1] = (member)
                                first[2] = (member_lvl)
                            
                            if i == 2:
                                second[0] = (i)
                                second[1] = (member)
                                second[2] = (member_lvl)
                            
                            if i == 3:
                                third[0] = (i)
                                third[1] = (member)
                                third[2] = (member_lvl)
                            
                            if i == 4:
                                fourth[0] = (i)
                                fourth[1] = (member)
                                fourth[2] = (member_lvl)
                            
                            if i == 5:
                                fifth[0] = (i)
                                fifth[1] = (member)
                                fifth[2] = (member_lvl)
                            
                            if i == 6:
                                sixth[0] = (i)
                                sixth[1] = (member)
                                sixth[2] = (member_lvl)
                            
                            if i == 7:
                                seventh[0] = (i)
                                seventh[1] = (member)
                                seventh[2] = (member_lvl)

                            if i == 8:
                                eighth[0] = (i)
                                eighth[1] = (member)
                                eighth[2] = (member_lvl)
                            
                            if i == 9:
                                ninth[0] = (i)
                                ninth[1] = (member)
                                ninth[2] = (member_lvl)
                            
                            if i == 10:
                                tenth[0] = (i)
                                tenth[1] = (member)
                                tenth[2] = (member_lvl)
                            
                            i = i + 1 

                        except IndexError:
                            break

                        if i == 11:
                            break
                    
                    description = f"""
> อันดับ {first[0]} : {first[1]} เลเวล :{first[2]}
> อันดับ {second[0]} : {second[1]} เลเวล :{second[2]}
> อันดับ {third[0]} : {third[1]} เลเวล :{third[2]}
> อันดับ {fourth[0]} : {fourth[1]} เลเวล :{fourth[2]}
> อันดับ {fifth[0]} : {fifth[1]} เลเวล :{fifth[2]}
> อันดับ {sixth[0]} : {sixth[1]} เลเวล :{sixth[2]}
> อันดับ {seventh[0]} : {seventh[1]} เลเวล :{seventh[2]}
> อันดับ {eighth[0]} : {eighth[1]} เลเวล :{eighth[2]}
> อันดับ {ninth[0]} : {ninth[1]} เลเวล :{ninth[2]}
> อันดับ {tenth[0]} : {tenth[1]} เลเวล :{tenth[2]}
"""                    
                    embed = discord.Embed(
                        title="เเรงค์เลเวลในเซิฟเวอร์",
                        colour=0x00FFFF,
                        description = description
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                
                else:
                    embed = discord.Embed(
                            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}level on เพื่อเปิดใช้",
                            colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('❌')

def setup(bot: commands.Bot):
    bot.add_cog(Level(bot))
