import discord
import random
import asyncio
import settings
from discord.ext import commands


class Game(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def rps(self,ctx):
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

            if server_language == "Thai":
                embed = discord.Embed(
                    colour =0x00FFFF,
                    title = "เกมเป่ายิ้งฉุบ"
                )

                embed.set_image(url = 'https://i.imgur.com/ZvX4DrC.gif')
                embed.set_footer(text=f"⏳ กดที่ emoji ภายใน10วินาที")
                message = await ctx.send(embed=embed)
                await message.add_reaction('✊')
                await message.add_reaction('✋')
                await message.add_reaction('✌️')

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

                    if str(reaction.emoji) == "✊":
                        #rock , paper , scissor
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        #rock , paper , scissor
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        #rock , paper , scissor
                        answer = "scissor"

                    responses = ['https://i.imgur.com/hdG222Q.jpg', 'https://i.imgur.com/O3ZLDRr.jpg' ,'https://i.imgur.com/dZOVJ4r.jpg']
                    botresponse = random.choice(responses)

                    if botresponse == "https://i.imgur.com/hdG222Q.jpg":
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😮 คุณเสมอ"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😄 คุณชนะ"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😭 คุณเเพ้"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")
                            await message.edit(embed=embed)

                    elif botresponse == "https://i.imgur.com/O3ZLDRr.jpg":
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😭 คุณเเพ้"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😮 คุณเสมอ"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😄 คุณชนะ"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")
                            await message.edit(embed=embed)
                    
                    else:
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😄 คุณชนะ"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😭 คุณเเพ้"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "เกมเป่ายิ้งฉุบ",
                            description = "😮 คุณเสมอ"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")
                            await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "🕑 หมดเวลา" ,
                    )

                    embed.set_image(url ="https://i.imgur.com/bBMSqvf.jpg")

                    await message.edit(embed=embed)

            if server_language == "English":
                embed = discord.Embed(
                    colour =0x00FFFF,
                    title = "เกมเป่ายิ้งฉุบ"
                )

                embed.set_image(url = 'https://i.imgur.com/ZvX4DrC.gif')
                embed.set_footer(text=f"⏳ click on emoji in 10 seconds")
                message = await ctx.send(embed=embed)
                await message.add_reaction('✊')
                await message.add_reaction('✋')
                await message.add_reaction('✌️')

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

                    if str(reaction.emoji) == "✊":
                        #rock , paper , scissor
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        #rock , paper , scissor
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        #rock , paper , scissor
                        answer = "scissor"

                    responses = ['https://i.imgur.com/hdG222Q.jpg', 'https://i.imgur.com/O3ZLDRr.jpg' ,'https://i.imgur.com/dZOVJ4r.jpg']
                    botresponse = random.choice(responses)

                    if botresponse == "https://i.imgur.com/hdG222Q.jpg":
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😮 Draw"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😄 You won"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😭 You lose"
                            )
                            embed.set_image(url="https://i.imgur.com/hdG222Q.jpg")
                            await message.edit(embed=embed)

                    elif botresponse == "https://i.imgur.com/O3ZLDRr.jpg":
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😭 You lose"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😮 Draw"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😄 You won"
                            )
                            embed.set_image(url="https://i.imgur.com/O3ZLDRr.jpg")
                            await message.edit(embed=embed)
                    
                    else:
                        if answer == "rock":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😄 You won"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")

                            await message.edit(embed=embed)

                        elif answer == "paper":
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😭 You lose"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")
                            await message.edit(embed=embed)
                        
                        else:
                            embed = discord.Embed(
                            colour = 0x00FFFF,
                            title = "Rock paper scissor",
                            description = "😮 Draw"
                            )
                            embed.set_image(url="https://i.imgur.com/dZOVJ4r.jpg")
                            await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "🕑 Out of time" ,
                    )

                    embed.set_image(url ="https://i.imgur.com/bBMSqvf.jpg")

                    await message.edit(embed=embed)

    @commands.command(aliases=['coin','flipcoin'])
    async def coinflip(self,ctx):
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
            responses = ['https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png']
            flip = random.choice(responses)
            
            if server_language == "Thai":

                if flip == "https://i.imgur.com/Jeeym59.png":
                    embed = discord.Embed(
                        colour =0x00FFFF,
                        title = "ทอยเหรียญ",
                        description = f"คุณ ``{ctx.author}`` ทอยได้ก้อย"
                
                    )
                    embed.set_image(url="https://i.imgur.com/Jeeym59.png")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)
        
                if flip == "https://i.imgur.com/Pq8ntth.png":
                    embed = discord.Embed(
                        colour =0x00FFFF,
                        title = "ทอยเหรียญ",
                        description = f"คุณ ``{ctx.author}`` ทอยได้หัว"
                
                    )

                    embed.set_image(url="https://i.imgur.com/Pq8ntth.png")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)

            if server_language == "English":

                if flip == "https://i.imgur.com/Jeeym59.png":
                    embed = discord.Embed(
                        colour =0x00FFFF,
                        title = "Coin flip",
                        description = f"คุณ ``{ctx.author}`` got tail"
                
                    )
                    embed.set_image(url="https://i.imgur.com/Jeeym59.png")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)
        
                if flip == "https://i.imgur.com/Pq8ntth.png":
                    embed = discord.Embed(
                        colour =0x00FFFF,
                        title = "Coin flip",
                        description = f"``{ctx.author}`` got head"
                
                    )

                    embed.set_image(url="https://i.imgur.com/Pq8ntth.png")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))