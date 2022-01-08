import nextcord
import settings
import random
import asyncio
from utils.languageembed import languageEmbed
from nextcord.ext import commands


class Economy(commands.Cog):

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(aliases=['openbal'])
    async def openbalance(self , ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            newbalance = {"guild_id": ctx.guild.id, "user_id":ctx.author.id,"bank":0 , "wallet":0}
                            await settings.collectionmoney.insert_one(newbalance)
                            embed = nextcord.Embed(
                                title = f"ทําบัญชีสําเร็จ",
                                description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}bal เพื่อดูเงินในบัญชี",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                        else:
                            embed = nextcord.Embed(
                                title = "มีบัญชีของคุณอยู่เเล้ว",
                                description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}bal เพื่อดูเงินในบัญชี",
                                colour = 0xB9E7A5
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
            
            if server_language == "English":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            newbalance = {"guild_id": ctx.guild.id, "user_id":ctx.author.id,"bank":0 , "wallet":0}
                            await settings.collectionmoney.insert_one(newbalance)
                            embed = nextcord.Embed(
                                title = f"Open balance",
                                description = f"Use {settings.COMMAND_PREFIX}bal to see your balance",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                        else:
                            embed = nextcord.Embed(
                                title = "You already have a balance",
                                description = f"Use {settings.COMMAND_PREFIX}bal to see your balance",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

                else:
                    embed = nextcord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @commands.command(aliases=['bal'])
    async def balance(self ,ctx, member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if not member is None:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":member.id})
                            if user is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                bank = user["bank"]
                            
                                embed = nextcord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"จำนวนเงินของ {member.name}", icon_url=f"{member.avatar.url}") 
                            
                                embed.add_field(name=f'เงินในธนาคาร', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'เงินทั้งหมด', value=f' ?? {currency}', inline = False)

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

                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        currency = guild["currency"]
                        status = guild["economy_system"]
                        if status == "YES":
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
                                bank = user["bank"]
                                wallet = user["wallet"]
                                total = bank + wallet
                            
                                embed = nextcord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"จำนวนเงินของ {ctx.author.name}", icon_url=f"{ctx.author.avatar.url}") 
                            
                                embed.add_field(name=f'เงินในธนาคาร', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'เงินในกระเป๋าตัง', value=f'{wallet} {currency}', inline = False)
                                embed.add_field(name=f'เงินทั้งหมด', value=f'{total} {currency}', inline = False)

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

            if server_language == "English":
                if not member is None:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":member.id})
                            if user is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                bank = user["bank"]
                            
                                embed = nextcord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"{member.name} balance", icon_url=f"{member.avatar.url}") 
                            
                                embed.add_field(name=f'Bank', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'Total money', value=f' ?? {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                                )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
                            if user is None:
                                embed = nextcord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                bank = user["bank"]
                                wallet = user["wallet"]
                                total = bank + wallet
                            
                                embed = nextcord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"{ctx.author.name} balance", icon_url=f"{ctx.author.avatar.url}") 
                            
                                embed.add_field(name=f'Bank', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'Wallet', value=f'{wallet} {currency}', inline = False)
                                embed.add_field(name=f'Total money', value=f'{total} {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')
        
    @commands.command()
    async def deposit(self,ctx, amount : int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if amount < 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')  
                    
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
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
                                current_wallet = user["wallet"]
                                new_bank = amount + user["bank"]
                                new_wallet = user["wallet"] - amount
                                if current_wallet >= amount:
                                    embed = nextcord.Embed(
                                        title = f"ฝากเงินเข้าบัญชีธนาคารสําเร็จ",
                                        description = f"ได้ทําการฝากเงินจํานวน {amount} {currency} เข้าธนาคาร",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
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
            
            if server_language == "English":
                if amount < 0:
                    embed = nextcord.Embed(
                        title = "Amount cannot be negative",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')  
                    
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
                            if user is None:
                                embed = nextcord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')

                            else:
                                current_wallet = user["wallet"]
                                new_bank = amount + user["bank"]
                                new_wallet = user["wallet"] - amount
                                if current_wallet >= amount:
                                    embed = nextcord.Embed(
                                        title = f"Deposit",
                                        description = f"Deposit {amount} {currency} to the bank",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = nextcord.Embed(
                                        title = "Not enough money in the wallet",
                                        description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                            
                    
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')      
                                
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

    @deposit.error
    async def deposit_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "จํานวนเงินที่จะฝากเข้าธนาคาร",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะฝากเข้าธนาคาร ``{settings.COMMAND_PREFIX}deposit (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "Amount of money to deposit",
                        description = f" ⚠️``{ctx.author}`` need to specify amount of money to deposit to the bank ``{settings.COMMAND_PREFIX}deposit (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def withdraw(self,ctx, amount : int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
        
            if server_language == "Thai":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')  
                    
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
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
                                user_bank = user["bank"]
                                new_bank = user["bank"] - amount
                                new_wallet = user["wallet"] + amount
                                if user_bank >= amount:
                                    embed = nextcord.Embed(
                                        title = f"ถอนเงินเสําเร็จ",
                                        description = f"ได้ทําการถอนเงินจํานวน {amount} {currency}",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
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

            if server_language == "English":
                if amount < 0:
                    embed = nextcord.Embed(
                        title = "Amount cannot be negative",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')    
                    
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
                            if user is None:
                                embed = nextcord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                            else:
                                user_bank = user["bank"]
                                new_bank = user["bank"] - amount
                                new_wallet = user["wallet"] + amount
                                if user_bank >= amount:
                                    embed = nextcord.Embed(
                                        title = f"Withdraw",
                                        description = f"Withdraw {amount} {currency} from the bank",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = nextcord.Embed(
                                        title = "Not enough money in the bank",
                                        description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                   
                    
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                                
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸') 

    @withdraw.error
    async def withdraw_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "จํานวนเงินที่จะถอนจากธนาคาร",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะถอนจากธนาคาร ``{settings.COMMAND_PREFIX}withdraw (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "Amount of money to withdraw",
                        description = f" ⚠️``{ctx.author}`` need to specify amount of money to withdraw from the bank ``{settings.COMMAND_PREFIX}withdraw (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addcredit(self,ctx ,amount : int , member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถตํ่ากว่าศูนย์",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivernew_bank = receiver["bank"] + amount

                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                embed = nextcord.Embed(
                                    title = f"โอนเงินสําเร็จ",
                                    description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                    colour = 0xB9E7A5
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
            
            if server_language == "English":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "Amount cannot be less than 0",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivernew_bank = receiver["bank"] + amount

                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                embed = nextcord.Embed(
                                    title = f"เพิ่มเงิน",
                                    description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                    colour = 0xB9E7A5
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')      
                    
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')      
                                
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

    @addcredit.error
    async def addcredit_error(self,ctx, error):
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
                        title = "คุณไม่มีสิทธิ์ให้ตัง",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )
                    
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️') 
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{settings.COMMAND_PREFIX}addcredit_error (amount) @member``"
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
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a member to add money``{settings.COMMAND_PREFIX}addcredit_error (amount) @member``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            

    @commands.command()
    async def pay(self,ctx ,amount : int , member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
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
                                user_bank = user["bank"]
                                usernew_bank = user["bank"] - amount

                                if user_bank >= amount:
                                    receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                                    if receiver is None:
                                        embed = nextcord.Embed(
                                            title = f"{member.name} ยังไม่มีบัญชี",
                                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')
                                
                                    else:
                                        receivernew_bank = receiver["bank"] + amount

                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":usernew_bank}})
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                        embed = nextcord.Embed(
                                            title = f"โอนเงินสําเร็จ",
                                            description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = nextcord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
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
            
            if server_language == "English":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
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
                                user_bank = user["bank"]
                                usernew_bank = user["bank"] - amount

                                if user_bank >= amount:
                                    receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                                    if receiver is None:
                                        embed = nextcord.Embed(
                                            title = f"{member.name} ยังไม่มีบัญชี",
                                            description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')
                                
                                    else:
                                        receivernew_bank = receiver["bank"] + amount

                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":usernew_bank}})
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                        embed = nextcord.Embed(
                                            title = f"โอนเงินสําเร็จ",
                                            description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = nextcord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
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

    @pay.error
    async def pay_error(self ,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{settings.COMMAND_PREFIX}addcredit_error (amount) @member``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a member to add money``{settings.COMMAND_PREFIX}addcredit_error (amount) @member``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def slot(self,ctx, amount:int):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
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
                                money  = user["wallet"]

                                if money >= amount:

                                    above = []
                                    middle = []
                                    below = []
                                    for i in range(3):
                                        a = random.choice(["🍒","🍍","🍇"])
                                        b = random.choice(["🍒","🍍","🍇"])
                                        c = random.choice(["🍒","🍍","🍇"])
                                        above.append(a)
                                        middle.append(b)
                                        below.append(c)

                                    result = (str(above[0] +"|"+ above[1] +"|"+ above[2])) + "\n" + (str(middle[0] +"|"+ middle[1] +"|"+ middle[2])+"⬅️") + "\n" + (str(below[0] +"|"+ below[1] +"|"+ below[2]))
                                    if ((middle[0] == middle[1] == middle[2])):
                                        prize = (amount * 3) - amount
                                        currentmoney = money + prize
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                        embed = nextcord.Embed(
                                            title = f"คุณได้เงินจำนวน {amount} {currency}",
                                            description = f"{result}",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar.url}") 
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                    else:
                                        currentmoney = money - amount
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                        embed = nextcord.Embed(
                                            title = f"คุณเสียเงินจำนวน {amount} {currency}",
                                            description = f"{result}",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar.url}") 
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = nextcord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
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

            if server_language == "English":
                if amount <= 0:
                    embed = nextcord.Embed(
                        title = "จํานวนเงินไม่สามารถติดลบได้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 
                
                else:
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        currency = guild["currency"]
                        if status == "YES":
                            user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
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
                                money  = user["wallet"]

                                if money >= amount:

                                    above = []
                                    middle = []
                                    below = []
                                    for i in range(3):
                                        a = random.choice(["🍒","🍍","🍇"])
                                        b = random.choice(["🍒","🍍","🍇"])
                                        c = random.choice(["🍒","🍍","🍇"])
                                        above.append(a)
                                        middle.append(b)
                                        below.append(c)

                                    result = (str(above[0] +"|"+ above[1] +"|"+ above[2])) + "\n" + (str(middle[0] +"|"+ middle[1] +"|"+ middle[2])+"⬅️") + "\n" + (str(below[0] +"|"+ below[1] +"|"+ below[2]))
                                    if ((middle[0] == middle[1] == middle[2])):
                                        prize = (amount * 3) - amount
                                        currentmoney = money + prize
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                        embed = nextcord.Embed(
                                            title = f"คุณได้เงินจำนวน {amount} {currency}",
                                            description = f"{result}",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar.url}") 
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                    else:
                                        currentmoney = money - amount
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                        embed = nextcord.Embed(
                                            title = f"คุณเสียเงินจำนวน {amount} {currency}",
                                            description = f"{result}",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar.url}") 
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = nextcord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
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

    @slot.error
    async def slot_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "จํานวนเงินที่จะลงพนัน",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะลงพนัน``{settings.COMMAND_PREFIX}slot (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "Amount of money to bet",
                        description = f" ⚠️``{ctx.author}`` need to specify amount of money to bet``{settings.COMMAND_PREFIX}slot (amount)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
            
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcurrency(self,ctx, *, currency):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = guild["economy_system"]
                    if status == "YES":
                        if not len(currency) > 100:
                            await settings.collection.update_one({"guild_id":ctx.guild.id},{"$set":{"currency":currency}})
                            embed = nextcord.Embed(
                                colour= 0x00FFFF,
                                title = "ตั้งค่าค่าเงิน",
                                description= f"ตั้ง ``{currency}`` เป็นค่าเงินสําเร็จ"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed)
                            await message.add_reaction('✅')

                        else:
                            embed = nextcord.Embed(
                                colour= 0x983925,
                                title = "ตั้งค่าค่าเงิน",
                                description= f"ไม่สามารถตั้ง ``{currency}`` เป็นค่าเงินเพราะยาวเกินไป"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed=embed)
                            await message.add_reaction('✅')
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

            if server_language == "English":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = guild["economy_system"]
                    if status == "YES":
                        if not len(currency) > 100:
                            await settings.collection.update_one({"guild_id":ctx.guild.id},{"$set":{"currency":currency}})
                            embed = nextcord.Embed(
                                colour= 0x00FFFF,
                                title = "set currency",
                                description= f"currency have been set to ``{currency}``"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed)
                            await message.add_reaction('✅')
                
                        else:
                            embed = nextcord.Embed(
                                colour= 0x983925,
                                title = "set currency",
                                description= f"unable to set ``{currency}`` as currency because it is too long"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")

                            message = await ctx.send(embed=embed)
                            await message.add_reaction('✅')
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

                else:
                    embed = nextcord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @setcurrency.error
    async def setcurrency_error(self,ctx, error):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "ค่าเงิน",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ค่าเงินที่จะเปลี่ยน ``{settings.COMMAND_PREFIX}setcurrency (currency)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "คุณไม่มีสิทธิ์เเอดมิน",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )
                    
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️') 
            
            if server_language == "English":
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "currency",
                        description = f" ⚠️``{ctx.author}`` need to specify a currency symbol to set ``{settings.COMMAND_PREFIX}setcurrency (currency)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                if isinstance(error, commands.MissingPermissions):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "You don't have permission",
                        description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

    @commands.command()
    async def rob(self,ctx , member: nextcord.Member):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
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
                            user_wallet = user["wallet"] 

                            taking = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if taking is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                                
                            else:
                                victimwallet = taking["wallet"] 

                                if victimwallet > 0:
                                    percent = (random.randint(1,101))
                                    if percent >= 30:
                                        percentmoney = (random.randint(60,101))
                                        stolen = (victimwallet * (percentmoney/100))
                                        stolen = round(stolen)
                                        victimnew_wallet = victimwallet - stolen
                                        stolernew_wallet = user_wallet + stolen
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":stolernew_wallet}})
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"wallet":victimnew_wallet}})
                                        embed = nextcord.Embed(
                                            title = f"ขโมยเงินจาก {member.name}",
                                            description = f"ขโมยเงินได้จํานวน {stolen} {currency}",
                                            colour = 0x00FFFF

                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')  

                                    else:
                                        reason = ["วิ่งหนีทัน","ไหวตัวทัน","วิ่งเร็วโครต","มีไหวพริบดี","รู้ตัวว่าจะโดนปล้น"]
                                        num = (random.randint(0,4))
                                        randomreason = reason[num]
                                        embed = nextcord.Embed(
                                            title = f"ปล้นเงินจาก {member.name} ไม่สําเร็จ",
                                            description = f"เพราะว่า {member.name} {randomreason}",
                                            colour = 0x983925

                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸') 

                                else:
                                    embed = nextcord.Embed(
                                        title = f"ปล้นเงินจาก {member.name} ไม่สําเร็จ",
                                        description = f"เพราะว่า {member.name} ไม่มีเงินในกระเป๋าตังสักบาท",
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

            if server_language == "English":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id,"user_id":ctx.author.id})
                        if user is None:
                            embed = nextcord.Embed(
                                title = f"{ctx.author.name} don't have a balance",
                                description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')
                            
                        else:
                            user_wallet = user["wallet"] 

                            taking = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if taking is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                                
                            else:
                                victimwallet = taking["wallet"]  

                                if victimwallet > 0:
                                    percent = (random.randint(1,101))
                                    if percent >= 30:
                                        percentmoney = (random.randint(60,101))
                                        stolen = (victimwallet * (percentmoney/100))
                                        stolen = round(stolen)
                                        victimnew_wallet = victimwallet - stolen
                                        stolernew_wallet = user_wallet + stolen
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":stolernew_wallet}})
                                        await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"wallet":victimnew_wallet}})
                                        embed = nextcord.Embed(
                                            title = f"rob from {member.name}",
                                            description = f"you have earned {stolen} {currency}",
                                            colour = 0x00FFFF

                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')  

                                    else:
                                        reason = ["run away","is aware","run too fast","know how to fight","fight back" , "there is a police nearby"]
                                        num = (random.randint(0,4))
                                        randomreason = reason[num]
                                        embed = nextcord.Embed(
                                            title = f"fail to rob {member.name}",
                                            description = f"reason : {member.name} {randomreason}",
                                            colour = 0x983925

                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸') 

                                else:
                                    embed = nextcord.Embed(
                                        title = f"fail to rob {member.name} ",
                                        description = f"reason : {member.name} have no money in his wallet",
                                        colour = 0x983925

                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸') 

                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')     
                                
                else:
                    embed = nextcord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @commands.command()
    async def work(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
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
                            user_wallet = user["wallet"] 
                            
                            money = (random.randint(1000,9500))
                            usernew_wallet = user_wallet + money
                            work = ["ล้างจาน","ถูพื้น","ขายตัว","ขับ taxi","ไปส่ง pizza","ขับ Grab"]
                            num = (random.randint(0,5))
                            ranwork = work[num]
                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":usernew_wallet}})
                            embed = nextcord.Embed(
                                title = f"",
                                description = f"{ctx.author} ได้ {ranwork} เเละได้รับเงิน {money}{currency}",
                                colour = 0xB9E7A5
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

            if server_language == "English":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            embed = nextcord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')
                        
                        else:
                            user_wallet = user["wallet"] 
                            
                            money = (random.randint(1000,9500))
                            usernew_wallet = user_wallet + money
                            work = ["Wash the dishes","Mop the floor","drive uber","deliver a pizza"]
                            num = (random.randint(0,5))
                            ranwork = work[num]
                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":usernew_wallet}})
                            embed = nextcord.Embed(
                                title = f"",
                                description = f"{ctx.author} have {ranwork} and earned {money}{currency}",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')     
                        
                else:
                    embed = nextcord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @commands.command()
    async def beg(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
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
                            user_wallet = user["wallet"] 
                            
                            money = (random.randint(500,2500))
                            usernew_wallet = user_wallet + money
                            work = "ขอทาน"
                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":usernew_wallet}})
                            embed = nextcord.Embed(
                                title = f"",
                                description = f"{ctx.author} ได้ {work} เเละได้รับเงิน {money}{currency}",
                                colour = 0xB9E7A5
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

            if server_language == "English":
                guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    currency = guild["currency"]
                    status = guild["economy_system"]
                    if status == "YES":
                        user = await settings.collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            embed = nextcord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')
                        
                        else:
                            user_wallet = user["wallet"] 
                            
                            money = (random.randint(500,2500))
                            usernew_wallet = user_wallet + money
                            work = "beg"
                            await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":usernew_wallet}})
                            embed = nextcord.Embed(
                                title = f"",
                                description = f"{ctx.author} have {work} and earned {money}{currency}",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')
                    else:
                        embed = nextcord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')     
                        
                else:
                    embed = nextcord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def resetmoney(self,ctx , member: nextcord.Member = None):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            server_language = languageserver["Language"]

            if server_language == "Thai":
                if member is None:
                    member = ctx.author

                try:
                    embed = nextcord.Embed(
                        colour = 0x00FFFF,
                        title = f"คุณเเน่ในที่จะ reset เงินของ {member.name}",
                        description = "พิม YES / NO")

                    embed.set_footer(text=":")
                    message = await ctx.send(embed=embed)

                    choice = await self.bot.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                    userchoice = choice.content
                    userchoice = userchoice.lower()
                    await asyncio.sleep(1) 
                    await choice.delete() 
                    await asyncio.sleep(1) 
                    await message.delete() 

                except asyncio.TimeoutError:
                    await message.delete()
                
                if userchoice == "yes":
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        if status == "YES":
                            receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivernew_bank = 0
                                receivernew_wallet = 0

                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank,"wallet":receivernew_wallet}})
                                embed = nextcord.Embed(
                                    title = f"reset เงิน",
                                    description = f"ได้ทําการ reset เงินของ {member.name}",
                                    colour = 0xB9E7A5
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

            if server_language == "English":  
                if member is None:
                    member = ctx.author
                try:
                    embed = nextcord.Embed(
                        colour = 0x00FFFF,
                        title = f"Are you sure you want to reset {ctx.author} money ?",
                        description = "type YES / NO")

                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)

                    choice = await self.bot.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                    userchoice = choice.content
                    userchoice = userchoice.lower()
                    await asyncio.sleep(1) 
                    await choice.delete() 
                    await asyncio.sleep(1) 
                    await message.delete() 

                except asyncio.TimeoutError:
                    await message.delete()
                
                if userchoice == "yes":
                    guild = await settings.collection.find_one({"guild_id":ctx.guild.id})
                    if not guild is None:
                        status = guild["economy_system"]
                        if status == "YES":
                            receiver = await settings.collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = nextcord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {settings.COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivernew_bank = 0
                                receivernew_wallet = 0

                                await settings.collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank,"wallet":receivernew_wallet}})
                                embed = nextcord.Embed(
                                    title = f"โอนเงินสําเร็จ",
                                    description = f"ได้ทําการ reset เงินของ {member.name}",
                                    colour = 0xB9E7A5
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')      
                    
                        else:
                            embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')     
                                
                    else:
                        embed = nextcord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {settings.COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

    @resetmoney.error
    async def resetmoney_error(self,ctx, error):
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
                        title = "คุณไม่มีสิทธิ์ให้ตัง",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )
                    
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️') 
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
                        description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{settings.COMMAND_PREFIX}resetmoney @member``"
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
                
                if isinstance(error, commands.MissingRequiredArgument):
                    embed = nextcord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify a member to reset money``{settings.COMMAND_PREFIX}resetmoney @member``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

def setup(bot: commands.Bot):
    bot.add_cog(Economy(bot))