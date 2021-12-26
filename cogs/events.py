from typing import Text
import discord
import datetime
from discord import user
import settings
from discord.ext import commands


class Events(commands.Cog): 

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload): 
        await self.bot.wait_until_ready()
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if message.author == self.bot.user:
            data = await settings.collectionrole.find_one({"guild_id":payload.guild_id,"message_id":message.id})
            if not data is None:
                emoji = data["emoji"]
                role = data["role_give_id"]
                if str(payload.emoji) == str(emoji):
                    role = data["role_give_id"]
                    role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id = role)
                    if role and payload.member != self.bot.user:
                        await payload.member.add_roles(role)
                
                else:
                    await message.remove_reaction(payload.emoji, payload.member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        await self.bot.wait_until_ready()
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if message.author == self.bot.user:
            data = await settings.collectionrole.find_one({"guild_id":payload.guild_id,"message_id":message.id})
            if data is None:
                pass

            else:
                emoji = data["emoji"]
                role = data["role_give_id"]
                if str(payload.emoji) == str(emoji):
                    member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                    if role in [role.id for role in member.roles]:
                        role = data["role_give_id"]
                        role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, id = role)
                        await member.remove_roles(role)
                    
                    else:
                        pass

                else:
                    pass

        else:
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        await self.bot.wait_until_ready()
        languageserver = await settings.collectionlanguage.find_one({"guild_id":member.guild.id})
        if not languageserver is None:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    logchannel = data["log_channel_id"]
                    logstatus = data["log_voice_system"]
                    if not logchannel == "None":
                        channel = self.bot.get_channel(id = int(logchannel))
                        if channel:
                            if logstatus == "YES":
                                if before.channel is None:
                                    embed = discord.Embed(
                                        colour = 0x56FF2D,
                                        description = f"🢂 ``Joined voice channel`` {after.channel} :loud_sound:"
                                    )
                                    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
                                    embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                    embed.timestamp = datetime.datetime.utcnow()
                                    await channel.send(embed=embed)
                                
                                elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                                        embed = discord.Embed(
                                            colour = 0x00FFFF,
                                            description = f"🢆 ``Moved from`` {before.channel} :loud_sound: to {after.channel} :loud_sound:"
                                        )
                                        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}") 
                                        embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                        embed.timestamp = datetime.datetime.utcnow()
                                        await channel.send(embed=embed)
                                
                                elif before.channel == after.channel:
                                    pass
                                
                                else:
                                    embed = discord.Embed(
                                        colour = 0x983925,
                                        description = f"🢀``Left voice channel`` {before.channel} :loud_sound:"
                                    )
                                    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}") 
                                    embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                    embed.timestamp = datetime.datetime.utcnow()
                                    await channel.send(embed=embed)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass        
                
            if server_language == "English":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    logchannel = data["log_channel_id"]
                    logstatus = data["log_voice_system"]
                    if not logchannel == "None":
                        channel = self.bot.get_channel(id = int(logchannel))
                        if channel:
                            if logstatus == "YES":
                                if before.channel is None:
                                    embed = discord.Embed(
                                        colour = 0x56FF2D,
                                        description = f"🢂 ``Joined voice channel`` {after.channel} :loud_sound:"
                                    )
                                    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
                                    embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                    embed.timestamp = datetime.datetime.utcnow()
                                    await channel.send(embed=embed)
                                
                                elif before.channel is not None and after.channel is not None and before.channel != after.channel:
                                    embed = discord.Embed(
                                        colour = 0x00FFFF,
                                        description = f"🢆 ``Moved from`` {before.channel} :loud_sound: to {after.channel} :loud_sound:"
                                    )
                                    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}") 
                                    embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                    embed.timestamp = datetime.datetime.utcnow()
                                    await channel.send(embed=embed)

                                elif before.channel == after.channel:
                                    pass

                                
                                else:
                                    embed = discord.Embed(
                                        colour = 0x983925,
                                        description = f"🢀``Left voice channel`` {before.channel} :loud_sound:"
                                    )
                                    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}") 
                                    embed.set_footer(text=f"{member}" + f"  ⮞ ")
                                    embed.timestamp = datetime.datetime.utcnow()
                                    await channel.send(embed=embed)
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

    @commands.Cog.listener()
    async def on_member_join(self,member):
        await self.bot.wait_until_ready()
        languageserver = await settings.collectionlanguage.find_one({"guild_id":member.guild.id})
        if not languageserver is None:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    welcome = data["welcome_id"] 
                    if not welcome == "None":
                        channel = self.bot.get_channel(id = int(welcome))
                        if channel:
                            embed = discord.Embed(
                                colour = 0x99e68b,
                                title =f'ยินดีต้อนรับเข้าสู่ {member.guild.name}',
                                description = 'กรุณาอ่านกฏเเละเคารพกันเเละกันด้วยนะครับ'
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            channel = self.bot.get_channel(id = int(welcome))
                            await channel.send(embed=embed)
                    
                    else:
                        return
    
            if server_language == "English":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    welcome = data["welcome_id"] 
                    if not welcome == "None":
                        channel = self.bot.get_channel(id = int(welcome))
                        if channel:
                            embed = discord.Embed(
                                    colour = 0x99e68b,
                                    title =f'Welcome to {member.guild.name}',
                                    description = 'Please read and follow our rules'
                                )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()
                            
                            channel = self.bot.get_channel(id = int(welcome))
                            await channel.send(embed=embed)
                    
                    else:
                        return

        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        await self.bot.wait_until_ready()
        languageserver = await settings.collectionlanguage.find_one({"guild_id":member.guild.id})
        if not languageserver is None:
            server_language = languageserver["Language"]
            
            if server_language == "Thai":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    welcome = data["leave_id"] 
                    if not welcome == "None":
                        channel = self.bot.get_channel(id = int(data["leave_id"]))
                        if channel:
                            embed = discord.Embed(
                                colour=0x983925, 
                                title = "Member leave",
                                description= f"{member.name}ได้ออกจากเซิฟเวอร์"
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            channel = self.bot.get_channel(id = int(data["leave_id"]))
                            await channel.send(embed=embed)
                    else:
                        return
            
            if server_language == "English":
                data = await settings.collection.find_one({"guild_id":member.guild.id})
                if not data is None:
                    welcome = data["leave_id"] 
                    if not welcome == "None":
                        channel = self.bot.get_channel(id = int(data["leave_id"]))
                        if channel:
                            embed = discord.Embed(
                                colour=0x983925, 
                                title = "Member leave",
                                description= f"{member.name} have left the server"
                                )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()
 
                            channel = self.bot.get_channel(id = int(data["leave_id"]))
                            await channel.send(embed=embed)

                    else:
                        return
        
        else:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(id = int(settings.logchannel))
        embed = discord.Embed(
            title = f"Bot have joined a new server {guild.name} with {guild.member_count} members",
            colour = 0x00FFFF
        )
        await channel.send(embed=embed)
        try:
            async for entry in guild.audit_logs(limit= 1 ,action=discord.AuditLogAction.bot_add):
                uembed = discord.Embed(
                                    colour = 0x00FFFF,
                                    description =
f"""สวัสดีครับ {entry.user.name}
ขอบคุณที่เชิญบอท{self.bot.user.name} เข้าร่วมเซิร์ฟเวอร์ {entry.user.mention}

เว็บไซต์บอท : [Smilewin](https://smilewindiscord-th.web.app/)


                                    """) 
                uembed.add_field(name="🤝Partner : ",value=f"[allzone](https://allzone.online/)")
                await entry.user.send(embed=uembed)
        
        except discord.Forbidden:
            pass

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"🙏 สวัสดีครับเซิฟเวอร์ / Hello {guild.name}",
                    description = f"""
                    พิม ``{settings.COMMAND_PREFIX}help`` เพื่อดูคําสั่งของบอท
                    Support : https://discord.com/invite/R8RYXyB4Cg

                    use ``{settings.COMMAND_PREFIX}help`` to view bot commands
                    support : https://discord.com/invite/R8RYXyB4Cg

                    """

                )
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='┗Powered by REACT')

                message = await channel.send(embed=embed)
                await message.add_reaction('🙏')
                print(f"Bot have joined a new server {guild.name} with {guild.member_count} members")

            break

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(id = int(settings.logchannel))
        embed = discord.Embed(
            title = f"Bot have left {guild.name}",
            colour = 0x983925
        )  
        await channel.send(embed=embed)
        print(f"Bot have left {guild.name}")

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
