from aiohttp.helpers import ProxyInfo
import discord
from discord.ext import commands
import aiohttp
import asyncio
import re
import requests
import settings
from utils.languageembed import languageEmbed
import bson
import json

with open("data/developer_id.txt") as developerid:
    developerid = developerid.read()
    developerid = developerid.splitlines()
    developerid = [int(i) for i in developerid]

async def get_domain_name_from_url(url):
    return url.split("//")[-1].split("/")[0]

with open("data/phishing.txt") as f:
    phishing = [x.strip() for x in f.readlines()] 

async def get_link_bypassing(url):
    return requests.Session().head(url,allow_redirects=True).url

async def get_mode(guild_id):
    #if server setting have scam in it, then check is scam mode is warn or delete
    server_setting = await settings.collection.find_one({"guild_id":guild_id})
    if server_setting is None:
        await settings.collection.insert_one({"guild_id":guild_id,"scam":"warn"})
        return "warn"
    else:
        if "scam" in server_setting:
            return server_setting["scam"]
        else:
            await settings.collection.update_one({"guild_id":guild_id}, {"$set":{"scam":"warn"}})
            return "warn"

async def check_scam_link(message):
    server_lang = await settings.collectionlanguage.find_one({"guild_id":message.guild.id})
    if server_lang is None:
        server_lang = "English"
    else:
        server_lang = server_lang["Language"]
    link = re.search("(?P<url>https?://[^\s]+)", message.content)
    mode = await get_mode(message.guild.id)

    if link != None:
        link = link.group("url")
        if "bit.ly" in link:
            url = await get_link_bypassing(link)
            domain = await get_domain_name_from_url(url)
        else:
            domain = await get_domain_name_from_url(link)
        if domain in phishing:
            if mode == "warn":
                if server_lang == "Thai":
                    await message.channel.send(f"{message.author.mention} โปรดอย่าส่งลิ้งค์ที่ไม่น่าเชื่อถือ")
                elif server_lang == "English":
                    await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
            elif mode == "delete":
                await message.delete()
                if server_lang == "Thai":
                    await message.channel.send(f"{message.author.mention} โปรดอย่าส่งลิ้งค์ที่ไม่น่าเชื่อถือ")
                elif server_lang == "English":
                    await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
            
    else:
        for content in message.content.split():
            if content in phishing:
                if mode == "warn":
                    await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
                elif mode == "delete":
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Please do not send a scam link here.")
class Scam(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def scam(self,ctx):
        languageserver = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        
        else:
            languageserver = languageserver["language"]
            if languageserver == "Thai":
                embed = discord.Embed(
                    title = "ข้อมูลเกี่ยวคำสั่ง scam",
                    colour = 0xFED000,
                )
                embed.add_field(name="Add",value="`scam add [link]`")
                embed.add_field(name="Remove",value="`scam remove [link]`")
                embed.add_field(name="📢หมายเหตุ",value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""", Inline=False)
            elif languageserver == "English":
                embed = discord.Embed(
                    title = "Scam command information",
                    colour = 0xFED000,
                )
                embed.add_field(name="Add",value="`scam add [link]`")
                embed.add_field(name="Remove",value="`scam remove [link]`")
                embed.add_field(name="📢Note",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""", Inline=False)


    @scam.command()
    async def mode(self,ctx,mode1):
        languageserver = await get_server_lang(ctx)
        if languageserver == "Thai":
            if mode1 == "warn":
                await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"warn"}})
                await ctx.send(f"{ctx.author.mention} ตั้งโหมดเป็นตักเตือนแล้ว")
            elif mode1 == "delete":
                await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"delete"}})
                await ctx.send(f"{ctx.author.mention} ตั้งโหมดเป็นลบทันทีแล้ว")
            
            else:
                await ctx.send(f"{ctx.author.mention} กรุณาใช้ `{settings.COMMAND_PREFIX} scam mode [warn/delete]`")
        
        if languageserver == "English":
            if mode1 == "warn":
                await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"warn"}})
                await ctx.send(f"{ctx.author.mention} Set mode to warn")
            elif mode1 == "delete":
                await settings.collection.update_one({"guild_id":ctx.guild.id},{'$set':{"scam":"delete"}})
                await ctx.send(f"{ctx.author.mention} Set mode to delete")

            else:
                await ctx.send(f"{ctx.author.mention} Please use `{settings.COMMAND_PREFIX} scam mode [warn/delete]`")

    @scam.command()
    async def add(self,ctx,link=None):
        server_lang = await get_server_lang(ctx)
        link= await get_domain_name_from_url(link)
        if server_lang == "Thai":
            if link != None:
                #check is the link is in data/scram_link.json
                if link in phishing:
                    await ctx.send(f"{ctx.author.mention} มีลิ้งค์นี้ในระบบแล้ว")
                    return

                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                newdata = {"category": "add", "link": link, "author":str(ctx.author), "author_id": ctx.author.id, "id": str(bson.objectid.ObjectId())}
                data.append(newdata)

                with open("data/request_approve.json","w") as f:
                    json.dump(data,f, indent=2)

                for dev in developerid:
                    user = await self.bot.fetch_user(dev)
                    text = await text_beautifier(f"New add scam link request from {str(ctx.author)}\nData : {json.dumps(newdata, indent=2)}")
                    await user.send(text)
                
                await ctx.send(f"{ctx.author.mention} ส่งคำขอเพิ่มลิ้งสำเร็จ")
            else:
                await ctx.send(f"{ctx.author.mention} กรุณาใช้ `{settings.COMMAND_PREFIX} scam add [link]`")
        
        elif server_lang == "English":
            if link != None:
                #check is the link is in data/scram_link.json
                if link in phishing:
                    await ctx.send(f"{ctx.author.mention} The link is already in the database")
                    return

                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                id = str(bson.objectid.ObjectId())
                newdata = {"category": "add", "link": link, "author":str(ctx.author), "author_id": ctx.author.id, "id": id}
                data.append(newdata)

                with open("data/request_approve.json","w") as f:
                    json.dump(data,f, indent=2)
                
                for dev in developerid:
                    user = await self.bot.fetch_user(dev)
                    text = await text_beautifier(f"New add scam link request from {str(ctx.author)}\nData : {json.dumps(newdata, indent=2)}")
                    await user.send(text)
                
                await ctx.send(f"{ctx.author.mention} Request add link success")
                await ctx.author.send(f"Your request add link has been sent to developer\nTo cancel your request, use `{settings.COMMAND_PREFIX} scam cancel {id}`")
            else:
                await ctx.send(f"{ctx.author.mention} Please use `{settings.COMMAND_PREFIX} scam add [link]`")


            


    @scam.command()
    async def remove(self,ctx,link=None):
        server_lang = await get_server_lang(ctx)
        link = await get_domain_name_from_url(link)
        if server_lang == "Thai":
            if link != None:
                #check is the link is in data/scram_link.json
                if link not in phishing:
                    await ctx.send(f"{ctx.author.mention} ไม่มีลิ้งค์นี้ในระบบ")
                    return
                
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                newdata = {"category": "remove", "link": link, "author":str(ctx.author), "author_id": ctx.author.id, "id": str(bson.objectid.ObjectId())}
                data.append(newdata)

                with open("data/request_approve.json","w") as f:
                    json.dump(data,f, indent=2)

                for dev in developerid:
                    user = await self.bot.fetch_user(dev)
                    text = await text_beautifier(f"New remove scam link request from {str(ctx.author)}\nData : {json.dumps(newdata, indent=2)}")
                    await user.send(text)

                await ctx.send(f"{ctx.author.mention} ส่งคำขอลบลิ้งสำเร็จ")
            else:
                await ctx.send(f"{ctx.author.mention} กรุณาใช้ `{settings.COMMAND_PREFIX} scam remove [link]`")
        
        elif server_lang == "English":
            if link != None:
                #check is the link is in data/scram_link.json
                if link not in phishing:
                    await ctx.send(f"{ctx.author.mention} The link is not in the database")
                    return

                
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                id = str(bson.objectid.ObjectId())
                newdata = {"category": "remove", "link": link, "author":str(ctx.author), "author_id": ctx.author.id, "id": id}
                data.append(newdata)

                with open("data/request_approve.json","w") as f:
                    json.dump(data,f, indent=2)

                for dev in developerid:
                    user = await self.bot.fetch_user(dev)
                    text = await text_beautifier(f"New remove scam link request from {str(ctx.author)}\nData : {json.dumps(newdata, indent=2)}")
                    await user.send(text)
                    
                
                await ctx.send(f"{ctx.author.mention} Request remove link success")
                await ctx.author.send(f"Your request remove link has been sent to developer\nTo cancel your request, use `{settings.COMMAND_PREFIX} scam cancel {id}`")
            else:
                await ctx.send(f"{ctx.author.mention} Please use `{settings.COMMAND_PREFIX} scam remove [link]`")
        
    @scam.command(aliases=["request_list"])
    async def list(self,ctx):
        server_lang = await get_server_lang(ctx)
        if server_lang == "Thai":
            if ctx.author.id in developerid:
                await ctx.send(f"{ctx.author.mention} ส่งไปที่แชทส่วนตัวแล้ว!!!.")
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                text = await text_beautifier(f"The list of all requests\n{json.dumps(data, indent=2)}")
                await ctx.author.send(text)
            else:
                await ctx.send("คุณไม่มีสิทธิ์ใช้คำสั่งนี้")
            
        elif server_lang == "English":
            if ctx.author.id in developerid:
                await ctx.send(f"{ctx.author.mention} I have sent it to you DM!!!.")
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                text = await text_beautifier(f"The list of all requests\n{json.dumps(data, indent=2)}")
                await ctx.author.send(text)
            else:
                await ctx.send("You don't have permission to use this command")
    
    @scam.command()
    async def approve(self,ctx,id):
        server_lang = await get_server_lang(ctx)
        if server_lang == "Thai":
            if ctx.author.id in developerid:
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                for i in data:
                    if i["id"] == id:
                        if i["category"] == "add":
                            
                            phishing.append(i["link"])
                            phishing.sort()
                            
                            with open("data/phishing.txt","w") as f:
                                f.write("\n".join(phishing))
                            
                            await ctx.send(f"{ctx.author.mention} อนุมัติคำขอเพิ่มลิ้งสำเร็จ")
                        
                            data.remove(i)
                            with open("data/request_approve.json","w") as f:
                                json.dump(data,f, indent=2)
                            break
                        elif i["category"] == "remove":
                            for j in phishing:
                                if j == i["link"]:
                                    phishing.remove(j)
                                    phishing.sort()
                                    with open("data/phishing.txt","w") as f:
                                        f.write("\n".join(phishing))
                                    break
                            await ctx.send(f"{ctx.author.mention} อนุมัติคำขอลบลิ้งสำเร็จ")
                            data.remove(i)
                            with open("data/request_approve.json","w") as f:
                                json.dump(data,f, indent=2)
                            break
                for dev_user_id in developerid:
                        user = await self.bot.fetch_user(dev_user_id)
                        text = await text_beautifier(f"{str(ctx.author)} has approved the request from {i['author']}\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                        await user.send(text)
            else:
                await ctx.send("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้")
        elif server_lang == "English":
            if ctx.author.id in developerid:
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                for i in data:
                    if i["id"] == id:
                        if i["category"] == "add":
                            
                            phishing.append(i["link"])
                            phishing.sort()
                            with open("data/phishing.txt","w") as f:
                                f.write("\n".join(phishing))
                            
                            await ctx.send(f"{ctx.author.mention} Approve add link success")
                            data.remove(i)
                            with open("data/request_approve.json","w") as f:
                                json.dump(data,f, indent=2)
                            break
                        elif i["category"] == "remove":
                            
                            for j in phishing:
                                if j == i["link"]:
                                    phishing.remove(j)
                                    phishing.sort()
                                    with open("data/phishing.txt","w") as f:
                                        f.write("\n".join(phishing))
                                    break
                            await ctx.send(f"{ctx.author.mention} Approve remove link success")
                            
                            data.remove(i)
                            with open("data/request_approve.json","w") as f:
                                json.dump(data,f, indent=2)
                            break
                
                for dev_user_id in developerid:
                    user = await self.bot.fetch_user(dev_user_id)
                    text = await text_beautifier(f"{str(ctx.author)} has approved the request from {i['author']}\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                    await user.send(text)
                                
            else:
                await ctx.send("You don't have permission to use this command")
    
    @scam.command()
    async def disapprove(self,ctx,id):
        server_lang = await get_server_lang(ctx)
        if server_lang == "Thai":
            if ctx.author.id in developerid:
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                for i in data:
                    if i["id"] == id:
                        await ctx.send(f"{ctx.author.mention} ปฏิเสธคำขอแล้ว")
                        data.remove(i)
                        with open("data/request_approve.json","w") as f:
                            json.dump(data,f, indent=2)
                        break
                for dev_user_id in developerid:
                    user = await self.bot.fetch_user(dev_user_id)
                    text = await text_beautifier(f"{str(ctx.author)} has disapproved the request from {i['author']}\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                    await user.send(text)
            else:
                await ctx.send("คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้")
        elif server_lang == "English":
            if ctx.author.id in developerid:
                with open("data/request_approve.json","r") as f:
                    data = json.load(f)
                
                for i in data:
                    if i["id"] == id:
                        await ctx.send(f"{ctx.author.mention} Approve add link success")
                        data.remove(i)
                        with open("data/request_approve.json","w") as f:
                            json.dump(data,f, indent=2)
                        break
                
                for dev_user_id in developerid:
                    user = await self.bot.fetch_user(dev_user_id)
                    text = await text_beautifier(f"{str(ctx.author)} has approved the request from {i['author']}\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                    await user.send(text)
            else:
                await ctx.send("You don't have permission to use this command")
    
    @scam.command()
    async def cancel(self,ctx,id):
        server_lang = await get_server_lang(ctx)
        if server_lang == "Thai":
            with open("data/request_approve.json","r") as f:
                data = json.load(f)
            
            for i in data:
                if i["id"] == id:
                    await ctx.send(f"{ctx.author.mention} ยกเลิกคำขอแล้ว")
                    data.remove(i)
                    with open("data/request_approve.json","w") as f:
                        json.dump(data,f, indent=2)
                    break
            
            for dev_user_id in developerid:
                user = await self.bot.fetch_user(dev_user_id)
                text = await text_beautifier(f"{str(ctx.author)} has canceled his request.\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                await user.send(text)

        elif server_lang == "English":
            with open("data/request_approve.json","r") as f:
                data = json.load(f)

            for i in data:
                if i["id"] == id:
                    await ctx.send("Cancel request success")
                    data.remove(i)
                    with open("data/request_approve.json","w") as f:
                        json.dump(data,f, indent=2)
                    break
            
            for dev_user_id in developerid:
                user = await self.bot.fetch_user(dev_user_id)
                text = await text_beautifier(f"{str(ctx.author)} has canceled his request.\nid : {i['id']}\ncategory : {i['category']}\nlink : {i['link']}")
                await user.send(text)

                

async def get_server_lang(ctx,mode="ctx"):
    server_lang = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server_lang is None:
        message = await ctx.send(embed=languageEmbed.languageembed(ctx))
        await message.add_reaction('👍')
        return None
    
    return server_lang["Language"]

async def text_beautifier(text):
    start_end = "-"*50
    result = start_end + "\n" + text + "\n" + start_end
    return result

def setup(bot):
    bot.add_cog(Scam(bot))