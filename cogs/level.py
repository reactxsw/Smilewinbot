import nextcord
from nextcord.ext import commands
from utils.languageembed import languageEmbed
import settings
import requests

class Level(commands.Cog): 

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
    
    @commands.command()
    async def rank(self , ctx , member : nextcord.Member=None):
        language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
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

                        embed = nextcord.Embed(
                            title = f"เลเวลของ {member}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{member.name}")
                        embed.add_field(name = "xp",value= f"{current_xp}/{int(200*((1/2)*current_level))}")
                        embed.add_field(name = "เลเวล",value= f"{current_level}")
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}")
                        embed.add_field(name = "ความคืบหน้า",value= boxes *":blue_square:"+(20-boxes)*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = nextcord.Embed(
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

                        embed = nextcord.Embed(
                            title = f"เลเวลของ {member}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{member.name}")
                        embed.add_field(name = "xp",value= f"{current_xp}/{int(200*((1/2)*current_level))}")
                        embed.add_field(name = "เลเวล",value= f"{current_level}")
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}")
                        embed.add_field(name = "ความคืบหน้า",value= boxes *":blue_square:"+(20-boxes)*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = nextcord.Embed(
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
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
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
                    
                    embed = nextcord.Embed(
                        title="เเรงค์เลเวลในเซิฟเวอร์",
                        colour=0x00FFFF,
                        description = description
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                
                else:
                    embed = nextcord.Embed(
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
                    embed = nextcord.Embed(
                        title="เเรงค์เลเวลในเซิฟเวอร์",
                        colour=0x00FFFF,
                        description = description
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                
                else:
                    embed = nextcord.Embed(
                            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}level on เพื่อเปิดใช้",
                            colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('❌')

def setup(bot: commands.Bot):
    bot.add_cog(Level(bot))
