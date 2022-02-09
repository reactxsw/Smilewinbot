import asyncio
import nextcord
import random
import numpy
import settings
from utils.languageembed import languageEmbed
from nextcord.ext import commands

async def getlastestoutcome(guild):
    data = await settings.collectiongamble.find_one({"guild_id":guild})
    if data is None:
        arr = []
        for data in [random.randint(0, 37) for i in range(10)]:
            if data == 0:
                arr.append(3)
            
            elif 0 < data < 19:
                arr.append(1)
            
            elif data > 18:
                arr.append(0)
        await settings.collectiongamble.insert_one({"guild_id":guild,"previous":arr})
        return arr

    else:
        return data["previous"]

async def checkwin(colour):
    num = random.randint(0, 37)
    if num == 0:
        outcome = 3
    
    elif 0 < num < 19:
        outcome = 1
    
    elif num > 18:
        outcome = 0
    
    dic ={
        3 : "green",
        1 : "black",
        0 : "red"
    }
    if colour == "green" and outcome == 0:
        return "win","green",3
    
    elif colour == "black" and outcome == 1:
        return "win","black",1
    
    elif colour == "red" and outcome == 2:
        return "win","red",0
    
    else:
        return "lose", dic[outcome], outcome


class Gamble(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command()
    async def cockfight(self,ctx):
        pass

    @commands.group()
    async def roulette(self,ctx):
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
                        lastest = await getlastestoutcome(ctx.guild.id)
                        lastest = "".join(["🟢" if i == 3 else "⚫" if i == 1 else "🔴" for i in lastest])
                        embed = nextcord.Embed(
                            title = "รูเล็ต | Roulette",
                            description= f"ผล Roulette ล่าสุด \n```{lastest}```",
                            colour = 0xFED000
                        )
                        embed.add_field(name=f"{settings.COMMAND_PREFIX}roulette green [จํานวน]",value="ลงพนัน รูเล็ตสีเขียว \n`(ได้เงิน 5x หากชนะ)`")
                        embed.add_field(name=f"{settings.COMMAND_PREFIX}roulette red [จํานวน]",value="ลงพนัน รูเล็ตสีเเดง \n`(ได้เงิน 2x หากชนะ)`")
                        embed.add_field(name=f"{settings.COMMAND_PREFIX}roulette black [จํานวน]",value="ลงพนัน รูเล็ตสีดํา \n`(ได้เงิน 2x หากชนะ)`")
                        embed.add_field(name="📢หมายเหตุ",value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""", inline=False)
                        await ctx.send(embed=embed)

    @roulette.command()
    async def green(self,ctx,amount:int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            data = await settings.collection.find_one({"guild_id":ctx.guild.id})
            if not data is None:
                if data["economy_system"] == "YES":
                    roulette = await settings.collectiongamble.find_one({"guild_id":ctx.guild.id})
                    if roulette is None:
                        await getlastestoutcome(ctx.guild.id)
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
                        if current >= amount:
                            result, colour,outcome =await checkwin("green")
                            await settings.collectiongamble.update_one({"guild_id": ctx.guild.id}, {'$pop': {'previous': -1}}) 
                            await settings.collectiongamble.update_one({"guild_id":ctx.guild.id}, {'$push': {'previous': outcome}})
                            if result == "win":
                                newwallet = amount*5 + current
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":newwallet}})
                                embed= nextcord.Embed(
                                    title="คุณชนะ",
                                    description=f"พนัน green จํานวน{amount}{currency} \nได้รับเงินรางวัล{amount*5}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
                            else:
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":current-amount}})
                                embed= nextcord.Embed(
                                    title="คุณเเพ้ !",
                                    description=f"สีที่ออก {colour}\nพนัน green จํานวน{amount}{currency} \nเสียเงิน{amount}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
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

    @roulette.command()
    async def red(self,ctx,amount:int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            data = await settings.collection.find_one({"guild_id":ctx.guild.id})
            if not data is None:
                if data["economy_system"] == "YES":
                    roulette = await settings.collectiongamble.find_one({"guild_id":ctx.guild.id})
                    if roulette is None:
                        await getlastestoutcome(ctx.guild.id)
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
                        if current >= amount:
                            result, colour,outcome =await checkwin("red")
                            await settings.collectiongamble.update_one({"guild_id": ctx.guild.id}, {'$pop': {'previous': -1}}) 
                            await settings.collectiongamble.update_one({"guild_id":ctx.guild.id}, {'$push': {'previous': outcome}})
                            if result == "win":
                                newwallet = amount*2 + current
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":newwallet}})
                                embed= nextcord.Embed(
                                    title="คุณชนะ",
                                    description=f"พนัน red จํานวน{amount}{currency} \nได้รับเงินรางวัล{amount*2}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
                            else:
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":current-amount}})
                                embed= nextcord.Embed(
                                    title="คุณเเพ้ !",
                                    description=f"สีที่ออก {colour}\nพนัน red จํานวน{amount}{currency} \nเสียเงิน{amount}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
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

    @roulette.command()
    async def black(self,ctx,amount:int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            data = await settings.collection.find_one({"guild_id":ctx.guild.id})
            if not data is None:
                if data["economy_system"] == "YES":
                    roulette = await settings.collectiongamble.find_one({"guild_id":ctx.guild.id})
                    if roulette is None:
                        await getlastestoutcome(ctx.guild.id)
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
                        if current >= amount:
                            result, colour,outcome =await checkwin("black")
                            await settings.collectiongamble.update_one({"guild_id": ctx.guild.id}, {'$pop': {'previous': -1}}) 
                            await settings.collectiongamble.update_one({"guild_id":ctx.guild.id}, {'$push': {'previous': outcome}})
                            if result == "win":
                                newwallet = amount*2 + current
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":newwallet}})
                                embed= nextcord.Embed(
                                    title="คุณชนะ",
                                    description=f"พนัน black จํานวน{amount}{currency} \nได้รับเงินรางวัล{amount*2}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
                            else:
                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":current-amount}})
                                embed= nextcord.Embed(
                                    title="คุณเเพ้ !",
                                    description=f"สีที่ออก {colour}\nพนัน black จํานวน{amount}{currency} \nเสียเงิน{amount}{currency}",
                                    color=0xfed000
                                )
                                await ctx.send(embed=embed)
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