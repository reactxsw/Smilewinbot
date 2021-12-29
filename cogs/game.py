import discord
import random
import asyncio
import settings
from utils.languageembed import languageEmbed
from discord.ext import commands


class Game(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def rps(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                embed = discord.Embed(
                    colour =0xFED000,
                    title = "เกมเป่ายิ้งฉุบ"
                )

                embed.set_image(url = 'https://i.imgur.com/09sTceV.gif')
                embed.set_footer(text=f"⏳ กดที่ emoji ภายใน10วินาที")
                message = await ctx.send(embed=embed)
                await message.add_reaction('✊')
                await message.add_reaction('✋')
                await message.add_reaction('✌️')

                answer = "none"
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

                    if str(reaction.emoji) == "✊":
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        answer = "scissor"

                    rps = ['https://i.imgur.com/zkxuAGQ.png', 'https://i.imgur.com/paMpgkb.png' ,'https://i.imgur.com/aNkWXXy.png']
                    responses = {
                        "https://i.imgur.com/zkxuAGQ.png":{
                            "rock":"😮 เสมอ",
                            "paper":"😄 คุณชนะ",
                            "scissor":"😭 คุณเเพ้"
                        },
                        "https://i.imgur.com/paMpgkb.png":{
                            "rock":"😭 คุณเเพ้",
                            "paper":"😮 คุณเสมอ",
                            "scissor":"😄 คุณชนะ"
                        }
                        ,
                        "https://i.imgur.com/aNkWXXy.png":{
                            "rock":"😄 คุณชนะ",
                            "paper":"😭 คุณเเพ้",
                            "scissor":"😮 คุณเสมอ"
                        }
                    }
                    botresponse = random.choice(rps)
                    embed = discord.Embed(
                        colour = 0xFED000,
                        title = "Rock paper scissor",
                        description = responses[botresponse][answer]
                    )
                    embed.set_image(url=botresponse)
                    await message.edit(embed=embed)
                
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "🕑 หมดเวลา" ,
                    )

                    embed.set_image(url ="https://i.imgur.com/9mQV5cF.jpg")

                    await message.edit(embed=embed)



            if server_language == "English":
                embed = discord.Embed(
                    colour =0xFED000,
                    title = "เกมเป่ายิ้งฉุบ"
                )

                embed.set_image(url = 'https://i.imgur.com/09sTceV.gif')
                embed.set_footer(text=f"⏳ click on emoji in 10 seconds")
                message = await ctx.send(embed=embed)
                await message.add_reaction('✊')
                await message.add_reaction('✋')
                await message.add_reaction('✌️')
                answer = "none"
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

                    if str(reaction.emoji) == "✊":
                        answer = "rock"
                    if str(reaction.emoji) == "✋":
                        answer = "paper"
                    if str(reaction.emoji) == "✌️":
                        answer = "scissor"

                    rps = ['https://i.imgur.com/zkxuAGQ.png', 'https://i.imgur.com/paMpgkb.png' ,'https://i.imgur.com/aNkWXXy.png']
                    responses = {
                        "https://i.imgur.com/zkxuAGQ.png":{
                            "rock":"😮 Draw",
                            "paper":"😄 You won",
                            "scissor":"😭 You lose"
                        },
                        "https://i.imgur.com/paMpgkb.png":{
                            "rock":"😭 You lose",
                            "paper":"😮 Draw",
                            "scissor":"😄 You won"
                        }
                        ,
                        "https://i.imgur.com/aNkWXXy.png":{
                            "rock":"😄 You won",
                            "paper":"😭 You lose",
                            "scissor":"😮 Draw"
                        }
                    }
                    botresponse = random.choice(rps)
                    embed = discord.Embed(
                        colour = 0xFED000,
                        title = "Rock paper scissor",
                        description = responses[botresponse][answer]
                    )
                    embed.set_image(url=botresponse)
                    await message.edit(embed=embed)

                except asyncio.TimeoutError:
                    
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "🕑 Out of time" ,
                    )

                    embed.set_image(url ="https://i.imgur.com/9mQV5cF.jpg")

                    await message.edit(embed=embed)

    @commands.command(aliases=['coin','flipcoin'])
    async def coinflip(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            responses = ['https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png']
            flip = random.choice(responses)
            
            if server_language == "Thai":

                if flip == responses[0]:
                    embed = discord.Embed(
                        colour =0xFED000,
                        title = "ทอยเหรียญ",
                        description = f"คุณ ``{ctx.author}`` ทอยได้ก้อย"
                
                    )
                    embed.set_image(url=responses[0])
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)
        
                if flip == responses[1]:
                    embed = discord.Embed(
                        colour =0xFED000,
                        title = "ทอยเหรียญ",
                        description = f"คุณ ``{ctx.author}`` ทอยได้หัว"
                
                    )

                    embed.set_image(url=responses[1])
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)

            if server_language == "English":

                if flip == responses[0]:
                    embed = discord.Embed(
                        colour =0xFED000,
                        title = "Coin flip",
                        description = f"คุณ ``{ctx.author}`` got tail"
                
                    )
                    embed.set_image(url=responses[0])
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)
        
                if flip == responses[1]:
                    embed = discord.Embed(
                        colour =0xFED000,
                        title = "Coin flip",
                        description = f"``{ctx.author}`` got head"
                
                    )

                    embed.set_image(url=responses[1])
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))