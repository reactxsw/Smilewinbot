import asyncio
import nextcord
import random
import settings
from utils.languageembed import languageEmbed
from nextcord.ext import commands

class Gamble(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def cockfight(self,ctx):
        pass

    @commands.command()
    async def roulette(self,ctx , colour , amount:int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            data = await settings.collection.find_one({"guild_id":ctx.guild.id})
            if not data is None:
                if data["economy_system"] == "YES":
                    user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                    if user is None:
                        embed = nextcord.Embed(
                            title = f"{ctx.author.name} ยังไม่มีบัญชี",
                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')
                    
                    else:
        pass

    @commands.command()
    async def horse(self,ctx , horse : int , money : int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            data = await settings.collection.find_one({"guild_id":ctx.guild.id})
            if not data is None:
                if data["economy_system"] == "YES":
                    user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                    if user is None:
                        embed = nextcord.Embed(
                            title = f"{ctx.author.name} ยังไม่มีบัญชี",
                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')
                    
                    else:
                        current = user["wallet"]
                        currency = data["currency"]
                        if current >= money:
                            run = True
                            board = [(random.randint(3,7)) for i in range(5)]
                            for i in range(5):
                                board.append(random.randint(3,7))

                            render = "".join([(f"**🏁"+"- "*board[j] + f"🏇{j+1}.**\n") for j in range(5)])
                            embed = nextcord.Embed(
                                title= f"**Horse : {horse}**\n**Bet : {money} {currency}**",
                                colour=0xFED000,
                                description=render
                            )
                            embed.set_footer(text=ctx.author)
                            race = await ctx.send(embed=embed)
                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":current - money}})
                            while run:
                                await asyncio.sleep(0.6)
                                render = "".join([(f"**🏁"+"- "*board[j] + f"🏇{j+1}.**\n") for j in range(5)])
                                embed = nextcord.Embed(
                                    title= f"**Horse : {horse}**\n**Bet : {money}  {currency}**",
                                    colour=0xFED000,
                                    description=render
                                )
                                embed.set_footer(text=ctx.author)
                                await race.edit(embed=embed)
                                x = random.randint(1,4)
                                g = [(random.randint(0,4)) for i in range(x)]
                                for d in g:
                                    board[d] = board[d]-1
                                    if board[d] == 0:
                                        render = "".join([(f"**🏁"+"- "*board[j] + f"🏇{j+1}.**\n") for j in range(5)])
                                        if d == horse-1:
                                            embed = nextcord.Embed(
                                                title= f"คุณชนะ !",
                                                colour=0xFED000,
                                                description=f"ได้รับเงิน {money*5} {currency}\n{render}"
                                            )
                                            embed.set_footer(text=ctx.author)
                                            await race.edit(embed=embed)
                                            current = current + money*6
                                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":current}})
                                        
                                        else:
                                            embed = nextcord.Embed(
                                                title= f"คุณเเพ้ !",
                                                colour=0xFED000,
                                                description=f"เสียเงิน {money} {currency}\n{render}"
                                                
                                            )
                                            embed.set_footer(text=ctx.author)
                                            await race.edit(embed=embed)
                                        run = False
                                        break
                        else:
                            embed = nextcord.Embed(
                                title = "จํานวนเงินในกระเป๋าตังไม่พอ",
                                description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')  
                else:
                    embed = nextcord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')  
            else:
                embed = nextcord.Embed(
                    title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                    description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')  

def setup(bot: commands.Bot):
    bot.add_cog(Gamble(bot))