#import
import discord , asyncio , datetime , itertools , os , praw , requests , random , urllib , aiohttp , bs4 ,json ,humanize , time , platform , re ,sqlite3 , pymongo , json , httplib2 , psutil , subprocess
import DiscordUtils
#from
from typing import Text
from PIL import Image, ImageDraw , ImageFont
from discord.channel import StoreChannel
from discord import Webhook , RequestsWebhookAdapter
from discord.ext import commands, tasks
from discord.utils import get
from datetime import date, timedelta
from itertools import cycle
from bs4 import BeautifulSoup,element
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlencode
from captcha.image import ImageCaptcha
from threading import Thread
from pymongo import MongoClient
from pathlib import Path
from googleapiclient.discovery import build

os.system("title Smilewin#0644")
if Path("config.json").exists():
    with open('config.json') as setting:
        config = json.load(setting)

    TOKEN = config.get("bot_token")
    COMMAND_PREFIX = config.get("bot_prefix")
    openweathermapAPI = config.get("openweathermap_api")
    reddit = praw.Reddit(
        client_id=config.get("reddit_client_id"),
        client_secret=config.get("reddit_client_secret"),
        username=config.get("reddit_username"),
        password=config.get("reddit_password"),
        user_agent=config.get("reddit_user_agent")
    )
    mongodb = config.get("connect_mongodb")
    trackerapi = config.get("tracker.gg_api")
    pastebinapi = config.get("pastebin_api_dev_key")
    supportchannel = config.get("support_channel")
    youtubeapi = config.get("youtube_api")

else: 
    with open("config.json", "w") as setting:
        setting.writelines(
            [
                "{",
                    "\n",
                    "    "+'"bot_token": "_____________________________________",',
                    "\n",
                    "    "+'"bot_prefix": "_____________________________________",',
                    "\n",
                    "    "+'"connect_mongodb": "_____________________________________",',
                    "\n",
                    "    "+'"support_channel": "_____________________________________",',
                    "\n",
                    "\n",
                    "    "+'"openweathermap_api": "_____________________________________",',
                    "\n",
                    "    "+'"tracker.gg_api": "_____________________________________",',
                    "\n",
                    "\n",
                    "    "+'"reddit_client_id": "_____________________________________",',
                    "\n",
                    "    "+'"reddit_client_secret": "_____________________________________",',
                    "\n",
                    "    "+'"reddit_username": "_____________________________________",',
                    "\n",
                    "    "+'"reddit_password":"_____________________________________",',
                    "\n",
                    "    "+'"reddit_user_agent": "_____________________________________",',
                    "\n",
                    "\n",
                    "    "+'"pastebin_api_dev_key": "_____________________________________"',
                    "\n",
                    "    "+'"youtube_api": "_____________________________________"',
                "}"
            ]
        )


developer = "REACT#1120"
PYTHON_VERSION = platform.python_version()
OS = platform.system()
#tracker.gg api key
headers = {
        'TRN-Api-Key': trackerapi
    }

status = cycle([f' REACT  | {COMMAND_PREFIX}help ' 
              , f' R      | {COMMAND_PREFIX}help ' 
              , f' RE     | {COMMAND_PREFIX}help '
              , f' REA    | {COMMAND_PREFIX}help '
              , f' REAC   | {COMMAND_PREFIX}help '
              , f' REACT  | {COMMAND_PREFIX}help ' 
              , f' REACT! | {COMMAND_PREFIX}help '])

#not needed delete if want
ASCII_ART = """
 ____            _ _               _       
/ ___| _ __ ___ (_) | _____      _(_)_ __  
\___ \| '_ ` _ \| | |/ _ \ \ /\ / / | '_ \ 
  __) | | | | | | | |  __/\ V  V /| | | | |
|____/|_| |_| |_|_|_|\___| \_/\_/ |_|_| |_|
                                 REACT#1120
""" 

def clearcmd():
    if platform.system() == ("Windows"):
        os.system("cls")
    
    else:
        os.system("clear")


intents = discord.Intents.default()
intents.members = True
client = discord.Client()
client = commands.AutoShardedBot(command_prefix = COMMAND_PREFIX,  case_insensitive=True ,intents=intents)
start_time = datetime.datetime.utcnow()
music = DiscordUtils.Music()
client.remove_command('help')
cluster = MongoClient(mongodb)

db = cluster["Smilewin"]
collection = db["Data"]
collectionlevel = db["Level"]
collectionmoney = db["Money"]
collectionlanguage = db["Language"]

print(ASCII_ART)
print("BOT STATUS : OFFLINE")

@tasks.loop(seconds=1)
async def change_status():
    await client.change_presence(status = discord.Status.idle, activity=discord.Game(next(status)))

@client.event
async def on_ready():
    clearcmd()
    clearcmd()
    change_status.start()
    print(ASCII_ART)
    print(f"BOT NAME : {client.user}")
    print(f"BOT ID : {client.user.id}")
    print("BOT STATUS : ONLINE")
    print("SERVER : " + str(len(client.guilds)))
    print("USER : " + str(len(client.users)))
    print("")
    print("CONSOLE : ")
    print("")

@client.group(invoke_without_command=True)
async def setlanguage(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            colour = 0x00FFFF,
            description = "specify language / ต้องระบุภาษา : thai / english"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

@setlanguage.command()
@commands.has_permissions(administrator=True)
async def thai(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        newserver = {"guild_id":ctx.guild.id,
        "Language":"Thai"
        }

        collectionlanguage.insert_one(newserver)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าภาษา",
            description= f"ภาษาได้ถูกตั้งเป็น Thai"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    else:
        collectionlanguage.update_one({"guild_id":ctx.guild.id},{"$set":{"Language":"Thai"}})
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าภาษา",
            description= f"ภาษาได้ถูกอัพเดตเป็น Thai"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

@setlanguage.command()
@commands.has_permissions(administrator=True)
async def english(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        newserver = {"guild_id":ctx.guild.id,
        "Language":"English"
        }

        collectionlanguage.insert_one(newserver)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าภาษา",
            description= f"ภาษาได้ถูกตั้งเป็น English"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    else:
        collectionlanguage.update_one({"guild_id":ctx.guild.id},{"$set":{"Language":"English"}})
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าภาษา",
            description= f"ภาษาได้ถูกอัพเดตเป็น English"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

@client.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def setrole(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "คุณต้องระบุ give / remove"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        else:
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "you need to specify give / remove"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

@setrole.error
async def setrole_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')         

@setrole.command()
@commands.has_permissions(administrator=True)
async def give(ctx, role: discord.Role):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai": 
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    give_role_id = data["introduce_role_give_id"]
                if give_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                        description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                        description= f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    give_role_id = data["introduce_role_give_id"]
                if give_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                        description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
                        description= f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English": 
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    give_role_id = data["introduce_role_give_id"]
                if give_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "role to give after member introduce themself",
                        description= f"role to give after member introduce themself have been set to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to give after member introduce themself",
                        description= f"role to give after member introduce themself have been updated to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    give_role_id = data["introduce_role_give_id"]
                if give_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "role to give after member introduce themself",
                        description= f"role to give after member introduce themself have been set to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_give_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to give after member introduce themself",
                        description= f"role to give after member introduce themself have been updated to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
@give.error
async def give_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
    
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุยศที่จะให้หลังจากเเนะนําตัว",
                description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะให้หลังจากเเนะนําตัว ``{COMMAND_PREFIX}setrole give @role``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุยศที่จะให้หลังจากเเนะนําตัว",
                    description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะให้หลังจากเเนะนําตัว ``{COMMAND_PREFIX}setrole give @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a role to give after a member introduce themself",
                    description = f" ⚠️``{ctx.author}`` need to specify a role to give after a member introduce themself ``{COMMAND_PREFIX}setrole give @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@setrole.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, role: discord.Role):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
            }
                collection.insert_one(newserver)
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    remove_role_id = data["introduce_role_remove_id"]
                if remove_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                        description= f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                        description= f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    remove_role_id = data["introduce_role_remove_id"]
                if remove_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                        description= f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่ายศที่ลบหลังเเนะนําตัว",
                        description= f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
            }
                collection.insert_one(newserver)
                results = collection.find_one({"guild_id":ctx.guild.id})
                for data in results:
                    remove_role_id = data["introduce_role_remove_id"]
                if remove_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to remove after member introduce themself",
                        description= f"role to remove after member introduce themself have been set to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to remove after member introduce themself",
                        description= f"role to remove after member introduce themself have been updated to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    remove_role_id = data["introduce_role_remove_id"]
                if remove_role_id == "None": 
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to remove after member introduce themself",
                        description= f"role to remove after member introduce themself have been set to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_role_remove_id":role.id}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "role to remove after member introduce themself",
                        description= f"role to remove after member introduce themself have been updated to {role.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

@remove.error
async def remove_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุยศที่จะลบหลังจากเเนะนําตัว",
                description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะลบหลังจากเเนะนําตัว ``{COMMAND_PREFIX}setrole remove @role``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุยศที่จะลบหลังจากเเนะนําตัว",
                    description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะลบหลังจากเเนะนําตัว ``{COMMAND_PREFIX}setrole remove @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a role to remove after a member introduce themself",
                    description = f" ⚠️``{ctx.author}`` need to specify a role to give after a member introduce themself ``{COMMAND_PREFIX}setrole give @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setintroduce(ctx, channel:discord.TextChannel):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    introduce_channel = data["introduce_channel_id"]
                if introduce_channel == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    introduce_channel = data["introduce_channel_id"]
                if introduce_channel == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    introduce_channel = data["introduce_channel_id"]
                if introduce_channel == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "channel for introduction",
                        description= f"Channel have been set to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "channel for introduction",
                        description= f"Channel have been updated to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    introduce_channel = data["introduce_channel_id"]
                if introduce_channel == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "channel for introduction",
                        description= f"Channel have been set to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_channel_id":channel.id,"introduce_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title= "channel for introduction",
                        description= f"Channel have been updated to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
@setintroduce.error
async def setintroduce_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุห้องที่จะตั้ง",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเนะนําตัว ``{COMMAND_PREFIX}setintroduce #channel``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุห้องที่จะตั้ง",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเนะนําตัว ``{COMMAND_PREFIX}setintroduce #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a channel",
                    description = f" ⚠️``{ctx.author}`` need to specify a channel ``{COMMAND_PREFIX}setintroduce #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
@client.command()
@commands.has_permissions(administrator=True)
async def setframe(ctx, *,frame):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai": 
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)

                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    frame = data["introduce_frame"]
                if frame == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ากรอบเเนะนําตัว",
                        description= f"กรอบได้ถูกตั้งเป็น {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ากรอบเเนะนําตัว",
                        description= f"กรอบได้ถูกอัพเดตเป็น {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    frame = data["introduce_frame"]
                if frame == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ากรอบเเนะนําตัว",
                        description= f"กรอบได้ถูกตั้งเป็น {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่ากรอบเเนะนําตัว",
                        description= f"กรอบได้ถูกอัพเดตเป็น {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English": 
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)

                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    frame = data["introduce_frame"]
                if frame == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "set frame",
                        description= f"frame have been set to {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "set frame",
                        description= f"frame have been updated to {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    frame = data["introduce_frame"]
                if frame == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "set frame",
                        description= f"frame have been set to {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_frame":frame}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "set frame",
                        description= f"frame have been updated to {frame}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
@setframe.error
async def setframe_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุกรอบที่จะตั้ง",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุกรอบที่จะตั้ง ``{COMMAND_PREFIX}setframe (frame)``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุกรอบที่จะตั้ง",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุกรอบที่จะตั้ง ``{COMMAND_PREFIX}setframe (frame)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a frame",
                    description = f" ⚠️``{ctx.author}`` need to specify a frame ``{COMMAND_PREFIX}setframe (frame)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.group(invoke_without_command=True)
async def introduce(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "คุณต้องระบุ ON / OFF"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "you need to specify ON / OFF"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

@introduce.command()
@commands.has_permissions(administrator=True)
async def on(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            status = "YES"
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าเเนะนําตัว",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าเเนะนําตัว",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าเเนะนําตัว",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":

            status = "YES"
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

@on.error
async def on_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@introduce.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            status = "NO"
            server = collection.find({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องเเนะนําตัว",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":
            status = "NO"
            server = collection.find({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["introduce_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"introduce_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

@off.error
async def off_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        else:
            language = collectionlanguage.find({"guild_id":ctx.guild.id})
            for data in language:
                server_language = data["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.MissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "คุณไม่มีสิทธิ์ตั้งค่า",
                        description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
        
            if server_language == "English":
                if isinstance(error, commands.MissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "You don't have permission",
                        description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setwebhook(ctx , channel:discord.TextChannel):
    webhook = await channel.create_webhook(name='Smilewinbot')
    webhook = webhook.url
    
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    webhook = data["webhook_url"]
                if webhook == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    webhook = data["webhook_url"]
                if webhook == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    webhook = data["webhook_url"]
                if webhook == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "room to talk to a stranger",
                        description= f"channel have been set to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "room to talk to a stranger",
                        description= f"channel have been updated to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    webhook = data["webhook_url"]
                if webhook == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "room to talk to a stranger",
                        description= f"channel have been set to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_url":webhook,"webhook_channel_id":channel.id,"webhook_status":"YES"}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "room to talk to a stranger",
                        description= f"channel have been updated to {channel.mention}"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
@setwebhook.error
async def setwebhook_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุห้องที่จะตั้ง",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องคุย ``{COMMAND_PREFIX}setwebhook #text-channel``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุห้องที่จะตั้ง",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องคุย ``{COMMAND_PREFIX}setwebhook #text-channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a channel",
                    description = f" ⚠️``{ctx.author}`` need to specify a channel ``{COMMAND_PREFIX}setwebhook #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def chat(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "ต้องระบุ on / off"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "you need to specify on / off"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

@chat.error
async def chat_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@chat.command(aliases=['on'])
@commands.has_permissions(administrator=True)
async def _on(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            status = "YES"
     
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

        if server_language == "English":
            status = "YES"
     
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been activated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

@_on.error
async def chaton_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@chat.command(aliases=['off'])
@commands.has_permissions(administrator=True)
async def _off(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            status = "NO"

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
                        description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
     
        if server_language == "English":
            status = "NO"
     
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
    
                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    status = data["webhook_status"]
                if status == "None":
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')

                else:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"webhook_status":status}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "Anonymous chat",
                        description= f"The command have been deactivated"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
@_off.error
async def chatoff_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx , channel:discord.TextChannel):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["welcome_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["welcome_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
                            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅') 

        if server_language == "English":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["welcome_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "channel for welcome",
                            description= f"Channel have been set to {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "channel for welcome",
                            description= f"Channel have been set to {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["welcome_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "channel for welcome",
                            description= f"Channel have been set to {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"welcome_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "channel for welcome",
                            description= f"Channel have been set to {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')        

@setwelcome.error
async def setwelcome_error(ctx, error):

    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุห้องที่จะตั้ง",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนเข้าเซิฟเวอร์ ``{COMMAND_PREFIX}setwelcome #channel``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุห้องที่จะตั้ง",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนเข้าเซิฟเวอร์``{COMMAND_PREFIX}setwelcome #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a channel",
                    description = f" ⚠️``{ctx.author}`` need to specify a channel ``{COMMAND_PREFIX}setwelcome #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setleave(ctx , channel:discord.TextChannel):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["leave_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["leave_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
                            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

        if server_language == "English":

            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["leave_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "channel for leave",
                            description= f"Channel have been set to {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "channel for leave",
                            description= f"Channel have been set to {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

            else:
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["leave_id"] == "None":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "channel for leave",
                            description= f"Channel have been set to {channel.mention}"
                        )

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"leave_id":channel.id}})

                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title= "channel for leave",
                            description= f"Channel have been set to {channel.mention}"
                        )
        
                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
@setleave.error
async def setleave_error(ctx, error):

    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ระบุห้องที่จะตั้ง",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนออกเซิฟเวอร์ ``{COMMAND_PREFIX}setleave #channel``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุห้องที่จะตั้ง",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือนคนออกเซิฟเวอร์``{COMMAND_PREFIX}setleave #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify a channel",
                    description = f" ⚠️``{ctx.author}`` need to specify a channel ``{COMMAND_PREFIX}setleave #channel``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            if amount < 2000:
                await ctx.channel.purge(limit= amount +1)
                print(f"{amount} of message have been cleared by {ctx.author}")

            else:   
                embed = discord.Embed(
                    colour = 0x983925,
                    title = f"คําสั่งลบข้อความ {amount}",
                    description = f"⚠️ ``{ctx.author}`` การลบข้อความที่จํานวนมากกว่า 2000 นั้นมากเกินไป"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":

            if amount < 2000:
                await ctx.channel.purge(limit= amount +1)
                print(f"{amount} of message have been cleared by {ctx.author}")

            else:   
                embed = discord.Embed(
                    colour = 0x983925,
                    title = f"Clear message {amount}",
                    description = f"⚠️ ``{ctx.author}`` Cannot clear more than 2000 messages"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@clear.error
async def clear_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "จํานวนข้อความที่ต้องการที่จะลบ",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนของข้อความที่จะลบหลังจากคําสั่ง ``{COMMAND_PREFIX}clear [จํานวน]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ลบข้อความ",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``ลบข้อความ`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "จํานวนข้อความที่ต้องการที่จะลบ",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนของข้อความที่จะลบหลังจากคําสั่ง ``{COMMAND_PREFIX}clear [จํานวน]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ลบข้อความ",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``ลบข้อความ`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Amount of messages",
                    description = f" ⚠️``{ctx.author}`` need to specify amount of messages to delete ``{COMMAND_PREFIX}clear [จํานวน]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``manage messages`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        


@client.event
async def on_member_join(member):
    languageserver = collectionlanguage.find_one({"guild_id":member.guild.id})
    if not languageserver is None:
        language = collectionlanguage.find({"guild_id":member.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
     
            try:
                results = collection.find({"guild_id":member.guild.id})
                for data in results:
                    if not data["welcome_id"] == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x99e68b,
                                title =f'ยินดีต้อนรับเข้าสู่ {member.guild.name}',
                                description = 'กรุณาอ่านกฏเเละเคารพกันเเละกันด้วยนะครับ'
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            print(f"{member.name} have joined the server {member.guild.name}")      
                            channel = client.get_channel(id = int(data["welcome_id"]))
                            await channel.send(embed=embed)

                        except Exception:
                            pass
                
                    else:
                        return
    
            except Exception:
                pass
    
        if server_language == "English":
     
            try:
                results = collection.find({"guild_id":member.guild.id})
                for data in results:
                    if not data["welcome_id"] == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x99e68b,
                                title =f'Welcome to {member.guild.name}',
                                description = 'Please read and follow our rules'
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            print(f"{member.name} have joined the server {member.guild.name}")      
                            channel = client.get_channel(id = int(data["welcome_id"]))
                            await channel.send(embed=embed)

                        except Exception:
                            pass
                
                    else:
                        return
    
            except Exception:
                pass
    
    else:
        pass

@client.event
async def on_member_remove(member):
    languageserver = collectionlanguage.find_one({"guild_id":member.guild.id})
    if not languageserver is None:
        language = collectionlanguage.find({"guild_id":member.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
     
            try:
                results = collection.find({"guild_id":member.guild.id})
                for data in results:
                    if not data["leave_id"] == "None":
                        try:
                            embed = discord.Embed(
                                colour=0x983925, 
                                title = "Member leave",
                                description= f"{member.name}ได้ออกจากเซิฟเวอร์"
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            print(f"{member.name} have left the server {member.guild.name}")      
                            channel = client.get_channel(id = int(data["leave_id"]))
                            await channel.send(embed=embed)

                        except Exception:
                            pass
                
                    else:
                        return
    
            except Exception:
                pass
        
        if server_language == "English":
     
            try:
                results = collection.find({"guild_id":member.guild.id})
                for data in results:
                    if not data["leave_id"] == "None":
                        try:
                            embed = discord.Embed(
                                colour=0x983925, 
                                title = "Member leave",
                                description= f"{member.name} have left the server"
                            )

                            embed.set_thumbnail(url=f"{member.avatar_url}")
                            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
                            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                            embed.timestamp = datetime.datetime.utcnow()

                            print(f"{member.name} have left the server {member.guild.name}")      
                            channel = client.get_channel(id = int(data["leave_id"]))
                            await channel.send(embed=embed)

                        except Exception:
                            pass
                
                    else:
                        return
    
            except Exception:
                pass
    
    else:
        pass

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"🙏 สวัสดีครับเซิฟเวอร์ {guild.name}",
                description = f"""
                พิม ``{COMMAND_PREFIX}help`` เพื่อดูคําสั่งของบอท
                Support : https://discord.com/invite/R8RYXyB4Cg
                """

            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='┗Powered by REACT')

            message = await channel.send(embed=embed)
            await message.add_reaction('🙏')
            print(f"Bot have joined a new server {guild.name}")

        break

@client.event
async def on_guild_remove(guild):
    print(f"Bot have left {guild.name}")

@client.event
async def on_command_error(ctx, error):
    try:
        languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if languageserver is None:
            pass

        else:
            language = collectionlanguage.find({"guild_id":ctx.guild.id})
            for data in language:
                server_language = data["Language"]
            
            if server_language == "Thai":
                if isinstance(error, commands.CommandNotFound):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️ไม่มีคําสั่งนี้กรุณาเช็คการสะกดคําว่าถูกหรือผิด"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                else:
                    raise error
            
            if server_language == "English":
                if isinstance(error, commands.CommandNotFound):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"⚠️ Command not found"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')

                else:
                    raise error
    
    except Exception:
        pass

@client.command()
async def membercount(ctx):
    totalmember =ctx.guild.member_count
    memberonly = len([member for member in ctx.guild.members if not member.bot])
    botonly = int(totalmember) - int(memberonly)

    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "English":
            embed = discord.Embed(
                color= 0xffff00,
                title=f"members in {ctx.guild.name}",
                description= f"""

```❤️ Total member : {totalmember}
🧡 Human member : {memberonly}
💛 Bot member : {botonly}```"""

        )  

            embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed=embed)
            await message.add_reaction('❤️')

        if server_language == "Thai":
            embed = discord.Embed(
                color= 0xffff00,
                title=f"สมาชิกใน {ctx.guild.name}",
                description= f"""

```❤️ สมาชิกทั้งหมด : {totalmember}
🧡 สมาชิกที่เป็นคน : {memberonly}
💛 สมาชิกที่เป็นบอท : {botonly}```"""

        )  

            embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed=embed)
            await message.add_reaction('❤️')

@client.command()
async def uptime(ctx): 
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":

            embed = discord.Embed(
                color = 0xffff00,
                title =  "เวลาทำงานของบอท Smilewin",
                description = "```🕒 " + uptime +"```",
            )

            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed=embed)
            await message.add_reaction('🕒')
        
        if server_language == "English":

            embed = discord.Embed(
                color = 0xffff00,
                title =  "Smilewin bot uptime",
                description = "```🕒 " + uptime +"```",
            )

            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed=embed)
            await message.add_reaction('🕒')

@client.command(aliases=['stat'])
async def botinfo(ctx):
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]

    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            embed = discord.Embed(
                colour = 0xffff00,
                title='ข้อมูลของบอท Smilewin bot'
            )

            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name='🤖 ``ชื่อของบอท``', value=f'{client.user}',inline =False)
            embed.add_field(name='🏆 ``ผู้พัฒนาบอท``', value=f'{developer}',inline =False)
            embed.add_field(name='📁 ``จํานวนเซิฟเวอร์``', value=f'{len(client.guilds)}',inline =True)
            embed.add_field(name='📁 ``จํานวนคําสั่ง``', value=f'{len(client.commands)}',inline =True)
            embed.add_field(name='📁 ``สมาชิกทั้งหมด``', value=f'{len(client.users)}',inline =True)
            embed.add_field(name='🤖 ``เครื่องหมายหน้าคำสั่ง``', value=f'{client.command_prefix}',inline =True)
            embed.add_field(name='🤖 ``คําสั่งช่วยเหลือ``', value=f'{COMMAND_PREFIX}help',inline =True)
            embed.add_field(name='🤖 ``เวลาทำงาน``', value=f'{uptime}',inline =True)
            embed.add_field(name='🤖 ``Ping ของบอท``', value=f'{round(client.latency * 1000)}ms',inline =True)
            embed.add_field(name='💻 ``ระบบปฏิบัติการ``', value=f'{OS}',inline =True)
            embed.add_field(name='💻 ``เเรมที่ใช้``', value=f"{psutil.virtual_memory().percent} %" ,inline =True)
            embed.add_field(name='🤖 ``ภาษาที่ใช้เขียนบอท``', value=f'Python {PYTHON_VERSION}',inline =True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_thumbnail(url=client.user.avatar_url)

            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')
        
        if server_language == "English":

            embed = discord.Embed(
                colour = 0xffff00,
                title='Smilewin bot info'
            )

            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name='🤖 ``Bot name``', value=f'{client.user}',inline =False)
            embed.add_field(name='🏆 ``Developer``', value=f'{developer}',inline =False)
            embed.add_field(name='📁 ``Total servers``', value=f'{len(client.guilds)}',inline =True)
            embed.add_field(name='📁 ``Total commands``', value=f'{len(client.commands)}',inline =True)
            embed.add_field(name='📁 ``Total user``', value=f'{len(client.users)}',inline =True)
            embed.add_field(name='🤖 ``Command prefix``', value=f'{client.command_prefix}',inline =True)
            embed.add_field(name='🤖 ``Help command``', value=f'{COMMAND_PREFIX}help',inline =True)
            embed.add_field(name='🤖 ``Bot uptime``', value=f'{uptime}',inline =True)
            embed.add_field(name='🤖 ``Bot ping``', value=f'{round(client.latency * 1000)}ms',inline =True)
            embed.add_field(name='💻 ``OS``', value=f'{OS}',inline =True)
            embed.add_field(name='💻 ``RAM``', value=f"{psutil.virtual_memory().percent} %" ,inline =True)
            embed.add_field(name='🤖 ``Programming language``', value=f'Python {PYTHON_VERSION}',inline =True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_thumbnail(url=client.user.avatar_url)

            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')

@client.command()
async def serverinfo(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0xffff00,
                title=f"{ctx.guild.name}", 
                description="ข้อมูลเซิฟเวิร์ฟ" + f'{ctx.guild.name}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="วันที่สร้างเซิฟเวอร์", value=f"{ctx.guild.created_at}")
            embed.add_field(name="เจ้าของเซิฟเวอร์", value=f"{ctx.guild.owner}")
            embed.add_field(name="พื้นที่เซิฟเวอร์", value=f"{ctx.guild.region}")
            embed.add_field(name="เซิฟเวอร์ ID", value=f"{ctx.guild.id}")
            embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0xffff00,
                title=f"{ctx.guild.name}", 
                description="Server info" + f'{ctx.guild.name}')
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="Creation date", value=f"{ctx.guild.created_at}")
            embed.add_field(name="Server owner", value=f"{ctx.guild.owner}")
            embed.add_field(name="Region", value=f"{ctx.guild.region}")
            embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
            embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')

@client.command()
async def userinfo(ctx, member: discord.Member = None):

    roles = [role for role in member.roles]
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = member.color,
                title = f"ข้อมูลของสมาชิก {member}"
            )
            embed.set_author(name = f'ข้อมูลของ {member}', icon_url=f"{member.avatar_url}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}",icon_url=ctx.author.avatar_url)
            embed.add_field(name="```ID ของสมาชิก:```",value=member.id)
            embed.add_field(name="```ชื่อในเซิฟ:```",value=member.display_name)
            embed.add_field(name="```วันที่สมัคร:```",value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="```วันที่เข้าเซิฟ:```",value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name=f"```ยศทั้งหมด:```({len(roles)})",value=" ".join([role.mention for role in roles]))
            embed.add_field(name="```ยศสูงสุด:```",value=member.top_role.mention)
            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = member.color,
                title = f"Info of {member}"
            )
            embed.set_author(name = f'Info of {member}', icon_url=f"{member.avatar_url}")
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}",icon_url=ctx.author.avatar_url)
            embed.add_field(name="```Member id:```",value=member.id)
            embed.add_field(name="```Member nickname:```",value=member.display_name)
            embed.add_field(name="```Creation date:```",value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="```Joined date:```",value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name=f"```All roles:```({len(roles)})",value=" ".join([role.mention for role in roles]))
            embed.add_field(name="```Highest role:```",value=member.top_role.mention)
            message = await ctx.send(embed=embed)
            await message.add_reaction('🤖')

@client.command()
async def ping(ctx):
    latency = requests.get("https://discord.com/").elapsed.total_seconds()
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "English":

            embed = discord.Embed(
                color = 0xffff00,
                title = 'Smilewin bot ping',
                description = f"""
```⌛ Ping : {round(client.latency * 1000)}ms
⌛ Discord Latency : {latency}ms```
        
        """, 

            )

            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('⌛')
            print(f"{ctx.author} ping bot and the latency is {round(client.latency * 1000)}ms")
        
        if server_language == "Thai":

            embed = discord.Embed(
                color = 0xffff00,
                title = 'Smilewin bot ping',
                description = f"""
```⌛ ปิงของบอท : {round(client.latency * 1000)}ms
⌛ เวลาในการตอบสนอง Discord : {latency}ms```
        
        """, 

            )

            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('⌛')
            print(f"{ctx.author} ping bot and the latency is {round(client.latency * 1000)}ms")

@client.command()
async def hastebin(ctx, *, message): 
    r = requests.post("https://hastebin.com/documents", data=message).json()
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f'Hastebin link ของ {ctx.author}',
                description = f"""
```📒 นี้คือลิงค์ Hastebin ของคุณ : 

https://hastebin.com/{r['key']}```"""
    )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed = embed)
            await message.add_reaction('📒')
            print(f"{ctx.author} have made a hastebinlink : https://hastebin.com/{r['key']}")
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f'Hastebin link ของ {ctx.author}',
                description = f"""
```📒 This is your Hastebin link : 

https://hastebin.com/{r['key']}```"""
    )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed = embed)
            await message.add_reaction('📒')
            print(f"{ctx.author} have made a hastebinlink : https://hastebin.com/{r['key']}")

@hastebin.error
async def hastebin_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ข้อความที่ต้องการที่จะใส่",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{COMMAND_PREFIX}hastebin (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ข้อความที่ต้องการที่จะใส่",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{COMMAND_PREFIX}hastebin (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "message",
                    description = f" ⚠️``{ctx.author}`` need to specify of messages to put in hastebin ``{COMMAND_PREFIX}hastebin (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def pastebin(ctx, *,message):
    data = {
    'api_option': 'paste',
    'api_dev_key':pastebinapi,
    'api_paste_code':message,
    'api_paste_name':"Smilewinbot",
    'api_paste_expire_date': 'N',
    'api_user_key': None,
    'api_paste_format': 'python'
    }
    r = requests.post("https://pastebin.com/api/api_post.php", data=data)
    r = r.text
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f'Pastebin link ของ {ctx.author}',
                description = f"""
```📒 นี้คือลิงค์ Pastebin ของคุณ : 

{r.text}```"""
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed = embed)
            await message.add_reaction('📒')
            print(f"{ctx.author} have made a Pastebinlink : {r.text}")
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f'Pastebin link ของ {ctx.author}',
                description = f"""
```📒 This is your Pastebin link : 

{r.text}```"""
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message = await ctx.send(embed = embed)
            await message.add_reaction('📒')
            print(f"{ctx.author} have made a Pastebinlink : {r.text}")

@pastebin.error
async def pastebin_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ข้อความที่ต้องการที่จะใส่",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{COMMAND_PREFIX}pastebin (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ข้อความที่ต้องการที่จะใส่",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่ต้องการที่จะใส่ ``{COMMAND_PREFIX}pastebin (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "message",
                    description = f" ⚠️``{ctx.author}`` need to specify of messages to put in pastebin ``{COMMAND_PREFIX}pastebin (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def sreddit(ctx, subreddit):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            subreddit=reddit.subreddit(subreddit)
            all_subs = []
            hot = subreddit.hot(limit = 10)

            for submission in hot:
                all_subs.append(submission) 
        
            random_sub = random.choice(all_subs)
            title =random_sub.title
            url = random_sub.url
            embed = discord.Embed(
                colour = 0x00FFFF,
                title =f"{title}",
                description = f"ที่มาของรูปคือ subreddit r/{subreddit}"
                )

            embed.set_image(url=url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message= await ctx.send(embed=embed)
            await message.add_reaction('✨')
        
        if server_language == "English":
            subreddit=reddit.subreddit(subreddit)
            all_subs = []
            hot = subreddit.hot(limit = 10)

            for submission in hot:
                all_subs.append(submission) 
        
            random_sub = random.choice(all_subs)
            title =random_sub.title
            url = random_sub.url
            embed = discord.Embed(
                colour = 0x00FFFF,
                title =f"{title}",
                description = f"Source : subreddit r/{subreddit}"
                )

            embed.set_image(url=url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()

            message= await ctx.send(embed=embed)
            await message.add_reaction('✨')

@sreddit.error
async def sreddit_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` กรุณาระบุsubreddit ที่ต้องการ ``{COMMAND_PREFIX}sreddit (subreddit)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` กรุณาระบุsubreddit ที่ต้องการ ``{COMMAND_PREFIX}sreddit (subreddit)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` please specify a subreddit ``{COMMAND_PREFIX}sreddit (subreddit)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
@client.command()
async def dota2now(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/570"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น dota2 ในตอนนี้",
                        description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg?t=1608587587")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')
        
        if server_language == "English":
            url = "https://steamcharts.com/app/570"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น dota2 ในตอนนี้",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg?t=1608587587")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def csgonow(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/730"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น CS:GO",
                        description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg?t=1607046958")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

        if server_language == "English":
            url = "https://steamcharts.com/app/730"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น CS:GO",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg?t=1607046958")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def pubgnow(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/578080"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น PUBG ในตอนนี้",
                        description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/578080/header.jpg?t=1608093288")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')
        
        if server_language == "English":
            url = "https://steamcharts.com/app/578080"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น PUBG ในตอนนี้",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/578080/header.jpg?t=1608093288")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def rb6now(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/359550"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น RB6 ในตอนนี้",
                        description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/359550/header.jpg?t=1606776740")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

        if server_language == "English":
            url = "https://steamcharts.com/app/359550"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น RB6 ในตอนนี้",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/359550/header.jpg?t=1606776740")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def apexnow(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/1172470"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น APEX LEGEND ในตอนนี้",
                        description = f"""```
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/1172470/header.jpg?t=1609705061")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

        if server_language == "English":
            url = "https://steamcharts.com/app/1172470"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น APEX LEGEND ในตอนนี้",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/1172470/header.jpg?t=1609705061")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def gtanow(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = "https://steamcharts.com/app/271590"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    soupObject = BeautifulSoup(await response.text(), "html.parser")
                    div = soupObject.find_all('div', class_='app-stat')[0]
                    div1 = soupObject.find_all('div', class_='app-stat')[1]
                    div2 = soupObject.find_all('div', class_='app-stat')[2]

                    online = div.contents[1].string
                    online24 = div1.contents[1].string
                    onlineall = div2.contents[1].string
                    player = humanize.intcomma(online)
                    player24 = humanize.intcomma(online24)
                    playerall = humanize.intcomma(onlineall)

                    embed = discord.Embed(
                        color=0x75ff9f,
                        title = "จํานวนคนที่เล่น GTAV ในตอนนี้",
                        description = f"""```
Currently online : {player}
Highest player online in 24hrs : {player24}
Higest player online {playerall}``` """
            )

                    embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1592866696")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.timestamp = datetime.datetime.utcnow()
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('🎮')

@client.command()
async def botinvite(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            invitelink = str(f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
            embed = discord.Embed(  
                colour = 0x00FFFF,
                title = f"ลิงค์เชิญบอท SmileWin : ",
                description = f"[คลิกที่นี้]({invitelink})"

            )
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('💖')
        
        if server_language == "English":

            invitelink = str(f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
            embed = discord.Embed(  
                colour = 0x00FFFF,
                title = f"invite link : ",
                description = f"[click here]({invitelink})"

            )
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('💖')

@client.command(aliases=['bitcoin'])
async def btc(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,THB')
        r = r.json()
        usd = r['USD']
        eur = r['EUR']
        thb = r['THB']
        embed = discord.Embed(
            colour = 0xffff00,
            title = "Bitcoin",
            description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`\nTHB: `{str(thb)}฿`')
        embed.set_author(name='Bitcoin', icon_url='https://i.imgur.com/3gVaQ4z.png')
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

@client.command(aliases=['ethereum'])
async def eth(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,THB')
        r = r.json()
        usd = r['USD']
        eur = r['EUR']
        thb = r['THB']  
        embed = discord.Embed(
            colour = 0xffff00,
            title = "Ethereum",
            description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`\nTHB: `{str(thb)}฿`')
        embed.set_author(name='Ethereum', icon_url='https://i.imgur.com/vsWBny2.png')
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

@client.command()
async def ascii(ctx, *, text):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai": 
            r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
            if len('```'+r+'```') > 2000:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` ตัวอักษรมากเกินไป ``"
                )
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            else:
    
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "🎨 ASCII ",
                    description = (f"```{r}```")

                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('🎨')
        
        if server_language == "English": 
            r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
            if len('```'+r+'```') > 2000:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` Too much letter ``"
                )
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            else:
    
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "🎨 ASCII ",
                    description = (f"```{r}```")

                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('🎨')

@ascii.error
async def ascii_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
    
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่ต้องการสร้าง ascii art ``{COMMAND_PREFIX}ascii (word)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่ต้องการสร้าง ascii art ``{COMMAND_PREFIX}ascii (word)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` please specify what to turn into ascii art ``{COMMAND_PREFIX}ascii (word)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
@client.command(aliases=['coin'])
async def coinflip(ctx):
    responses = ['https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png']
    flip = random.choice(responses)
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
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

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            await member.kick(reason=reason)
            if reason is None:
                reason = "None"

            embed = discord.Embed(
                color = 0x983925,
                title = f"😤 สมาชิก {member} ถูกเตะออกจากเซิร์ฟเวอร์",
                description = f"""
                ผู้เเตะ : ``{ctx.author}``
                สาเหตุ : ``{reason}``"""
        
            )

            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')
        
        if server_language == "English":
            await member.kick(reason=reason)
            if reason is None:
                reason = "None"

            embed = discord.Embed(
                color = 0x983925,
                title = f"😤 {member} have been kicked from server",
                description = f"""
                Punisher : ``{ctx.author}``
                Reason : ``{reason}``"""
        
            )

            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
    
            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')

            print(f"{ctx.author} have kicked {member} with reason {reason}")

@kick.error
async def kick_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ชื่อสมาชิกที่จะเเตะ",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเตะ ``{COMMAND_PREFIX}kick [@user]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์เเตะ",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเตะ`` ก่อนใช้งานคำสั่งนี้"
            )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️') 
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ชื่อสมาชิกที่จะเเตะ",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเตะ ``{COMMAND_PREFIX}kick [@user]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์เเตะ",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเตะ`` ก่อนใช้งานคำสั่งนี้"
                )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify member",
                    description = f" ⚠️``{ctx.author}`` need to specify who to kick ``{COMMAND_PREFIX}kick [@user]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``kick`` to be able to use this command"
                )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            await member.ban(reason=reason)
            if reason is None:
                reason = "None"

            embed = discord.Embed(
                color = 0x983925,
                title = f"😤 สมาชิก {member} ถูกเเบนออกจากเซิร์ฟเวอร์",
                description = f"""
                ผู้เเบน : ``{ctx.author}``
                สาเหตุ : ``{reason}``"""
                
            )

            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')
        
        if server_language == "English":
            await member.ban(reason=reason)
            if reason is None:
                reason = "None"
                
            embed = discord.Embed(
                color = 0x983925,
                title = f"😤 {member} have been banned from server",
                description = f"""
                Punisher : ``{ctx.author}``
                Reason : ``{reason}``"""
                
            )

            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')

@ban.error
async def ban_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ชื่อสมาชิกที่จะเเบน",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}ban [@user]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์เเตะ",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเบน`` ก่อนใช้งานคำสั่งนี้"
            )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️') 
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ชื่อสมาชิกที่จะเเบน",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}ban [@user]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์เเตะ",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเบน`` ก่อนใช้งานคำสั่งนี้"
            )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify member",
                    description = f" ⚠️``{ctx.author}`` need to specify who to ban ``{COMMAND_PREFIX}ban [@user]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``ban`` to be able to use this command"
            )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def disconnect(ctx, member : discord.Member):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x983925,
                title = f'สมาชิก {member} ได้ถูกดีดออกจาก voice chat โดย {ctx.author}'
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')
            await member.move_to(channel=None)
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x983925,
                title = f'{member} have been disconnected from voice chat by {ctx.author}'
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('😤')
            await member.move_to(channel=None)

@disconnect.error
async def disconnect_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ชื่อสมาชิกที่จะdisconnect",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}disconnect [@user]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
    
            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ย้ายสมาชิก",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️') 

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ชื่อสมาชิกที่จะdisconnect",
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}disconnect [@user]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
    
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ย้ายสมาชิก",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                    )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️') 


@client.command()
async def covid19th(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get('https://covid19.th-stat.com/api/open/today')
        r = r.json()

        newconfirm = r['NewConfirmed']
        newdeath = r['NewDeaths']
        recover = r['Recovered']
        death = r['Deaths']
        source = r['Source']
        update = r['UpdateDate']
        confirm = r['Confirmed']
        hospital = r['Hospitalized']
        hospitalnew = r['NewHospitalized']

        if server_language == "Thai":

            embed = discord.Embed(
                title="💊 ข้อมูล COVID-19 ประเทศไทย",
                description=f"อัพเดตล่าลุดเมื่อ {update}",
                color=0x00FFFF
            )

            embed.add_field(name='🤒 ผู้ป่วยสะสม',value=f"{confirm} คน")
            embed.add_field(name='😷 ผู้ป่วยรายใหม่',value=f"{newconfirm} คน")
            embed.add_field(name='🏠 ผู้ป่วยรักษาหายแล้ว',value=f"{recover} คน")
            embed.add_field(name='🏠 ผู้ป่วยที่เข้าโรงพยาบาลทั้งหมด',value=f"{hospital} คน")
            embed.add_field(name='🏠 ผู้ป่วยที่อยู่เข้าโรงพยาบาลใหม่',value=f"{hospitalnew} คน")
            embed.add_field(name='☠️ ผู้ป่วยเสียชีวิตทั้งหมด',value=f"{death} คน")
            embed.add_field(name='☠️ ผู้ป่วยเสียชีวิตใหม่',value=f"{newdeath} คน")
            embed.set_footer(text=f'''ข้อมูลจาก {source}''')

            message= await ctx.send(embed=embed)
            await message.add_reaction('💊')
        
        if server_language == "English":

            embed = discord.Embed(
                title="💊 Thailand COVID-19 status",
                description=f"lastest update: {update}",
                color=0x00FFFF
            )

            embed.add_field(name='🤒 Total confirm cases',value=f"{confirm} คน")
            embed.add_field(name='😷 New cases',value=f"{newconfirm} คน")
            embed.add_field(name='🏠 Total recover patients',value=f"{recover} คน")
            embed.add_field(name='🏠 Total hospitalize',value=f"{hospital} คน")
            embed.add_field(name='🏠 New hospitalize',value=f"{hospitalnew} คน")
            embed.add_field(name='☠️ Total death',value=f"{death} คน")
            embed.add_field(name='☠️ New death',value=f"{newdeath} คน")
            embed.set_footer(text=f'''Source : {source}''')

            message= await ctx.send(embed=embed)
            await message.add_reaction('💊')

@client.command()
async def help(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คำสั่งสำหรับใช้งานบอท',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}help``',value='คําสั่งช่วยเหลือ' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpbot``',value='คําสั่งเกี่ยวกับตัวบอท' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpfun``',value='คําสั่งบรรเทิง' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpgeneral``',value='คําสั่งทั่วไป' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpgame``',value='คําสั่งเกี่ยวกับเกม' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpadmin``',value='คําสั่งของเเอดมิน' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpsetup``',value='คําสั่งเกี่ยวกับตั้งค่า' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpinfo``',value='คําสั่งเกี่ยวกับข้อมูล' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpimage``',value='คําสั่งเกี่ยวกับรูป' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpeconomy``',value='คําสั่งเกี่ยวกับระบบเศรษฐกิจ' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpuser``',value='คําสั่งข้อมูลของสมาชิกเช่น เลเวล' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpnsfw``',value='คําสั่ง 18 + ' , inline = False)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='Help command',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}help``',value='help commands' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpbot``',value='help commands related to bot' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpfun``',value='help commands related to fun' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpgeneral``',value='help general commands' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpgame``',value='help commands related to game' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpadmin``',value='help commands related to moderator' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpsetup``',value='help commands related to setup' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpinfo``',value='help commands related to information' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpimage``',value='help commands related to image' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpeconomy``',value='help commands related to economy' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpuser``',value='help commands related to user' , inline = False)
            embed.add_field(name=f'``{COMMAND_PREFIX}helpnsfw``',value='help commands related to NSFW' , inline = False)
            embed.set_thumbnail(url=client.user.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpeconomy(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับระบบเศรษฐกิจ',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}openbal``', value = 'เปิดบัญชีธนาคาร',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}bal (@member)``', value='ดูเงินของคุณหรือของสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}deposit (amount)``', value ='ฝากเงินเข้าธนาคาร', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}withdraw (amount)``', value = 'ถอนเงินจากธนาคาร',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pay @member``', value ='โอนเงินจากธนาคารให้สชาชิกในเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}slot (amount)``', value ='เล่นพนัน slot', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rob @member``', value ='ขโมยเงินจากสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}addcredit (amount) @member``', value ='เพิ่มตังให้สมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}work``', value ='ทํางาน', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='help commands related to economy',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}openbal``', value = 'Open a new balance',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}bal (@member)``', value='Check your balance', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}deposit (amount)``', value ='Deposit money to the bank', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}withdraw (amount)``', value = 'Withdraw money from the bank',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pay @member``', value ='Pay money to user in the server', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}slot (amount)``', value ='Slot machine', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rob @member``', value ='steal money', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}addcredit (amount) @member``', value ='add money to user', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpbot(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับตัวบอท',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}test``', value = 'ดูว่าบอทonline ไหม',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ping``', value='ส่ง ping ของบอท', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}uptime``', value ='ส่ง เวลาทำงานของบอท', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}botinvite``', value = 'ส่งลิงค์เชิญบอท',inline = True )
            embed.add_field(name=f'``{COMMAND_PREFIX}credit``',value='เครดิตคนทําบอท',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}botinfo``', value = 'ข้อมูลเกี่ยวกับตัวบอท',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}support (text)``', value = 'ส่งข้อความหา support หากพบปัญหา',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='help commands related to bot',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}test``', value = 'test command to see if the bot is online',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ping``', value='send bot ping', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}uptime``', value ='send bot uptime', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}botinvite``', value = 'send bot invite link',inline = True )
            embed.add_field(name=f'``{COMMAND_PREFIX}credit``',value='developer credit',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}botinfo``', value = 'information about bot',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}support (text)``', value = 'send support if error occur',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpuser(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งข้อมูลของสมาชิก',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}rank @member``', value = 'เช็คเเรงค์ของคุณหรือสมาชิก',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}leaderboard``', value='ดูอันดับเลเวลของคุณในเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ind``', value='เเนะนําตัว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}vfy``', value='ยืนยันตัวตนโดย captcha', inline = True)


            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='help commands related to user',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}rank @member``', value = 'see your level or member level in the server',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}leaderboard``', value='level leaderboard', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ind``', value='Introduce yourself', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}vfy``', value='captcha verification', inline = True)

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpsetup(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับตั้งค่า',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}setup``', value ='ลงทะเบียนเซิฟเวอร์ในฐานข้อมูล', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}welcomeset #text-channel``', value='ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}leaveset #text-channel``', value ='ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setwebhook #text-channel``', value =f'ตั้งค่าห้องที่จะใช้คําสั่ง {COMMAND_PREFIX}anon (message) เพื่อคุยกับคนเเปลกหน้าโดยที่ไม่เปิดเผยตัวตนกับเซิฟเวอร์ที่เปิดใช้คําสั่งนี้', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setintroduce #text-channel``', value =f'ตั้งค่าห้องที่จะให้ส่งข้อมูลของสมาชิกหลังจากเเนะนําตัวเสร็จ *พิม {COMMAND_PREFIX}ind เพื่อเเนะนําตัว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setrole give/remove @role``', value =f'ตั้งค่าที่จะ ให้/ลบหลังจากเเนะนําตัว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setframe``', value ='ตั้งกรอบที่ใส่ข้อมูลของสมาชิกจากปกติเป็น ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}chat on/off``', value ='เปิด / ปิดใช้งานห้องคุยกับคนเเปลกหน้า', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}level on/off``', value ='เปิด / ปิดใช้งานระบบเลเวล', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}introduce on/off``', value ='เปิด / ปิดการใช้งานคําสั่งเเนะนําตัว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}economy on/off``', value ='เปิด / ปิดการใช้งานระบบเศรษฐกิจ', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='help commands related to setup',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}setup``', value ='set up your server to our database', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}welcomeset #text-channel``', value='set up a channel to notify if new member join', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}leaveset #text-channel``', value ='set up a channel to notify if member left', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setwebhook #text-channel``', value =f'setup room to talk to a stranger and use {COMMAND_PREFIX}anon (message) to talk to stranger', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setintroduce #text-channel``', value =f'setup a room for member to introduce themself and use {COMMAND_PREFIX}ind to introduce', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setrole give/remove @role``', value =f'setup a role to give/remove after a member finish introducing himself/herself', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}setframe``', value ='set the frame around member information after they introduce themself, Normal frame: ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}chat on/off``', value ='turn on/off ability to talk to a stranger', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}level on/off``', value ='turn on/off level system', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}introduce on/off``', value ='turn on/off introduce command', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}economy on/off``', value ='turn on/off an economy system', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}verification on/off``', value ='turn on/off an verification system', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpgame(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับเกม',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}coinflip``', value='ทอยเหรียญ', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rps``', value = 'เป่ายิ้งฉับเเข่งกับบอท',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}roll``', value='ทอยลูกเต๋า', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}8ball (question) ``', value='ดูว่าควรจะทําสิงๆนั้นไหม', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}csgonow``', value = 'จํานวนคนที่เล่น CSGO ขณะนี้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}apexnow``', value = 'จํานวนคนที่เล่น APEX ขณะนี้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rb6now``', value = 'จํานวนคนที่เล่น RB6 ขณะนี้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pubgnow``', value = 'จํานวนคนที่เล่น PUBG ขณะนี้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}gtanow``', value = 'จํานวนคนที่เล่น GTA V ขณะนี้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}apexstat (username)``', value = 'ดูข้อมูลเกม apex ของคนๆนั้น',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rb6rank (user)``', value = 'ดูเเรงค์เเละmmrของคนๆนั้น',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับเกม',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}coinflip``', value='flip a coin', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rps``', value = 'play rock paper scissor',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}roll``', value='roll a dice', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}8ball (question) ``', value='plau 8ball', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}csgonow``', value = 'People playing CSGO at this time',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}apexnow``', value = 'People playing Apex at this time',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rb6now``', value = 'People playing RB6 at this time',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pubgnow``', value = 'People playing PUBG at this time',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}gtanow``', value = 'People playing gtanow at this time',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}apexstat (user)``', value = 'see a user apex in-game stat',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}rb6rank (username)``', value = 'see a user rank and mmr in rb6',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpinfo(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับข้อมูล',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}serverinfo``', value='ข้อมูลเกี่ยวกับเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}membercount``', value='จํานวนสมาชิกในเซิฟเวอร์', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}userinfo @member``', value ='ข้อมูลเกี่ยวกับสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}covid19th``', value = 'ข้อมูลเกี่ยวกับcovid19 ในไทย',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}covid19``', value = 'ข้อมูลเกี่ยวกับcovid19ทั่วโลก',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}geoip (ip)``', value = 'ข้อมูลเกี่ยว IP นั้น',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}weather (city)``', value = 'ดูสภาพอากาศของจังหวัด',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}country (country)``', value = 'ดูข้อมูลของประเทศ',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}btc``',value='ข้อมูลเกี่ยวกับราคา Bitcoin',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}eth``',value='ข้อมูลเกี่ยวกับราคา Ethereum ',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}github (username)``',value='ดูข้อมูลในของคนใน Github',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}avatar @member``',value='ดูรูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}searchavatar @member``',value='search หารูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}guildicon``',value='ดูรูปโปรไฟล์ของเซิฟเวอร์',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
        
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='help commands related to information',
                description=f'{ctx.author.mention}, The command prefix is ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}serverinfo``', value='info about your server', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}membercount``', value='Number of members in the server', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}userinfo @member``', value ='info about member', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}covid19th``', value = 'Thailand COVID-19 status',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}covid19``', value = 'Covid-19 around the world',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}geoip (ip)``', value = 'Info about the ip address',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}weather (city)``', value = 'display weather of a city',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}country (country)``', value = 'see info of a country',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}btc``',value='Bitcoin prices',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}eth``',value='Ethereum prices',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}github (username)``',value='info of Github user',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}avatar @member``',value='View your profile picture or a member profile picture',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}searchavatar @member``',value='search your profile picture or a member profile picture',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}guildicon``',value='View server icon',inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
        
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpadmin(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวเเอดมิน',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}kick @member``', value='เเตะสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ban @member``', value ='เเบนสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}unban member#1111``', value ='ปลดเเบนสมาชิก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}giverole @member @role``', value = 'ให้ยศกับสมาชิก',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}removerole @member @role``', value = 'เอายศของสมาชิกออก',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}roleall @role``', value = 'ให้ยศกับสมาชิกทุกคนที่สามารถให้ได้',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}removeroleall @role``', value = 'ลบยศกับสมาชิกทุกคน',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}changenick @member newnick``', value = 'เปลี่ยนชื่อของสมาชิก',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}clear (จํานวน) ``', value = 'เคลียข้อความตามจํานวน',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}disconnect @member``' ,value = 'disconnect สมาชิกที่อยู่ในห้องพูด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}movetome @member``' ,value = 'ย้ายสมาชิกมาห้องของเรา', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวเเอดมิน',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}kick @member``', value='ban a member', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ban @member``', value ='kick a member', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}unban member#1111``', value ='unban a member', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}giverole @member @role``', value = 'give role to member',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}removerole @member @role``', value = 'remove role from member',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}roleall @role``', value = 'give role to all member',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}removeroleall @role``', value = 'remove role to all member',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}changenick @member newnick``', value = 'change member nickname',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}clear (จํานวน) ``', value = 'clear messages',inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}disconnect @member``' ,value = 'disconnect a member', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}movetome @member``' ,value = 'move a member to your voice chat', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpfun(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งบรรเทิง',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
            )
            embed.add_field(name=f'``{COMMAND_PREFIX}anon (message)``', value=f'พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {COMMAND_PREFIX}helpsetup', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}sreddit (subreddit)``', value='ส่งรูปจาก subreddit', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}meme``', value='ส่งมีม', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ascii (message)``', value='เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}tweet (username) (message)``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}phcomment (text)``', value='สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}wasted @member``', value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}gay @member``', value='ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}trigger @member``', value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}slim``', value='สุ่มส่งคําพูดของสลิ่ม', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}youtube (ชื่อคลิป)``', value='ดูข้อมูลของคลิปใน YouTube', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ytsearch (keyword)``', value='ค้นหาคลิปใน YouTube', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}captcha (text)``', value='ทํา captcha จากคําที่ใส่', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='คําสั่งบรรเทิง',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
            )
            embed.add_field(name=f'``{COMMAND_PREFIX}anon (message)``', value=f'พูดคุยกัคนเเปลกหน้าที่อยู่เซิฟเวอร์อื่น *ต้องตั้งค่าก่อน {COMMAND_PREFIX}helpsetup', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}sreddit (subreddit)``', value='ส่งรูปจาก subreddit', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}meme``', value='ส่งมีม', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ascii (message)``', value='เปลี่ยนตัวอักษรภาษาอังกฤษเป็นภาพ ASCII', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}tweet (username) (message)``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}phcomment (text)``', value='สร้างรูป commentใน pornhub โดยใช้ชื่อเเละภาพของเรา', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}wasted @member``', value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}gay @member``', value='ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}trigger @member``', value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}slim``', value='สุ่มส่งคําพูดของสลิ่ม', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}youtube (ชื่อคลิป)``', value='ดูข้อมูลของคลิปใน YouTube', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}ytsearch (keyword)``', value='ค้นหาคลิปใน YouTube', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}captcha (text)``', value='ทํา captcha จากคําที่ใส่', inline = True)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpgeneral(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งทั่วไป',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}qr (message)``', value='สร้าง qr code', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}hastebin (message)``', value='สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pastebin (message)``', value='สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}lmgtfy (message)``', value= 'สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}timer (second)``', value= 'นาฬิกานับถอยหลัง (ห้ามมีจุดทศนิยม)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}count (second)``', value= 'นาฬิกานับเวลา (ห้ามมีจุดทศนิยม)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}upper (message)``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}lower (message)``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}enbinary (message)``', value= 'เเปลคําพูดเป็น binary (0101)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}debinary (binnary)``', value= 'เเปลbinary เป็นคําพูด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}calculator (equation)``', value= 'คํานวนคณิตศาสตร์ + - * / ^ ', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}embed (message)``', value= 'สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}length (text)``', value= 'นับจำนวนตัวอักษร', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}reverse (message)``', value= 'กลับหลังประโยค', inline = True)

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='คําสั่งทั่วไป',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}qr (message)``', value='สร้าง qr code', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}hastebin (message)``', value='สร้างลิงค์ Hastebin โดยมีข้อความข้อข้างใน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}pastebin (message)``', value='สร้างลิงค์ Pastebin โดยมีข้อความข้อข้างใน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}lmgtfy (message)``', value= 'สร้างลิงค์ lmgtfy เพื่อsearchหาสิ่งที่เขียน', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}timer (second)``', value= 'นาฬิกานับถอยหลัง (ห้ามมีจุดทศนิยม)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}count (second)``', value= 'นาฬิกานับเวลา (ห้ามมีจุดทศนิยม)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}upper (message)``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมใหญ่ทั้งหมด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}lower (message)``', value= 'เปลี่ยนประโยคหรือคําเป็นตัวพิมเล็กทั้งหมด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}enbinary (message)``', value= 'เเปลคําพูดเป็น binary (0101)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}debinary (binnary)``', value= 'เเปลbinary เป็นคําพูด', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}calculator (equation)``', value= 'คํานวนคณิตศาสตร์ + - * / ^ ', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}embed (message)``', value= 'สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}length (text)``', value= 'นับจำนวนตัวอักษร', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}reverse (message)``', value= 'กลับหลังประโยค', inline = True)

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpimage(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับรูป',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}bird``', value='ส่งภาพนก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}panda``', value='ส่งภาพเเพนด้า', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}cat``', value= 'ส่งภาพเเมว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}dog``', value= 'ส่งภาพหมา', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}fox``', value= 'ส่งภาพสุนัขจิ้งจอก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}koala``', value= 'ส่งภาพหมีโคอาล่า', inline = True)

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed=discord.Embed(
                title='คําสั่งเกี่ยวกับรูป',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f'``{COMMAND_PREFIX}bird``', value='ส่งภาพนก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}panda``', value='ส่งภาพเเพนด้า', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}cat``', value= 'ส่งภาพเเมว', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}dog``', value= 'ส่งภาพหมา', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}fox``', value= 'ส่งภาพสุนัขจิ้งจอก', inline = True)
            embed.add_field(name=f'``{COMMAND_PREFIX}koala``', value= 'ส่งภาพหมีโคอาล่า', inline = True)

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def helpnsfw(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            embed=discord.Embed(
                title='คําสั่งnsfw',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f"""

ส่งรูปตาม catergory 

{COMMAND_PREFIX}gsolo
{COMMAND_PREFIX}smallboob
{COMMAND_PREFIX}classic
{COMMAND_PREFIX}pussy
{COMMAND_PREFIX}eroyuri
{COMMAND_PREFIX}yuri
{COMMAND_PREFIX}solo
{COMMAND_PREFIX}anal
{COMMAND_PREFIX}erofeet
{COMMAND_PREFIX}feet
{COMMAND_PREFIX}hentai
{COMMAND_PREFIX}boobs
{COMMAND_PREFIX}tits
{COMMAND_PREFIX}blowjob
{COMMAND_PREFIX}lewd
{COMMAND_PREFIX}lesbian
{COMMAND_PREFIX}feed
{COMMAND_PREFIX}tickle 
{COMMAND_PREFIX}slap
{COMMAND_PREFIX}hug
{COMMAND_PREFIX}smug
{COMMAND_PREFIX}pat
{COMMAND_PREFIX}kiss

""", value= "บางคําสั่ง18+")

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":

            embed=discord.Embed(
                title='คําสั่งnsfw',
                description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
                color=0x00FFFF   
                )
            embed.add_field(name=f"""

Send photos according to the catergory

{COMMAND_PREFIX}gsolo
{COMMAND_PREFIX}smallboob
{COMMAND_PREFIX}classic
{COMMAND_PREFIX}pussy
{COMMAND_PREFIX}eroyuri
{COMMAND_PREFIX}yuri
{COMMAND_PREFIX}solo
{COMMAND_PREFIX}anal
{COMMAND_PREFIX}erofeet
{COMMAND_PREFIX}feet
{COMMAND_PREFIX}hentai
{COMMAND_PREFIX}boobs
{COMMAND_PREFIX}tits
{COMMAND_PREFIX}blowjob
{COMMAND_PREFIX}lewd
{COMMAND_PREFIX}lesbian
{COMMAND_PREFIX}feed
{COMMAND_PREFIX}tickle 
{COMMAND_PREFIX}slap
{COMMAND_PREFIX}hug
{COMMAND_PREFIX}smug
{COMMAND_PREFIX}pat
{COMMAND_PREFIX}kiss

""", value= "Some commands are 18+")

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def covid19(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get(f'https://disease.sh/v3/covid-19/all')
        r = r.json()

        case = r['cases']
        todaycase = r['todayCases']
        totaldeath = r['deaths']
        todaydeath = r['todayDeaths']
        recover = r['recovered']
        todayRecover = r['todayRecovered']      
        activecase = r['active']

        case = humanize.intcomma(case)
        todaycase = humanize.intcomma(todaycase)
        totaldeath = humanize.intcomma(totaldeath)
        todaydeath = humanize.intcomma(todaydeath)
        recover = humanize.intcomma(recover)
        todayRecover = humanize.intcomma(todayRecover)
        activecase = humanize.intcomma(activecase)

        if server_language == "Thai": 
            embed = discord.Embed(
                colour =0x00FFFF,
                title = "💊สถานะไวรัสโควิด-19 ทั่วโลก",
                description = "เเหล่งที่มา : https://disease.sh/v3/covid-19/all"

            )
            embed.set_thumbnail(url="https://i.imgur.com/kmabvi8.png")

            embed.add_field(name="📊 ยืนยันเเล้ว : ", value=f"{case}")
            embed.add_field(name="💀 เสียชีวิตแล้ว : ", value=f"{totaldeath}")
            embed.add_field(name="✅ รักษาหายแล้ว : ", value=f"{recover}")
            embed.add_field(name="📈 ผู้ติดเชื่อวันนี้ : ", value=f"{case}")
            embed.add_field(name="💀 จำนวนเสียชีวิตวันนี้ : ", value=f"{todaydeath}")
            embed.add_field(name="✅ รักษาหายวันนี้ : ", value=f"{todayRecover}")
            embed.add_field(name="⚠️ ผู้ติดเชื้อ : ", value=f"{activecase}")

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('💊')
        
        if server_language == "English": 
            embed = discord.Embed(
                colour =0x00FFFF,
                title = "💊Covid-19 around the world",
                description = "Source : https://disease.sh/v3/covid-19/all"

            )
            embed.set_thumbnail(url="https://i.imgur.com/kmabvi8.png")

            embed.add_field(name="📊 Total confirm cases : ", value=f"{case}")
            embed.add_field(name="💀 Total death : ", value=f"{totaldeath}")
            embed.add_field(name="✅ Total recover patients : ", value=f"{recover}")
            embed.add_field(name="📈 Total confirm cases today : ", value=f"{todaycase}")
            embed.add_field(name="💀 New death : ", value=f"{todaydeath}")
            embed.add_field(name="✅ Today recover patients : ", value=f"{todayRecover}")
            embed.add_field(name="⚠️ Active cases : ", value=f"{activecase}")

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('💊')
            

@client.command()
async def lmgtfy(ctx, *, message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        r = urlencode({"q": message})
        url = (f'<https://lmgtfy.com/?{r}>')

        if server_language == "Thai": 
            embed= discord.Embed(
                colour =0x00FFFF,
                title= f"ลิงค์ lmgtfy ของคุณ {ctx.author}",
                description = f"{url}"
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English": 
            embed= discord.Embed(
                colour =0x00FFFF,
                title= f"lmgtfy link for {ctx.author}",
                description = f"{url}"
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
    
@lmgtfy.error
async def lmgtfy_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหาใน lmgtfy ``{COMMAND_PREFIX}lmgtfy [message]``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหาใน lmgtfy ``{COMMAND_PREFIX}lmgtfy [message]``"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what to search on lmgtfy ``{COMMAND_PREFIX}lmgtfy [message]``"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
 
@client.command()
async def tweet(ctx, username: str, *, message: str): 
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
                response = await r.json()
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "🕊️ Twitter generator"


                )
                embed.set_image(url=response["message"])
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction('👍')

@client.command()
async def credit(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                title= '💻 เครดิตคนทําบอท',
                description=
                """
        ```ดิสคอร์ด : REACT#1120
        เซิฟดิสคอร์ด : https://discord.com/invite/R8RYXyB4Cg
        Github : https://github.com/reactxsw
                ```
                """,
                colour=0x00FFFF  
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')
        
        if server_language == "English":
            embed = discord.Embed(
                title= '💻 Developer',
                description=
                """
        ```Discord : REACT#1120
        Discord server : https://discord.com/invite/R8RYXyB4Cg
        Github : https://github.com/reactxsw
                ```
                """,
                colour=0x00FFFF  
            )

            message = await ctx.send(embed=embed)
            await message.add_reaction('👍')

@client.command()
async def rps(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

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
                reaction, user = await client.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

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
                reaction, user = await client.wait_for('reaction_add', timeout=10, check=lambda reaction, user: user.id == ctx.author.id)

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

@client.command()
@commands.has_permissions(administrator=True)

async def movetome(ctx, member : discord.Member):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai": 
            if ctx.author.voice and ctx.author.voice.channel:
                await member.move_to(channel=ctx.author.voice.channel)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"{member}ได้ถูกย้ายไปที่ห้องของ {ctx.author}"

                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
            
            else:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` คุณไม่ได้อยู่ในห้องคุย"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        
        if server_language == "English": 
            if ctx.author.voice and ctx.author.voice.channel:
                await member.move_to(channel=ctx.author.voice.channel)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"{member}have been move to {ctx.author} voice chat"

                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

            else:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` You are not connected to voice chat"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def guildicon(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai": 
            embed = discord.Embed(
                colour = 0x00FFFF,
                title=f"เซิฟเวอร์: {ctx.guild.name}")
            embed.set_image(url=ctx.guild.icon_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
        
        if server_language == "English": 
            embed = discord.Embed(
                colour = 0x00FFFF,
                title=f"Server: {ctx.guild.name}")
            embed.set_image(url=ctx.guild.icon_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")

@client.command()
async def avatar(ctx , member : discord.Member=None): 
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        if member is None:
            member = ctx.author

        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai": 

            embed = discord.Embed(
                colour = 0x00FFFF,
                title=f"รูปของสมาชิก: {member}",
                description = f"ลิงค์ : [คลิกที่นี้]({member.avatar_url})")
            embed.set_image(url=member.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")

        if server_language == "English": 

            embed = discord.Embed(
                colour = 0x00FFFF,
                title=f"{member} profile picture",
                description = f"link : [click here]({member.avatar_url})")
            embed.set_image(url=member.avatar_url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")

@client.command()
async def searchavatar(ctx, member: discord.Member=None): 
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        if member is None:
            member = ctx.author

        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai": 
            try:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"หารูปของสมาชิก: {member}",
                    description=f"https://images.google.com/searchbyimage?image_url={member.avatar_url}")
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")
            
            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    title = f"ไม่สามารถหาภาพของสมาชิก{member}ได้"

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("⚠️")
        
        if server_language == "English": 
            try:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"search for {member} profile picture",
                    description=f"https://images.google.com/searchbyimage?image_url={member.avatar_url}")
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")
            
            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    title = f"unable to find {member} profile picture"

                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed)
                await message.add_reaction("⚠️")
    
@client.command()
async def qr(ctx , *,text):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)}"

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "💻 QR CODE GENERATOR",
                description = f"ลิงค์ : [คลิกที่นี้](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)})"
            )
            embed.set_image(url=url)
            await ctx.send(embed=embed)

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "💻 QR CODE GENERATOR",
                description = f"link : [click here](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={urllib.parse.quote_plus(text)})"
            )
            embed.set_image(url=url)
            await ctx.send(embed=embed)

@client.command()
async def meme(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        r = requests.get('https://some-random-api.ml/meme')
        r = r.json()
        url  = r['image']
        cap = r['caption']

        embed=  discord.Embed(
            colour = 0x00FFFF,
            title = f"{cap}"
        )
        embed.set_image(url=url)
        message = await ctx.send(embed=embed)
        await message.add_reaction('😂')

@client.command()
async def geoip(ctx, *, ip):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        ip = str(ip)
        r = requests.get(f'http://extreme-ip-lookup.com/json/{ip}')
        r = r.json()

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title =f"💻 IP {ip}"
            )
            embed.add_field(name="IP",value=f":{r['query']}")
            embed.add_field(name="ประเภทของ IP",value=f":{r['ipType']}")
            embed.add_field(name="ประเทศ",value=f":{r['country']}")
            embed.add_field(name="code ประเทศ",value=f":{r['countryCode']}")
            embed.add_field(name="จังหวัด",value=f":{r['city']}")
            embed.add_field(name="ทวีป",value=f":{r['continent']}")
            embed.add_field(name="ค่ายเน็ท",value=f":{r['isp']}")
            embed.add_field(name="ภูมิภาค",value=f":{r['region']}")
            embed.add_field(name="ชื่อองค์กร",value=f":{r['org']}")
            embed.add_field(name="ชื่อบริษัท",value=f":{r['businessName']}")
            embed.add_field(name="เว็บไซต์บริษัท",value=f":{r['businessWebsite']}")
            embed.add_field(name="ค่า logitude",value=f":{r['lon']}")
            embed.add_field(name="ค่า latitude",value=f":{r['lat']}")

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('💻')

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title =f"💻 IP {ip}"
            )
            embed.add_field(name="IP",value=f":{r['query']}")
            embed.add_field(name="type of IP",value=f":{r['ipType']}")
            embed.add_field(name="country",value=f":{r['country']}")
            embed.add_field(name="country code",value=f":{r['countryCode']}")
            embed.add_field(name="city",value=f":{r['city']}")
            embed.add_field(name="continent",value=f":{r['continent']}")
            embed.add_field(name="isp",value=f":{r['isp']}")
            embed.add_field(name="region",value=f":{r['region']}")
            embed.add_field(name="organization",value=f":{r['org']}")
            embed.add_field(name="businessName",value=f":{r['businessName']}")
            embed.add_field(name="businessWebsite",value=f":{r['businessWebsite']}")
            embed.add_field(name="logitude",value=f":{r['lon']}")
            embed.add_field(name="latitude",value=f":{r['lat']}")

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('💻')

@geoip.error
async def geoip_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` กรุณาระบุ IP ที่ต้องการที่จะค้นหา ``{COMMAND_PREFIX}geoip [IP]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` กรุณาระบุ IP ที่ต้องการที่จะค้นหา ``{COMMAND_PREFIX}geoip [IP]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify an IP to search for ``{COMMAND_PREFIX}geoip [IP]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
@qr.error
async def qr_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่จะเขียนใน QR code ``{COMMAND_PREFIX}qr [message]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่จะเขียนใน QR code ``{COMMAND_PREFIX}qr [message]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            else:
                print(error)
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what to write on QR code ``{COMMAND_PREFIX}qr [message]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')


@tweet.error
async def tweet(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งชื่อเเละสิ่งที่จะเขียนในโพส twitter ``{COMMAND_PREFIX}tweet [username] [message]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งชื่อเเละสิ่งที่จะเขียนในโพส twitter ``{COMMAND_PREFIX}tweet [username] [message]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what to write on the twitter post ``{COMMAND_PREFIX}tweet [username] [message]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
@movetome.error
async def movetome_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}movetome @member``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์เเอดมิน",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️') 
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}movetome @member``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์เเอดมิน",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )
                
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️') 
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a member to move ``{COMMAND_PREFIX}movetome @member``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            if isinstance(error, commands.MissingPermissions):
                if isinstance(error, commands.MissingPermissions):
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = "You don't have permission",
                        description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                    )

                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')


@client.command()
async def wasted(ctx, member: discord.Member=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "💀 Wasted!",
                description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💀')
        
        if server_language == "English":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "💀 Wasted!",
                description = f"link: [click here](https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/wasted/?avatar={avatar_url})")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💀')

@client.command()
async def gay(ctx, member: discord.Member=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "🏳️‍🌈 Gay!" , 
                description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/gay/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/gay/?avatar={avatar_url}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('🏳️‍🌈')
        
        if server_language == "English":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "🏳️‍🌈 Gay!" , 
                description = f"link: [click here](https://some-random-api.ml/canvas/gay/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/gay/?avatar={avatar_url}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('🏳️‍🌈')

@client.command()
async def trigger(ctx, member: discord.Member=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "😠 Triggered",
                description = f"ลิงค์: [คลิกที่นี้](https://some-random-api.ml/canvas/triggered/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/triggered/?avatar={avatar_url}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('😠')

        if server_language == "English":
            if member is None:
                member = ctx.author

            avatar_url = member.avatar_url_as(format="png")

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "😠 Triggered",
                description = f"link: [click here](https://some-random-api.ml/canvas/triggered/?avatar={avatar_url})"
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=f"https://some-random-api.ml/canvas/triggered/?avatar={avatar_url}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('😠')

@client.command()
async def timer(ctx, second : int):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            number = second
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับถอยหลัง {second} วินาที",
                    description = f"{number}"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            while number >= 0:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับถอยหลัง {second} วินาที",
                    description = f"```{number}```"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                number = number - 1 
                time.sleep(1)
                await message.edit(embed=embed)

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"⏱️ นับถอยหลัง {second} วินาที",
                description = "เสร็จ"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await message.edit(embed=embed)
        
        if server_language == "Thai":

            number = second
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ countdown for {second} second",
                    description = f"{number}"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            while number >= 0:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ countdown for {second} second",
                    description = f"```{number}```"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                number = number - 1 
                time.sleep(1)
                await message.edit(embed=embed)

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"⏱️ countdown for {second} second",
                description = "Finished"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await message.edit(embed=embed)

@timer.error
async def timer_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับถอยหลัง ``{COMMAND_PREFIX}timer (second)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับถอยหลัง ``{COMMAND_PREFIX}timer (second)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify how long to countdown ``{COMMAND_PREFIX}timer (second)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def count(ctx, second : int):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            number = 0
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = f"{number}"
                )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            while number <= second:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = f"```{number}```"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                number = number + 1 
                time.sleep(1)
                await message.edit(embed=embed)

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"⏱️ นับเลขถึง {second} วินาที",
                description = "เสร็จ"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await message.edit(embed=embed)
        
        if server_language == "English":
            number = 0
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = f"{number}"
                )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            while number <= second:
                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"⏱️ นับเลขถึง {second} วินาที",
                    description = f"```{number}```"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                number = number + 1 
                time.sleep(1)
                await message.edit(embed=embed)

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"⏱️ นับเลขถึง {second} วินาที",
                description = "เสร็จ"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await message.edit(embed=embed)

@client.command()
async def upper(ctx, *, message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            big = message.upper()
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "UPPERCASE GENERATOR",
                description = f"""```
ข้อความปกติ : {message}
ข้อความตัวพิมพ์ใหญ่ : {big}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)
        
        if server_language == "English":
            big = message.upper()
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "UPPERCASE GENERATOR",
                description = f"""```
Normal text : {message}
Uppercase text : {big}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)

@upper.error
async def upper_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมใหญ่ ``{COMMAND_PREFIX}upper (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมใหญ่ ``{COMMAND_PREFIX}upper (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what to make into uppercase ``{COMMAND_PREFIX}upper (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def lower(ctx, *, message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            lower = message.lower()
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "LOWERCASE GENERATOR",
                description = f"""```
ข้อความปกติ : {message}
ข้อความตัวพิมพ์ใหญ่ : {lower}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)
        
        if server_language == "English":
            lower = message.lower()
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "LOWERCASE GENERATOR",
                description = f"""```
Normal text : {message}
Lowercase text : {lower}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)

@lower.error
async def lower_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมเล็ก ``{COMMAND_PREFIX}lower (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมเล็ก ``{COMMAND_PREFIX}lower (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what to make into lowercase ``{COMMAND_PREFIX}lower (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def reverse(ctx, *, message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":

            reverse = message[::-1]
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "REVERSE GENERATOR",
                description = f"""```
ข้อความปกติ : {message}
ข้อความกลับหลัง : {reverse}```"""
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)
        
        if server_language == "English":

            reverse = message[::-1]
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "REVERSE GENERATOR",
                description = f"""```
Normal text : {message}
Reverse text : {reverse}```"""
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)

@reverse.error
async def reverse_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะกลับด้าน ``{COMMAND_PREFIX}reverse (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะกลับด้าน ``{COMMAND_PREFIX}reverse (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what to reverse ``{COMMAND_PREFIX}reverse (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@count.error
async def count_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับ ``{COMMAND_PREFIX}count (second)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับ ``{COMMAND_PREFIX}count (second)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify how long to coun ``{COMMAND_PREFIX}count (second)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def apexstat(ctx, username):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        url = f"https://public-api.tracker.gg/v2/apex/standard/profile/origin/{username}"
        try:
            r = requests.get(url, headers=headers)
        
        except:
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}``API มีปัญหา ``{COMMAND_PREFIX}apexstat (username)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

        r = r.json()

        platform = r["data"]["platformInfo"]["platformSlug"]
        username = r["data"]["platformInfo"]["platformUserId"]
        avatar = r["data"]["platformInfo"]["avatarUrl"]
        level = r["data"]["segments"][0]["stats"]["level"]["value"]
        kills = r["data"]["segments"][0]["stats"]["kills"]["value"]

        level = int(level)
        kills = int(kills)
        kills = humanize.intcomma(kills)

        if server_language == "Thai":
            embed= discord.Embed(
                colour = 0x00FFFF,
                title = f"🎮 Stat เกม apex legend ของ {username}",
                description =f"""```
💻 เพลตฟอร์ม : {platform}
👀 ชื่อในเกม : {username}
📁 เลเวลในเกม : {level}
🔫 ฆ่าทั้งหมด : {kills}```
            """)

            embed.set_thumbnail(url=avatar)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction('🎮')
        
        if server_language == "English":
            embed= discord.Embed(
                colour = 0x00FFFF,
                title = f"🎮 apex legend stat of {username}",
                description =f"""```
💻 Platform : {platform}
👀 Username : {username}
📁 Level : {level}
🔫 Kills : {kills}```
            """)

            embed.set_thumbnail(url=avatar)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            
            message = await ctx.send(embed=embed)
            await message.add_reaction('🎮')

@apexstat.error
async def apexstat_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมใส่ชื่อของผู้เล่น ``{COMMAND_PREFIX}apexstat (username)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมใส่ชื่อของผู้เล่น ``{COMMAND_PREFIX}apexstat (username)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a username ``{COMMAND_PREFIX}apexstat (username)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def captcha(ctx, *, text):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            image = ImageCaptcha()
            image.write(text, 'captcha.png')
            file = discord.File("captcha.png", filename="captcha.png")

            embed = discord.Embed(
                colour  = 0x00FFFF,
                title = "Captcha"
            )
            embed.set_image(url = "attachment://captcha.png")
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await ctx.send(embed=embed , file=file)

        if server_language == "English":
            image = ImageCaptcha()
            image.write(text, 'captcha.png')
            file = discord.File("captcha.png", filename="captcha.png")

            embed = discord.Embed(
                colour  = 0x00FFFF,
                title = "Captcha"
            )
            embed.set_image(url = "attachment://captcha.png")
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            await ctx.send(embed=embed , file=file)

@captcha.error
async def captcha_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมคําที่จะทําเป็น captcha ``{COMMAND_PREFIX}captcha (word)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมคําที่จะทําเป็น captcha ``{COMMAND_PREFIX}captcha (word)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify text to make into captcha ``{COMMAND_PREFIX}captcha (word)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
 
@client.command()
async def anal(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/anal")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "Anal"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def smallboob(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/smallboobs")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "smallboobs"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def gsolo(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/solog")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "Girl solo"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def erofeet(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/erofeet")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "erofeet"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')
    
@client.command()
async def feet(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/feetg")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "feet"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def pussy(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/pussy_jpg")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "pussy"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def hentai(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/Random_hentai_gif")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "hentai"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def eroyuri(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/eroyuri")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "eroyuri"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def yuri(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/yuri")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "yuri"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def solo(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/solo")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "solo"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def classic(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/classic")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "classic"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def boobs(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/boobs")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "boobs"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def tits(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/tits")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "tits"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def blowjob(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/blowjob")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "blowjob"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)   
        await message.add_reaction('❤️')

@client.command()
async def lewd(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/nsfw_neko_gif")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "lewd"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}") 

        message = await ctx.send(embed=embed)  
        await message.add_reaction('❤️') 

@client.command()
async def lesbian(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/les")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "lesbian"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')   

@client.command()  
async def feed(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/feed")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "feed"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def tickle(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:  
        r = requests.get("https://nekos.life/api/v2/img/tickle")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "tickle"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def slap(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:  
        r = requests.get("https://nekos.life/api/v2/img/slap")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "slap"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def hug(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/hug")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "hug"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def smug(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/smug")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "smug"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def pat(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/pat")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "pat"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')

@client.command()
async def kiss(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 
        r = requests.get("https://nekos.life/api/v2/img/kiss")
        r = r.json()
        embed = discord.Embed(
            colour = 0xFC7EF5,
            title = "kiss"

        )   
        url = r['url']
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)  
        await message.add_reaction('❤️')

@client.command()
async def weather(ctx, *, city):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            try:
                r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermapAPI}')
                r = r.json()
                temperature = (float(r['main']['temp']) -273.15)
                feellike = (float(r['main']['feels_like']) -273.15)
                highesttemp = (float(r['main']['temp_max']) -273.15)
                lowesttemp = (float(r['main']['temp_min']) -273.15)
                humidity = float(r['main']['humidity'])
                windspeed = float(r['wind']['speed'])
                
                day = r['weather'][0]['description']

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"สภาพอากาศในจังหวัด {city}",
                    description = f"""```
        อุณหภูมิตอนนี้ : {temperature}°C
        อุณหภูมิสูงสุดของวัน : {highesttemp}°C
        อุณหภูมิตํ่าสุดของวัน : {lowesttemp}°C
        อุณหภูมิรู้สึกเหมือน : {feellike}
        ความชื้น : {humidity}%
        ความเร็วลม : {windspeed}mph
        สภาพอากาศ : {day}```
                    """
                    
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` ไม่มีจังหวัดนี้กรุณาตรวจสอบตัวสะกด ``{COMMAND_PREFIX}weather (city)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            try:
                r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermapAPI}')
                r = r.json()
                temperature = (float(r['main']['temp']) -273.15)
                feellike = (float(r['main']['feels_like']) -273.15)
                highesttemp = (float(r['main']['temp_max']) -273.15)
                lowesttemp = (float(r['main']['temp_min']) -273.15)
                humidity = float(r['main']['humidity'])
                windspeed = float(r['wind']['speed'])
                
                day = r['weather'][0]['description']

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = f"weather in {city}",
                    description = f"""```
        Temperature now : {temperature}°C
        Highest temperature today : {highesttemp}°C
        Lowest temperature today : {lowesttemp}°C
        Feel like : {feellike}
        Humidity : {humidity}%
        windspeed : {windspeed}mph
        Weather : {day}```
                    """
                    
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                await ctx.send(embed=embed)

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` Cannot find this city ``{COMMAND_PREFIX}weather (city)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@weather.error
async def weather_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อจังหวัดที่จะดู ``{COMMAND_PREFIX}weather (city)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อจังหวัดที่จะดู ``{COMMAND_PREFIX}weather (city)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อจังหวัดที่จะดู ``{COMMAND_PREFIX}weather (city)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def bird(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/birb")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพนก"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐦')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="Bird"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐦')

@client.command()
async def panda(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/panda")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพเเพนด้า"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐼')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="Panda"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐼')

@client.command()
async def cat(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/cat")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพเเมว"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐱')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพเเมว"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐱')

@client.command()
async def dog(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/dog")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพหมา"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐶')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="Dog"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐶')

@client.command()
async def fox(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/fox")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพสุนัขจิ้งจอก"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🦊')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="Fox"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🦊')

@client.command()
async def koala(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get("https://some-random-api.ml/img/koala")
        r = r.json()
        url = r['link']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="ภาพหมีโคอาล่า"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐨')

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title="Koala"

            )
            embed.set_image(url=url)
            message = await ctx.send(embed= embed)
            await message.add_reaction('🐨')

@client.command()
async def country(ctx, *, country):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get(f"https://restcountries.eu/rest/v2/name/{country}?fullText=true")
        r = r.json()

        name = r[0]['name']
        population = r[0]['population']
        area = r[0]['area']
        capital = r[0]['capital']
        subregion = r[0]['subregion']
        nativename = r[0]['nativeName']
        timezone = r[0]['timezones'][0]
        currency = r[0]['currencies'][0]['name']
        symbol = r[0]['currencies'][0]['symbol']
        language = r[0]['languages'][0]['name']
        code = r[0]['alpha2Code']
        codephone = r[0]['callingCodes'][0]

        population = humanize.intcomma(population)
        area =humanize.intcomma(area)

        codelower = code.lower()

        flag = (f"https://flagcdn.com/256x192/{codelower}.png")

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"{name}",
                description = f"""```

        ชื่อพื้นเมือง : {nativename}
        โค้ดประเทศ : {code}
        รหัสโทร : {codephone}
        ภูมิภาค : {subregion}
        ประชากร : {population} คน
        เมืองหลวง : {capital}
        พื้นที่ : {area} km²
        เขตเวลา : {timezone}
        สกุลเงิน : {currency} สัญลักษณ์ : ({symbol})
        ภาษา : {language}```""")

            embed.set_thumbnail(url=flag)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            await message.add_reaction('😊')

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"{name}",
                description = f"""```

        Native name : {nativename}
        country code : {code}
        calling code : {codephone}
        subregion : {subregion}
        population : {population} peoples
        capital city : {capital}
        area : {area} km²
        timezone : {timezone}
        currency : {currency} symbol : ({symbol})
        language : {language}```""")

            embed.set_thumbnail(url=flag)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)

            await message.add_reaction('😊')

@country.error
async def country_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อประเทศที่จะดู ``{COMMAND_PREFIX}country (country)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อประเทศที่จะดู ``{COMMAND_PREFIX}country (country)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a country to search ``{COMMAND_PREFIX}country (country)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def pingweb(ctx, website = None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai": 
            if website is None: 
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมเว็บที่จะดู ``{COMMAND_PREFIX}pingweb (website)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            else:
                try:
                    r = requests.get(website).status_code
                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` เว็บอาจไม่ถูกต้อง ``{COMMAND_PREFIX}pingweb (website)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                    
                if r == 404:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"สถานะของเว็บไซต์ {website}",
                        description = f" ⚠️`` เว็บไซต์ไม่ออนไลน์```")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️') 

                else:
                    embed = discord.Embed(
                        colour = 0x75ff9f,
                        title = f"สถานะของเว็บไซต์ {website}",
                        description = f"```เว็บไซต์ออนไลน์ปกติ```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed )
        
        if server_language == "English": 
            if website is None: 
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a website to search ``{COMMAND_PREFIX}pingweb (website)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            else:
                try:
                    r = requests.get(website).status_code
                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` Unable to find the website ``{COMMAND_PREFIX}pingweb (website)``"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️')
                    
                if r == 404:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"Status of {website}",
                        description = f" ⚠️`` Website is offline```")
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed ) 
                    await message.add_reaction('⚠️') 

                else:
                    embed = discord.Embed(
                        colour = 0x75ff9f,
                        title = f"Status of {website}",
                        description = f"``` Website is online```"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed )

@client.command()
async def rb6rank(ctx , username):
    url = f"https://r6.tracker.network/profile/pc/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
            try:
                div = soupObject.find_all('div', class_='trn-defstat__value')[0]
                div1 = soupObject.find_all('div', class_='trn-defstat__value')[1]
                div2 = soupObject.find_all('div', class_='trn-defstat__value')[2]
                div3 = soupObject.find_all('div', class_='trn-defstat__value')[3]
                div4 = soupObject.find_all('div', class_='trn-text--dimmed')[2]
                platform = "PC"
                try:
                    div5 = soupObject.find_all('div', class_='trn-text--primary')[0]
                                
                except:
                    ranking = None
            
            except:
                try:
                    url = f"https://r6.tracker.network/profile/xbox/{username}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            soupObject = BeautifulSoup(await response.text(), "html.parser")
                            div = soupObject.find_all('div', class_='trn-defstat__value')[0]
                            div1 = soupObject.find_all('div', class_='trn-defstat__value')[1]
                            div2 = soupObject.find_all('div', class_='trn-defstat__value')[2]
                            div3 = soupObject.find_all('div', class_='trn-defstat__value')[3]
                            div4 = soupObject.find_all('div', class_='trn-text--dimmed')[2]
                            platform = "XBOX"
                            try:
                                div5 = soupObject.find_all('div', class_='trn-text--primary')[0]
                                
                            except:
                                ranking = None
                            
                except:
                    try:
                        url = f"https://r6.tracker.network/profile/psn/{username}"
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                soupObject = BeautifulSoup(await response.text(), "html.parser")
                                div = soupObject.find_all('div', class_='trn-defstat__value')[0]
                                div1 = soupObject.find_all('div', class_='trn-defstat__value')[1]
                                div2 = soupObject.find_all('div', class_='trn-defstat__value')[2]
                                div3 = soupObject.find_all('div', class_='trn-defstat__value')[3]
                                div4 = soupObject.find_all('div', class_='trn-text--dimmed')[2]
                                platform = "PSN"
                                try:
                                    div5 = soupObject.find_all('div', class_='trn-text--primary')[0]
                                
                                except:
                                    ranking = None
                                
                    except:
                        embed = discord.Embed(
                            colour = 0x983925,
                            description = f" ⚠️ไม่สามารถค้นหาชื่อของตัวละครได้โปรดเช็คตัวสะกด")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed ) 
                        await message.add_reaction('⚠️')
            
            level = div.contents
            highestmmr = div1.contents
            rank = div2.contents
            avgmmr = div3.contents
            mmr = div4.contents
            try:
                ranking = div5.contents
            except:
                ranking = None
            
            space = " "

            try:
                ranking = space.join(ranking)
                level = space.join(level)
                highestmmr = space.join(highestmmr)
                rank = space.join(rank)  
                avgmmr =space.join(avgmmr)
                mmr = space.join(mmr)
                ranking = None

            except:
                level = None
                highestmmr = None
                rank = None
                avgmmr = None
                mmr = None

            embed = discord.Embed(
                colour = 0x1e1e1f,
                title = f"{username}",
                description = f"ข้อมูลเเรงค์ของ {username} ใน {platform}"
            )     

            try:
                if "," in mmr:
                    mmr = mmr[:-3]
                    mmrint = mmr.replace(',', '')
                    mmrint = int(mmrint)

                if mmrint <= 1100:

                    imageurl = "https://i.imgur.com/wSCcUKn.png"
            
                elif mmrint >= 1200 and mmrint < 1300: # bronze 4

                    imageurl = "https://i.imgur.com/FwXHG5a.png"

                elif mmrint >= 1300 and mmrint < 1400: # bronze 3

                    imageurl = "https://i.imgur.com/HSaFvGT.png"
            
                elif mmrint >= 1400 and mmrint < 1500: # bronze 2

                    imageurl = "https://i.imgur.com/UQfxmme.png"

                elif mmrint >= 1500 and mmrint < 1600: # bronze 1

                    imageurl = "https://i.imgur.com/FC4eexb.png"

                elif mmrint >= 1600 and mmrint < 1700: # copper 5

                    imageurl = "https://i.imgur.com/KaFUckV.png"
            
                elif mmrint >= 1700 and mmrint < 1800: # copper 4

                    imageurl = "https://i.imgur.com/Ae1TVw1.png"
            
                elif mmrint >= 1800 and mmrint < 1900: # copper 3

                    imageurl = "https://i.imgur.com/wUyjfJU.png"
            
                elif mmrint >= 1900 and mmrint < 2000: # copper 2

                    imageurl = "https://i.imgur.com/Wuh4Yyh.png"

                elif mmrint >= 2000 and mmrint < 2100: # copper 1

                    imageurl = "https://i.imgur.com/8EwVqaf.png"

                elif mmrint >= 2100 and mmrint < 2200: # silver 5

                    imageurl = "https://i.imgur.com/papk0fC.png"
            
                elif mmrint >= 2200 and mmrint < 2300: # silver 4

                    imageurl = "https://i.imgur.com/dA1fkCP.png"
            
                elif mmrint >= 2300 and mmrint < 2400: # silver 3

                    imageurl = "https://i.imgur.com/ECXMkOM.png"
            
                elif mmrint >= 2400 and mmrint < 2500: # silver 2

                    imageurl = "https://i.imgur.com/wXsdvT2.png"

                elif mmrint >= 2500 and mmrint < 2600: # silver 1

                    imageurl = "https://i.imgur.com/iGPlsPP.png"
            
                elif mmrint >= 2600 and mmrint < 2800: # gold 3

                    imageurl = "https://i.imgur.com/aZKtpwt.png"
            
                elif mmrint >= 2800 and mmrint < 3000: # gold 2

                    imageurl = "https://i.imgur.com/3q4UzA0.png"
            
                elif mmrint >= 3000 and mmrint < 3200: # gold 1

                    imageurl = "https://i.imgur.com/ysYFyJN.png"
            
                elif mmrint >= 3200 and mmrint < 3600: # platinum 3

                    imageurl = "https://i.imgur.com/qOTqbzM.png"

                elif mmrint >= 3600 and mmrint < 4000: # platinum 2

                    imageurl = "https://i.imgur.com/8x83kyv.png"
            
                elif mmrint >= 4000 and mmrint < 4400: # platinum 1

                    imageurl = "https://i.imgur.com/HFOlYzY.png"

                elif mmrint >= 4000 and mmrint < 4400: # diamond

                    imageurl = "https://i.imgur.com/ZRq9KjK.png"

                elif mmrint >= 5000:

                    imageurl = "https://i.imgur.com/d36RkX2.png"
                
            except:

                imageurl = "https://i.imgur.com/yzkK5um.png"

            embed.add_field(name='**'+"Rank"+'**',value=f"{rank}")
            embed.add_field(name='**'+"MMR"+'**',value=f"{mmr}")
            embed.add_field(name='**'+"MMR เฉลี่ย"+'**',value=f"{avgmmr}")
            embed.add_field(name='**'+"MMR สูงสุด"+'**',value=f"{highestmmr}")
            embed.add_field(name='**'+"อันดับ"+'**',value=f"{ranking}")
            embed.add_field(name='**'+"Level"+'**',value=f"{level}")
            embed.set_thumbnail(url=imageurl)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('🎮')

@rb6rank.error
async def rb6rank_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อของผู้เล่นที่จะดู ``{COMMAND_PREFIX}rb6rank (username)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def iphonex(ctx , image=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 

        if image is None:
            image = ctx.author.avatar_url

        r = requests.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={image}")
        r = r.json()

        url = r['message']

        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "Iphone X"

        )
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('📱')

@client.command()
async def phcomment(ctx , * ,text, username = None , image=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else: 

        if image is None:
            image = ctx.author.avatar_url

        if username is None:
            username = ctx.author

        r = requests.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&image={image}&text={text}&username={username}")
        r = r.json()

        url = r['message']

        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "Pornhub"

        )
        embed.set_image(url=url)
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('📱')

@phcomment.error
async def phcomment_error(ctx,error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้อง text ที่จะใส่ใน comment``{COMMAND_PREFIX}phcomment (text)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้อง text ที่จะใส่ใน comment``{COMMAND_PREFIX}phcomment (text)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a text to put as comment ``{COMMAND_PREFIX}phcomment (text)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

                

@client.command()
async def slim(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        quoteslim = ["ไม่ใช่สลิ่มนะ แต่...",
                    "ไม่ใช่ติ่งลุงตู่ แต่..."
                    "เราคนไทยเหมือนกัน",
                    "ไม่มี REDACTED ประเทศไทยจะพัฒนามาถึงจุดนี้หรือ,",
                    "รักชาติ ศาสน์ กษัตริย์",
                    "ไอ้ทอน",
                    "ตี๋ทอน",
                    "ไอ้บุตร",
                    "ปีแยร์บูด",
                    "กะปิบูด",
                    "อีช่อ",
                    "อีฉ้อ",
                    "ชังชาติ",
                    "ขายชาติ",
                    "ไม่สำนึกในบุญคุณ ",
                    "หนักแผ่นดิน",
                    "เนรคุณแผ่นดิน",
                    "เราคือผู้อยู่อาศัย ไม่ใช่เจ้าของบ้าน",
                    "ล้มเจ้า",
                    "ส้มเน่า",
                    "เผาไทย",
                    "ลิเบอร่าน",
                    "คณะร่าน",
                    "เห่อหมอยคลั่งชาติฝรั่ง",
                    "ขุ่นพ่อง",
                    "รังนกสีฟ้า",
                    "เก่งอยู่หลังคีย์บอร์ด",
                    "ต่างชาติชักใยอยู่เบื้องหลัง",
                    "ชักศึกเข้าบ้าน",
                    "มีทุกอย่างที่ดีเพราะใคร ฉันจะไม่ลืม​",
                    "พวกเผาบ้านเผาเมือง",
                    "จำนำข้าว",
                    "เป็นคนปลอมตัวมาสร้างสถานการณ์ค่ะ คนเสื้อเหลืองไม่มีใครทำแบบนั้น",
                    "ศูนย์รวมจิตใจของชาติ",
                    "ให้มันจบที่เรือนจำ",
                    "ตอบแทนบุญคุณแผ่นดิน",
                    "ควายแดง",
                    "สวะส้ม",
                    "ด่าทุกเรื่องที่รัฐออกนโยบาย แต่ลงทะเบียนทุกอย่างที่รัฐแจกให้ฟรี",
                    "ไอแม้ว",
                    "ฟังคำเตือนจากผู้ใหญ่บ้าง",
                    "ไม่รักชาติก็ออกจากประเทศไป",
                    "เด็กๆพวกนี้มันคิดเองไม่ได้หรอก โดนหลอกกันมาทั้งนั้น",
                    "ไม่พอใจก็ไปอยู่ประเทศอื่น",
                    "ไม่ได้อยู่ฝั่งไหน",
                    "ด่ารัฐบาลก็ด่าไป อย่าไปวุ่นวายกับเบื้องสูง​",
                    "อาบน้ำร้อนมาก่อน",
                    "พวกหัวรุนแรง",
                    "ไร้ซึ่งจริยธรรม",
                    "โดนจูงจมูก",
                    "ลุงเป็นคนดี แค่เข้ามาผิดเวลา",
                    "เป็นกลาง ไม่เลือกข้าง",
                    "พวกอันธพาล ไม่พอใจก็ลงถนน​",
                    "ต้องเริ่มต้นที่ตัวเองก่อน",
                    "พวกขี้ข้าทักษิณ",
                    "ซ้ายจัดดัดจริต",
                    "โง่ไม่มีสมอง",
                    "ไม่เคารพผู้หลักผู้ใหญ่",
                    "เป็นบุคคลสาธารณะ อย่าพูดเรื่องการเมือง",
                    "นำชีวิตตัวเองยังทำให้ได้ดีไม่ได้",
                    "ไปทำหน้าที่ตัวเองให้ดีก่อน",
                    "ทำไมไม่ยืน",
                    "อย่าทำให้บ้านเมืองเดือดร้อน",
                    "จาบจ้วงสถาบัน",
                    "ประชามติ 16.8 ล้านเสียง",
                    "บังอาจก้าวล่วง",
                    "ทำร้ายจิตใจคนไทย",
                    "เป็นอันตรายต่อความมั่นคงของประเทศชาติ",
                    "รัฐมิได้ใช้ความรุนแรง",
                    "หยุดสร้างความแตกแยก",
                    "ขี้ข้าไอ้ทอน",
                    "ลุงมาจากการเลือกตั้ง",
                    "เชียร์ลุง",
                    "#อนุชนรักชาติศาสน์กษัตริย์",
                    "ที่มีแผ่นดินอยู่ทุกวันนี้เพราะใคร",
                    "ม๊อบสวะ",
                    "ทำประโยชน์อะไรให้ชาติบ้านเมืองบ้าง",
                    "ไอ้เจ็กกบฎ",
                    "แปะสติ๊กเกอร์ ซาลาเปา &​ ",
                    "โดนไอ้แม้วซื้อไปแล้ว",
                    "รับไปห้าร้อย",
                    "ประชาธิปไตยต้องเคารพกฎหมา",
                    "เขาแค่ทำตามที่กฏหมายห้ามเท่านั้น",
                    "นักการเมืองก็โกงเหมือนกันทุกคน",
                    "ลุงตู่เป็นคนดี",
                    "ลุงตู่อยู่บ้านเมืองสงบ",
                    "บ้านเมืองสงบ จบที่ลุงตู่",
                    "ระบอบทักษิณ",
                    "สมบูรณาญาสิทธิทุน",
                    "นี่คือการปฏิวัติที่อ่อนละมุน",
                    "รัฐประหารโดยสันติวิธี",
                    "Unfortunately, some people died.",
                    "คนดี ถึงจะเป็นเผด็จการ ก็เป็นเผด็จการที่ดี",
                    "ก็ไม่ได้ชอบลุงตู่นะ แต่ถ้าจะให้ไอ้ทอนมาเป็น ยังไงลุงตู่ก็ดีกว่า",
                    "หนึ่งคือนายกฯ รักประเทศชาติ, สองคือนายกฯ รักพระมหากษัตริย์, สามคือนายกจริงใจ และทำเพื่อประเทศไทยจริง ๆ",
                    "มึงมาไล่ดูสิ",
                    "ลูกหลานอยู่ไม่ได้วันหน้า ก็โทษพ่อมันนั่นแหละ",
                    "ถ้ารุนแรงคงมีคนตายไปแล้ว",
                    "ไปให้ตำรวจยิงหรอ",
                    "จะกี่รัฐบาลก็เหมือนกันหมด",
                    "เอาเวลาไปหาเงินเลี้ยงปากท้องเถอะ",
                    "เก่งมากก็ไปเป็นนายกฯเองสิ",
                    "แค่รถฉีดน้ำจะไปกลัวทำไม เขาทำตามหลักสากล",
                    "ท่านทรงงานหนัก",
                    "โดนแค่ฉีดน้ำทำเป็นบ่น ตอนนั้น กปปส โดนแก๊สน้ำตานะ",
                    "หัวก้าวหน้า ปัญญาล้าหลัง",
                    "สัตว์นรก",
                    "คนไทยทั้งประเทศ",
                    "ขอพูดแรงๆ ซักครั้งในชีวิต พูดแล้วอยากจะร้องไห้​",
                    "จะเปลี่ยนแปลงประเทศ ช่วยพ่อแม่ล้างจานหรือยัง",
                    "ถ้าคนไทยฆ่ากันเอง จะร้องเพลงชาติไทยให้ใครฟัง",
                    "ถ้าพวกมึงเป็นอะไรขึ้นมา คิดว่าพ่อนักการเมืองของมึงเขาจะมาช่วยเหรอ",
                    "เห็นเราเงียบ ใช่ว่าเราจะไม่รู้สึก คุณด่าพ่อเรา เราเสียใจนะ",
                    "ถ้าพ่อมองลงมา พ่อจะรู้สึกยังไง",
                    "พวกคอมมิวนิสต์",
                    "อยากได้เสรีภาพมากเกินไป",
                    "วันๆ เอาแต่เรียกร้องเสรีภาพ ถึงไม่รู้ไงว่าท่านทำอะไรบ้าง",
                    "หัดศึกษาประวัติศาสตร์บ้างนะ",
                    "ถอยกันคนละก้าว",
                    "เจ้าจะทำอะไรก็เรื่องของเค้า",
                    "จ่ายภาษีหรือเปล่า",
                    "ม็อบมุ้งมิ้ง",
                    "ทำไมไม่เคารพความเห็นต่าง",
                    "เป็น นร ก็กลับไปตั้งใจเรียนหนังสือ",
                    "เด็กๆเอาแต่เล่นโซเชียล fake news ทั้งนั้น",
                    "รัฐบาลมีผลงานเยอะแยะ แค่ข่าวไม่ออกเท่านั้นแหละ",
                    "คิดต่างได้ แต่ต้องมีสถาบัน",
                    "รักประยุทธ์ ก็ยังดีกว่าโดนล้างสมอง",
                    "อยู่อย่างจงรัก ตายอย่างภักดี ปกป้องสถาบัน",
                    "ไปฟังคนไม่จบ ม.6 มันพูดทำไม",
                    "ก่อนจะสานต่ออุดมการณ์เพื่อชาติ วันนี้ช่วยแม่ทำงานบ้าน กรอกน้ำใส่ตู้เย็นหรือยัง",
                    "ขยันอ่านหนังสือสอบให้เหมือนอ่านเบิกเนตรหรือยัง",
                    "คุณภาพชีวิตจะดีขึ้น ถ้าคนเป็นคนดี ถ้าตัวเราดี",
                    "แล้วที่หลานทำไม่เรียกว่าคุกคาม��ถาบันหรือ",
                    "เป็น IO ดีกว่าเป็นควายให้ไอ้แม้วไอ้ทอนจูงจมูก",
                    "ทำร้ายตำรวจ ด้วยคีมเหล็กขนาดใหญ่",
                    "พวกเนตรนารีคุกคามเราก่อน",
                    "เขามองพวกผมด้วยสายตาล้มสถาบัน",
                    "เยาวชนปลดแอ๊ก",
                    "ประชาธิปไตยแดกได้เหรอ",
                    "ควรอยู่อย่างพอเพียงนะ",
                    "เศรษฐกิจก็ดีอยู่แล้วนี่ เห็นคนซื้อนั่นซื้อนี่",
                    "ไอทอนมันมาทำให้ประเทศวุ่นวาย",
                    "อย่าไปดูการเมืองมาก มันปั่น",
                    "ดีจ๊ะหนู พ่อแม่คงภูมิใจมาก",
                    "รู้ทุกเรื่อง ยกเว้นเรื่องตนเอง หน้าที่ของตนเอง",
                    "ตบเสียบ้างก็ดีเหมือนกัน เด็กสมัยนี้ไม่รู้กินอะไรเข้าไป",
                    "ไอ้บูดจงพินาศ ประชาชาติจงพ้นภัย",
                    "ผมก็ว่าเนชั่นเป็นกลางสุดแล้วในการเสนอข่าว ไม่ได้อวยใดๆพูดตามเนื้อผ้าครับ",
                    "สร้างแต่ปัญหาให้ลุงตู่ แผนตื้นๆยังไปติดกับดัก",
                    "ไม่เอาต่างชาติเป็นนาย",
                    "เหยียบย่ำหัวใจคนไทย",
                    "ชู 3 นิ้ว กูเอามึงตายเลย",
                    "เราว่าลุงไม่เก่งนะ แต่ลุงไม่โกง",
                    "มันทำได้แม้กระทั่ง ปารองเท้าปาขวดเขย่ารถพระที่นั่ง!!",
                    "ไม่ภูมิใจเหรอ ที่ได้ตอบแทนคุณแผ่นดิน",
                    "เราไม่ได้สนใจอ่ะนะ เราต้องทำงาน ถ้าไม่ทำงาน ก็ไม่มีแดก",
                    "อย่าอ้างคำว่าประชาธิปไตยแล้วทำร้ายหัวใจคนทั้งชาติ",
                    "ผมไม่ใช่สลิ่มนะ แต่ผมว่าป้าม่วงไม่ผิด",
                    "โปรดอย่าบิดเบือนความจริงไปมากกว่านี้เลย มันเจ็บ...",
                    "3 แสนเสียงใน กทม. แต่เป็นเสียงที่มีคุณภาพ ย่อมดีกว่า 15 ล้านเสียงใน ตจว. แต่ไร้คุณภาพ",
                    "แน่จริงเรียนให้จบ มีเงินเดือน มีรายได้แล้วค่อยบอกว่าภาษีกู",
                    "จ่ายแค่ VAT 7% แล้วยังมาเรียกตัวเองว่าผู้เสียภาษี",
                    "ประเทศชาติจะดีขึ้นถ้าทุกคนหาเลี้ยงตัวเองได้",
                    "เด็กๆถ้าอยากเห็นอนาคตที่ดีอะ คุณต้องให้ประเทศชาติมีความมั่นคงก่อน อย่าขายชาติ",
                    "รังเกียจสถาบัน แล้วทำไมไม่เลิกใช้ธนบัตรและเหรียญเลยล่ะครับ​",
                    "แปะสติ๊กเกอร์หนูหิ่น",
                    "เมกามันอยู่เบื้องหลัง แล้วให้ไอ้ธรบงการอีกที",
                    "นักเลง อันธพาล คนเกเร คนติดยา ผีพนัน คนสีเทา เค้ายังรู้จักรัก ปกป้องสถาบัน",
                    "ผมน่ะทำงานเพื่อบ้านเมือง",
                    "จะไล่ประยุทธ์ก็ไล่ไปสิ ทำไมต้องเอาพระองค์ท่านมาเกี่ยวด้วย",
                    "ถ้าเข้ามาในฐานะคนรักดนตรีแล้วทิ้งเรื่องการเมืองไว้นอกรั้ว ก็คงไม่มีใครไปปิดกั้น",
                    "ทำมาหากินเลี้ยงตัวเองเลี้ยงครอบครัวให้รอด พอแล้ว ใครจะมาหาว่าเป็น Ignorant ช่างหัวพ่อมัน",
                    "วันแรกขาย iPhone 12 ในประเทศไทย คิวยาวเหยียด อ้าว! นึกว่าเศรษฐกิจไม่ดี!",
                    "คงได้ผัวก่อนเรียนจบ แต่งตัวแบบนี้",
                    "โกงนิดๆ หน่อยๆ ไม่เป็นไรหรอก ไอ้พวกนักการเมืองมันโกงมากกว่านี้เยอะ",
                    "ฉันเออ ฉันอยากร้องไห้ ฉันxxxไว้แก ฉันโอยฉัน อึ้ยฉัน โอ้ย แกแกฉันตื่นเต้นมาก ฉัน โอ้ย ฉันxxxxหนักมากเลย ฉันบอกแล้วว่าฉันร้องไห้ เออฉัน โอย ฉัน โอ้ยแก้หัวใจฉันจะวาย โอ้ยฉัน ใจฉันเต้นตึก ๆ โอยๆ แก ฉันได้จับมือท่านน่ารักมากแก แบบ โอ้ยฉันสุดฤทธิ์ แก ฉันจะเป็นลม ไม่ โอ้ยเออ แก ฉันดีใจ",
                    "ให้ใครมาด่าพ่อแม่คุณไม่ผิดเอาไหม",
                    "แม้เหลือคนเดียวทั้งโรง เราก็จะยืน",
                    "ถ้าเป็นรัฐบาลอื่น มาเจอวิกฤติโควิด สถานการณ์แม่งเละกว่านี้อีก",
                    "ไม่ได้เชียร์ลุง แต่ลุงเค้าทำตามกฏหมาย",
                    "แล้วคนด่ารับผิดชอบอะไร เกิดมาทำอะไรให้กับบ้านนี้เมืองนี้",
                    "เรียกร้องทุกอย่างจากกษัตริย์ขนาดนี้ เอาระบอบสมบูรณาญาสิทธิราชย์เลยไหม ไม่ต้องมีละนักการเมือง ไม่ต้องระบอบประชาธิปไตย",
                    "อีเด็กพวกนี้มันจะไปรู้อะไร",
                    "การซื้อตำแหน่งมันเรื่องปกติ ถ้าคุณขยันหาเงินนั่นคือคุณก็มีสิทธิ์ คนละเรื่องกับคอรัปชั่นเลย",
                    "ห้ามวิจารณ์ 112",
                    "พูดแต่เรื่องซ้ำซาก ไม่มีหลักฐาน",
                    "ไม่เอาสถาบันกษัตริย์ แต่พวกตัวเองก็ไม่เคยทำประโยชน์กับประชาชนเลยสักอย่าง เพราะฉะนั้นอยู่กับสถาบันกษัตริย์นี่แหละมีประโยชน์ที่สุดแล้ว",
                    "ติดอยู่ตรงกลาง ม๊อบก็ไม่ใช้ สลิ่มก็ไม่เชิง งงม่ะ?",
                    "ไม่อยากให้เพจนี้แสดงออกทางการเมืองเลยค่ะ",
                    "วันที่ออกมาไม่เจออากาศแย่ก็มี ถนนหน้าบ้านเราก็ไม่ได้พัง สวยด้วย น้ำก็ไม่ได้กร่อยอ่ะ คนที่จนแถวบ้าน เมื่อเช้าก็เห็นเค้านั่งโขกหมากรุก หัวเราะเอิ๊กอ๊ากอยู่นะ​",
                    "คือเราอยากให้ประเทศพัฒนา และในช่วงปีหลังๆ ตั้งแต่ 58 เป็นต้นมามันมีหลายอย่างที่พัฒนาแบบจับต้องได้มากๆ และรัฐบาลก็ผ่านการเลือกตั้งมาแล้ว เพราะงั้นเราไม่เห็นว่ามีความจำเป็นอะไรต้องล้มรัฐบาลในตอนนี้ที่วิกฤติ Covid ยังดำเนินอยู่ เว้นแต่ว่ามีคอรัปชันอะไรที่รับไม่ได้ถึงจะเห็นสมควรค่ะ",
                    "เป็นเพจการเมืองไปเสียแล้วคงต้องเลิกติดตาม ไปกิน MK ดีกว่า 555",
                    "กลับบ้านไปทำไร่ทำนาอยู่อย่างพอเพียง ขยันหน่อยอยู่ได้ครับ",
                    "ที่ภาคเหนือมีฝุ่นPM2.5เยอะ ก็ไม่ต้องไปโทษใคร เป็นผลกรรมจากไอ้แม้วนี่แหละ รู้เอาไว้นะคะ​",
                    "ถ้าข้างบ้านเขาทะเลาะกัน คุณจะทำยังไง ในเมื่อคุณก็แค่คนที่มีบ้านติดกับเขา",
                    "เรื่องนามงามพม่า เรื่องของประเทศเขาเราอย่าสนใจเลย ประเทศใครประเทศมัน"]
        
        slimrandom = random.choice(quoteslim)
        embed = discord.Embed(
            colour = 0xffe852,
            title = "คําพูดสลิ่ม",
            description = f"```{slimrandom}```"
        )
        
        embed.set_thumbnail(url="https://i.imgur.com/prrLCPC.png")
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🐃")

@client.command()
async def calculator(ctx , *,equation):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
        
            url = f"https://api.mathjs.org/v4/?expr={equation}"
            req = requests.get(url)
            result = BeautifulSoup(req.text, "html.parser")

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "เครื่องคิดเลข",
                description = f"""```
        โจทย์ : {equation}
        คําตอบ : {result}
        ```""")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)
        
        if server_language == "Thai":
        
            url = f"https://api.mathjs.org/v4/?expr={equation}"
            req = requests.get(url)
            result = BeautifulSoup(req.text, "html.parser")

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "Calculato",
                description = f"""```
        Equation : {equation}
        Answer : {result}
        ```""")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)


@calculator.error
async def calculator_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                title = "ข้อผิดพลาดในการคํานวณ",
                description = f" ⚠️``{ctx.author}`` จะต้องใส่สิ่งที่จะคําณวน ``{COMMAND_PREFIX}calculator (equation)``"
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "ระบุสิ่งที่จะคําณวน",
                    description = f" ⚠️``{ctx.author}`` จะต้องระบุใส่สิ่งที่จะคําณวน ``{COMMAND_PREFIX}calculator (equation)``"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify an equation",
                    description = f" ⚠️``{ctx.author}`` need to specify a math equation ``{COMMAND_PREFIX}calculator (equation)``"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def length(ctx, *, text):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        num = len(text)
        if server_language == "Thai": 
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "LENGTH COUNTER",
                description = f"""```
ข้อความ : {text}
ความยาว : {num}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)
        
        if server_language == "English": 
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "LENGTH COUNTER",
                description = f"""```
text : {text}
length : {num}```"""

            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed)

@length.error
async def length_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะนับตัวอักษร ``{COMMAND_PREFIX}length (text)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะนับตัวอักษร ``{COMMAND_PREFIX}length (text)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a text ``{COMMAND_PREFIX}length (text)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def github(ctx, *, user=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            url = f"https://api.github.com/users/{user}"
            if user is None:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อของGithubที่จะดู ``{COMMAND_PREFIX}github (user)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            try:
                r = requests.get(url)
                r = r.json()

                username = r['login']
                avatar =  r['avatar_url']
                githuburl = r['html_url']
                name = r['name']
                location = r['location']
                email = r['email']
                company = r['company']
                bio = r['bio']
                repo = r['public_repos']

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️ไม่สามารถค้นหาชื่อของGithubได้โปรดเช็คตัวสะกด")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"💻 ข้อมูล Github ของ {username}",
                description = f"""```
ชื่อ Github : {username}
ลิงค์ Github : {githuburl}
ชื่อ : {name}
ที่อยู่ : {location}
อีเมล : {email}
บริษัท : {company}
Bio : {bio}
จํานวนงานที่ลง : {repo}
        ```"""
            )
            embed.set_thumbnail(url = avatar)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            
            await message.add_reaction("💻")

        if server_language == "English":
            url = f"https://api.github.com/users/{user}"
            if user is None:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a github username to search ``{COMMAND_PREFIX}github (user)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            try:
                r = requests.get(url)
                r = r.json()

                username = r['login']
                avatar =  r['avatar_url']
                githuburl = r['html_url']
                name = r['name']
                location = r['location']
                email = r['email']
                company = r['company']
                bio = r['bio']
                repo = r['public_repos']

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️Unable to find the github profile please check your spelling")
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"💻 ข้อมูล Github ของ {username}",
                description = f"""```
Github username: {username}
Github link : {githuburl}
Name : {name}
Location : {location}
Email : {email}
Company : {company}
Bio : {bio}
Repository : {repo}
        ```"""
            )
            embed.set_thumbnail(url = avatar)
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            
            await message.add_reaction("💻")

@client.command()
async def roll(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        num = ["1","2","3","4 ","5","6","1","2","3","4","5","6","1","2","3","4","5","6"]
        x = random.choice(num)
        url = (f"https://www.calculator.net/img/dice{x}.png")

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "🎲 ทอยลูกเต่า"
            )
            embed.set_image(url = url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("🎲")
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "🎲 Dice"
            )
            embed.set_image(url = url)
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction("🎲")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *,question):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        r = requests.get(f"https://8ball.delegator.com/magic/JSON/{question}")
        r = r.json()

        answer = r['magic']['answer']
        ask = r['magic']['question']
        percent = r['magic']['type']

        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "🎱 8ball",
                description = f"""```
คําถาม : {ask}
คําตอบ : {answer}
ความน่าจะเป็น : {percent}```"""
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction("🎱")

        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = "🎱 8ball",
                description = f"""```
Question : {ask}
Respond : {answer}
Probability : {percent}```"""
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed=embed)
            await message.add_reaction("🎱")

@client.command()
async def embed(ctx,*,message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if "//" in message:
            message = message.replace('//', '\n')
            #somehow make it go to the next line
            #if // is in the message it will move to the next line and continue the message which is after the //
        
        embed = discord.Embed(
            colour = 0x00FFFF,
            title= f"{message}"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)

@embed.error
async def embed_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็น embed ``{COMMAND_PREFIX}embed (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็น embed ``{COMMAND_PREFIX}embed (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` Specify text to make into embed ``{COMMAND_PREFIX}embed (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":          
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator)==(member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"ปลดเเบน {member}",
                        description = f"{member} ได้ถูกปลนเเบน"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"ไม่พบชื่อ {member}",
                        description = "ไม่มีชื่อนี้ในรายชื่อคนที่ถูกเเบนโปรดเช็คชื่อเเละเลขข้างหลัง"

                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    await ctx.send(embed=embed)
        
        if server_language == "English":          
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator)==(member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        title = f"unban {member}",
                        description = f"{member} have been unban"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        colour = 0x983925,
                        title = f"No user named {member}",
                        description = "Please check spelling and number behind the name"

                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    await ctx.send(embed=embed)

@unban.error
async def unban_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะปลดเเบน ``{COMMAND_PREFIX}unban (member#1111)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ปลดเเบน",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะปลดเเบน ``{COMMAND_PREFIX}unban (member#1111)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ปลดเเบน",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "Specify member",
                    description = f" ⚠️``{ctx.author}`` need to specify who to unban ``{COMMAND_PREFIX}unban (member#1111)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def webhook(ctx , webhook ,* , message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        WEBHOOK_URL = webhook
        WEBHOOK_USERNAME = "Smilewinbot"
        WEBHOOK_AVATAR = client.user.avatar_url
        WEBHOOK_CONTENT = message

        if server_language == "Thai":
            try:
                payload = {"content":WEBHOOK_CONTENT,"username":WEBHOOK_USERNAME,"avatar_url":WEBHOOK_AVATAR}
                requests.post(WEBHOOK_URL,data=payload)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "ส่งข้อความไปยังwebhook",
                    description = f"""```
ข้อความ :
{message}```"""
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
                
            except Exception as e:
                print(e)

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    title= "ไม่สามารถส่งข้อความไปยังwebhook",
                    description= "Webhook อาจจะผิดโปรดตรวจสอบ"

                )
                
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            try:
                payload = {"content":WEBHOOK_CONTENT,"username":WEBHOOK_USERNAME,"avatar_url":WEBHOOK_AVATAR}
                requests.post(WEBHOOK_URL,data=payload)

                embed = discord.Embed(
                    colour = 0x00FFFF,
                    title = "sending message to webhook",
                    description = f"""```
message :
{message}```"""
                )

                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
                
            except Exception as e:
                print(e)

            except:
                embed = discord.Embed(
                    colour = 0x983925,
                    title= "Unable to send to webhook",
                    description= "Webhook might not be valid"

                )
                
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if get(ctx.guild.roles, name=role.name):
                try:
                    await user.add_roles(role)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        description = f"ได้ทําการเพิ่มยศ {role} ให้กับ {user} "
                    )

                    message = await ctx.send(embed = embed)
                    await message.add_reaction('✅')

                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f"ไม่สามารถให้ยศ{role} กับ {user.name} ได้"
                    )
                    message = await ctx.send(embed = embed)
                    await message.add_reaction('⚠️')
            else:
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f"ไม่มียศ{role}"
                    )
                message = await ctx.send(embed = embed)
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if get(ctx.guild.roles, name=role.name):
                try:
                    await user.add_roles(role)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        description = f"{role} have been given to {user}"
                    )

                    message = await ctx.send(embed = embed)
                    await message.add_reaction('✅')

                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f"unable to give role {role} to {user.name}"
                    )
                    message = await ctx.send(embed = embed)
                    await message.add_reaction('⚠️')
            else:
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f"No role name :{role}"
                    )
                message = await ctx.send(embed = embed)
                await message.add_reaction('⚠️')

@giverole.error
async def giverole_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะให้ยศเเละยศที่จะให้ ``{COMMAND_PREFIX}giverole @user @role``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ให้ยศ",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะให้ยศเเละยศที่จะให้ ``{COMMAND_PREFIX}giverole @user @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ให้ยศ",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify member and specify what role to give``{COMMAND_PREFIX}giverole @user @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``kick`` to be able to use this command"
                )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if get(ctx.guild.roles, name=role.name):
                try:
                    await user.remove_roles(role)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        description = f"ได้ทําการเอายศ {role} ออกให้กับ {user}"
                    )

                    message = await ctx.send(embed = embed)
                    await message.add_reaction('✅')

                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f"ไม่สามารถเอายศ {role} ของ {user.name} ออกได้"
                    )
                    message = await ctx.send(embed = embed)
                    await message.add_reaction('⚠️')
            
            else:
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f"ไม่มียศ{role}"
                    )
                message = await ctx.send(embed = embed)
                await message.add_reaction('⚠️')

        if server_language == "English":
            if get(ctx.guild.roles, name=role.name):
                try:
                    await user.remove_roles(role)
                    embed = discord.Embed(
                        colour = 0x00FFFF,
                        description = f"{role} have been removed from {user}"
                    )

                    message = await ctx.send(embed = embed)
                    await message.add_reaction('✅')

                except:
                    embed = discord.Embed(
                        colour = 0x983925,
                        description = f"unable to remove role {role} from {user.name}"
                    )
                    message = await ctx.send(embed = embed)
                    await message.add_reaction('⚠️')
            
            else:
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f"No role name :{role}"
                    )
                message = await ctx.send(embed = embed)
                await message.add_reaction('⚠️')

@removerole.error
async def removerole_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะให้ยศเเละยศที่เอาออก ``{COMMAND_PREFIX}removerole @role``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์เอายศออก",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะให้ยศเเละยศที่เอาออก ``{COMMAND_PREFIX}removerole @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์เอายศออก",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify member and specify what role to remove ``{COMMAND_PREFIX}giverole @user @role``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``kick`` to be able to use this command"
                )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def changenick(ctx, user: discord.Member, Change):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    description = f"ได้ทําการเปลี่ยนชื่อ {user.name} เป็น {Change}"
                )

            message = await ctx.send(embed = embed)
            await message.add_reaction('✅')
            await user.edit(nick=Change)
        
        if server_language == "English":
            embed = discord.Embed(
                    colour = 0x00FFFF,
                    description = f"{user.name} Name have been change to {Change}"
                )

            message = await ctx.send(embed = embed)
            await message.add_reaction('✅')
            await user.edit(nick=Change)


@changenick.error
async def changenick_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องที่จะเปลี่ยนชื่อเเละชื่อใหม่ ``{COMMAND_PREFIX}changenick @member newnick``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์เปลี่ยนชื่อ",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องที่จะเปลี่ยนชื่อเเละชื่อใหม่ ``{COMMAND_PREFIX}changenick @member newnick``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์เปลี่ยนชื่อ",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed) 
                await message.add_reaction('⚠️')

        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify member and new nickname ``{COMMAND_PREFIX}changenick @member newnick``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
            
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``kick`` to be able to use this command"
                )
            
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def anon(ctx, *,message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            username = "Smilewin"
            avatar = client.user.avatar_url

            author = ctx.author.name
            author = author[::-1]
            letter = len(author)

            while letter < 5:
                author = author + ("X")
                letter = letter+1

            author = author[:5]
            author = author[0] + author[4] + author[1] + author[3] + author[2]

            message = f"[{author}] : {message}"
            payload = {"content":message,"username":username,"avatar_url":avatar}
            
            anonresults = collection.find({"webhook_status":"YES"})
            results = collection.find({"guild_id":ctx.guild.id})
            for data in results:
                if data["webhook_status"] == "YES":
                    for anondata in anonresults:
                        webhook = anondata["webhook_url"]
                        requests.post(webhook,data=payload)
                        time.sleep(0.005)
            
                else:
                    results = collection.find({"guild_id":ctx.guild.id})
                    for data in results:
                        if data["webhook_status"] != "YES" and data["webhook_url"] == "None":
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = "ไม่พบ webhook ของคุณ",
                                description = f"คุณต้องตั้งค่าห้องคุยกับคนเเปลกหน้าก่อน ใช้คําสั่ง {COMMAND_PREFIX}setwebhook #channel"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed = embed)
                            await message.add_reaction('⚠️')

                        elif data["webhook_url"] != "None" and data["webhook_status"] == "NO":
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = "คุณได้ปิดคําสั่งนี้ไว้",
                                description = f"คุณต้องเปิดใช้คําสั่งนี้โดยใช้ {COMMAND_PREFIX}chat on"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed = embed)
                            await message.add_reaction('⚠️')
        
        if server_language == "English":
            username = "Smilewin"
            avatar = client.user.avatar_url

            author = ctx.author.name
            author = author[::-1]
            letter = len(author)

            while letter < 5:
                author = author + ("X")
                letter = letter+1

            author = author[:5]
            author = author[0] + author[4] + author[1] + author[3] + author[2]

            message = f"[{author}] : {message}"
            payload = {"content":message,"username":username,"avatar_url":avatar}
            
            anonresults = collection.find({"webhook_status":"YES"})
            results = collection.find({"guild_id":ctx.guild.id})
            for data in results:
                if data["webhook_status"] == "YES":
                    for anondata in anonresults:
                        webhook = anondata["webhook_url"]
                        requests.post(webhook,data=payload)
                        time.sleep(0.005)
            
                else:
                    results = collection.find({"guild_id":ctx.guild.id})
                    for data in results:
                        if data["webhook_status"] != "YES" and data["webhook_url"] == "None":
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = "Your webhook is not found",
                                description = f"You need to setup a room to talk to stranger {COMMAND_PREFIX}setwebhook #channel"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed = embed)
                            await message.add_reaction('⚠️')

                        elif data["webhook_url"] != "None" and data["webhook_status"] == "NO":
                            embed = discord.Embed(
                                colour = 0x983925,
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}chat on"
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message = await ctx.send(embed = embed)
                            await message.add_reaction('⚠️')

@anon.error
async def anon_error(ctx,error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่จะส่ง ``{COMMAND_PREFIX}anon (message)``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่จะส่ง ``{COMMAND_PREFIX}anon (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify a message to send ``{COMMAND_PREFIX}anon (message)``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        

@client.command()
async def enbinary(ctx, *, text): 
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            r = requests.get(f"https://some-random-api.ml/binary?text={text}")
            r = r.json()

            binary = r['binary']

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "Encode Binary",
                description = f"""```
คําปกติ : {text}
Binary : {binary}```"""
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💻')
        
        if server_language == "English":
            r = requests.get(f"https://some-random-api.ml/binary?text={text}")
            r = r.json()

            binary = r['binary']

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "Encode Binary",
                description = f"""```
Normal text : {text}
Binary : {binary}```"""
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💻')

@client.command()
async def debinary(ctx, *,text): 
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            r = requests.get(f"https://some-random-api.ml/binary?decode={text}")
            r = r.json()

            binary = r['text']

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "Encode Binary",
                description = f"""```
Binary : {text}
Normal text : {binary}```"""
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💻')
        
        if server_language == "Thai":
            r = requests.get(f"https://some-random-api.ml/binary?decode={text}")
            r = r.json()

            binary = r['text']

            embed = discord.Embed(
                colour=0x00FFFF,
                title= "Encode Binary",
                description = f"""```
Binary : {text}
Normal text : {binary}```"""
                )
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message =await ctx.send(embed=embed)
            await message.add_reaction('💻')

@client.command(aliases=['ind'])
async def introduction(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            results = collection.find({"guild_id":ctx.guild.id})
            for data in results:
                status = data["introduce_status"]
                frame = data["introduce_frame"]
                channel = data["introduce_channel_id"] 
                give = data["introduce_role_give_id"]
                remove = data["introduce_role_remove_id"]

            if status == "YES":
                if frame == "None":
                    frame = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

                    if channel == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[1] ชื่อ")
                
                            embed.set_footer(text="คำถามที่ [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[2] อายุ")
                
                            embed.set_footer(text="คำถามที่ [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()  

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[3] เพศ")
                
                            embed.set_footer(text="คำถามที่ [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=embed)
                        
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass
                    
                    else:
        
                        channel = channel
                        channel = client.get_channel(id=int(channel))
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[1] ชื่อ")
                
                            embed.set_footer(text="คำถามที่ [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[2] อายุ")
                
                            embed.set_footer(text="คำถามที่ [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[3] เพศ")
                
                            embed.set_footer(text="คำถามที่ [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await channel.send(ctx.author.mention)
                        await channel.send(embed=embed)

                    
                
                else:
                    frame = frame

                    if channel == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[1] ชื่อ")
                
                            embed.set_footer(text="คำถามที่ [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[2] อายุ")
                
                            embed.set_footer(text="คำถามที่ [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()  

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[3] เพศ")
                
                            embed.set_footer(text="คำถามที่ [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=embed)
                        
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass
                    
                    else:
        
                        channel = channel
                        channel = client.get_channel(id=int(channel))
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[1] ชื่อ")
                
                            embed.set_footer(text="คำถามที่ [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[2] อายุ")
                
                            embed.set_footer(text="คำถามที่ [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "กรุณาใส่ข้อมูลให้ครบถ้วน 📝",
                                description = "┗[3] เพศ")
                
                            embed.set_footer(text="คำถามที่ [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await channel.send(ctx.author.mention)
                        await channel.send(embed=embed)
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass              

            else:
                embed =discord.Embed(
                    colour = 0x983925,
                    description = f"คําสั่งนี้ได้ถูกปิดใช้งาน ใช้คําสั่ง {COMMAND_PREFIX}introduce on เพื่อเปิดใช้งาน"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
                await asyncio.sleep(3) 
                await message.delete()  

        if server_language == "English":
            results = collection.find({"guild_id":ctx.guild.id})
            for data in results:
                status = data["introduce_status"]
                frame = data["introduce_frame"]
                channel = data["introduce_channel_id"] 
                give = data["introduce_role_give_id"]
                remove = data["introduce_role_remove_id"]

            if status == "YES":
                if frame == "None":
                    frame = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

                    if channel == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[1] Name")
                
                            embed.set_footer(text="Question [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[2] Age")
                
                            embed.set_footer(text="Question [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()  

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[3] Gender")
                
                            embed.set_footer(text="Question [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=embed)
                        
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass
                    
                    else:
        
                        channel = channel
                        channel = client.get_channel(id=int(channel))
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[1] Name")
                
                            embed.set_footer(text="Question [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[2] Age")
                
                            embed.set_footer(text="Question [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[3] Gender")
                
                            embed.set_footer(text="Question [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await channel.send(ctx.author.mention)
                        await channel.send(embed=embed)
      
                else:
                    frame = frame

                    if channel == "None":
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[1] Name")
                
                            embed.set_footer(text="Question [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[2] Age")
                
                            embed.set_footer(text="Question [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()  

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[3] Gender")
                
                            embed.set_footer(text="Question [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await ctx.send(ctx.author.mention)
                        await ctx.send(embed=embed)
                        
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass
                    
                    else:
        
                        channel = channel
                        channel = client.get_channel(id=int(channel))
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[1] Name")
                
                            embed.set_footer(text="Question [1/3]")
                            message = await ctx.send(embed=embed)

                            username = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            name = username.content
                            await asyncio.sleep(1) 
                            await username.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝 📝",
                                description = "┗[2] Age")
                
                            embed.set_footer(text="Question [2/3]")
                            await message.edit(embed=embed)

                            userage = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            age = userage.content
                            await asyncio.sleep(1) 
                            await userage.delete()

                        except asyncio.TimeoutError:
                            await message.delete()
                
                        try:
                            embed = discord.Embed(
                                colour = 0x00FFFF,
                                title = "Please fill in all information. 📝",
                                description = "┗[3] Gender")
                
                            embed.set_footer(text="Question [3/3]")
                            await message.edit(embed=embed)

                            usersex = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            sex = usersex.content
                            await asyncio.sleep(1) 
                            await usersex.delete()

                        except asyncio.TimeoutError:
                            await message.delete()

                        embed = discord.Embed(
                            colour = 0x00FFFF,
                            description = (f"""```
    {frame}
    ชื่อ : {name}
    อายุ : {age}
    เพศ : {sex}
    {frame}```""")
                )
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text = ctx.author.id)
                        await message.delete()
                        await channel.send(ctx.author.mention)
                        await channel.send(embed=embed)
                        if not give == "None":
                            try:
                                role = give
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.add_roles(role)

                            except Exception:
                                pass
                
                        if not remove == "None":
                            try:
                                role = remove
                                role = int(role)
                                role = ctx.guild.get_role(role)
                                await ctx.author.remove_roles(role)

                            except Exception:
                                pass              

            else:
                embed =discord.Embed(
                    colour = 0x983925,
                    description = f"This command is disable please use {COMMAND_PREFIX}introduce on"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
                await asyncio.sleep(3) 
                await message.delete()

@client.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
     
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                embed = discord.Embed(
                    title = "ตั้งค่าสําเร็จ",
                    colour= 0x00FFFF,
                    description = f"ลงทะเบือนเซิฟเวอร์ในฐานข้อมูลสําเร็จ"
                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

            else:
                id = server["_id"]
                embed = discord.Embed(
                    title = "มีข้อมูลของเซิฟเวอร์ในฐานข้อมูลเเล้ว",
                    colour= 0x00FFFF,
                    description = f"ไอดีของเซิฟเวอร์ในฐานข้อมูลคือ {id}"
                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
        
        if server_language == "English":
     
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                embed = discord.Embed(
                    title = "Setup complete",
                    colour= 0x00FFFF,
                    description = f"Your server is now registered on the database"
                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

            else:
                id = server["_id"]
                embed = discord.Embed(
                    title = "Server data already exist",
                    colour= 0x00FFFF,
                    description = f"ID of your server in database {id}"
                )
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

@client.command()
@commands.has_permissions(administrator=True)
async def roleall(ctx, role: discord.Role):
    i = 0
    embed = discord.Embed(
        title = "ให้ยศสมาชิกทุกคน",
        colour = 0x00FFFF,
        description = f"กําลังดําเนินการให้ยศ {role} กับสมาชิกทั้งหมด {ctx.guild.member_count}คน"
    )
    message = await ctx.send(embed=embed)

    for user in ctx.guild.members:

        try:
            await user.add_roles(role)
            time.sleep(0.5)
            i +=1

        except:
            pass
    embed = discord.Embed(
        title = "ให้ยศสมาชิกทุกคน",
        colour = 0x00FFFF,
        description = f"ให้ยศ {role} สมาชิกทั้งหมด {i}คนสําเร็จ"
    )
    await message.edit(embed=embed)

@roleall.error
async def roleall_error(ctx ,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ยศที่จะให้ ``{COMMAND_PREFIX}roleall @role``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์เเอดมิน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

@client.command()
@commands.has_permissions(administrator=True)
async def removeroleall(ctx, role: discord.Role):
    i = 0
    embed = discord.Embed(
        title = "ลบยศสมาชิกทุกคน",
        colour = 0x00FFFF,
        description = f"กําลังดําเนินการลบยศ {role} กับสมาชิกทั้งหมด {ctx.guild.member_count}คน"
    )
    message = await ctx.send(embed=embed)

    for user in ctx.guild.members:

        try:
            await user.remove_roles(role)
            time.sleep(0.5)
            i +=1

        except:
            pass
    embed = discord.Embed(
        title = "ลบยศสมาชิกทุกคน",
        colour = 0x00FFFF,
        description = f"ลบยศ {role} สมาชิกทั้งหมด {i}คนสําเร็จ"
    )
    await message.edit(embed=embed)

@roleall.error
async def reomveroleall_error(ctx ,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ยศที่จะให้ ``{COMMAND_PREFIX}removeroleall @role``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์เเอดมิน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

@client.command()
async def support(ctx, * , message):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            channel = client.get_channel(id = int(supportchannel))
            embed = discord.Embed(
                title = f"ปัญหาบอทโดย {ctx.author}",
                description = message,
                colour = 0x00FFFF,
            )
            await channel.send(embed=embed)

            embed = discord.Embed(
                title = f"ขอบคุณครับ",
                description = "ปัญหาได้ถูกเเจ้งเรียบร้อย",
                colour = 0x00FFFF,
            )
            await ctx.send(embed=embed)
        
        if server_language == "Thai":
            channel = client.get_channel(id = int(supportchannel))
            embed = discord.Embed(
                title = f"ปัญหาบอทโดย {ctx.author}",
                description = message,
                colour = 0x00FFFF,
            )
            await channel.send(embed=embed)

            embed = discord.Embed(
                title = f"Thank you",
                description = "Bot developer will fix this soon",
                colour = 0x00FFFF,
            )
            await ctx.send(embed=embed)

@client.listen()
async def on_message(message):
    if message.guild:
        if not message.content.startswith('/r '):
            server = collection.find({"guild_id":message.guild.id})
            guild = collection.find_one({"guild_id":message.guild.id})
            if not guild is None:
                if not message.author.bot:
                    for data in server:
                        status = data["level_system"]
                    if status == "YES":
                        user = collectionlevel.find_one({"user_id":message.author.id})
                        if user is None:
                            newuser = {"guild_id": message.guild.id, "user_id":message.author.id,"xp":0 , "level":0}
                            collectionlevel.insert_one(newuser)
                        else:
                            userlevel = collectionlevel.find({"guild_id":message.guild.id , "user_id":message.author.id})
                            for data in userlevel:

                                userxp = data["xp"] + 5
                                collectionlevel.update_one({"guild_id":message.guild.id , "user_id":message.author.id},{"$set":{"xp":userxp}})
                                currentxp = data["xp"]
                                currentlvl = data["level"]
                                if currentxp > 200:
                                    currentlvl += 1
                                    currentxp = 0
                                    collectionlevel.update_one({"guild_id":message.guild.id , "user_id":message.author.id},{"$set":{"xp":currentxp, "level":currentlvl}})
                                    await message.channel.send(f"{message.author.mention} ได้เลเวลอัพเป็น เลเวล {currentlvl}")
                                else:
                                    pass
                    else:
                        pass
            else:
                pass
        
        else:
            pass
    else:
        pass
            
@client.command()
async def rank(ctx , member : discord.Member=None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if member is None:

                server = collection.find({"guild_id":ctx.guild.id})
                for data in server:
                    status = data["level_system"]
                if status != "NO":
                    user = collectionlevel.find_one({"user_id":ctx.author.id})
                    if user is None:
                        await ctx.send(f"เลเวลของ {ctx.author.id} คือ 0")
                
                    else:
                        userlevel = collectionlevel.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                        for data in userlevel:
                            currentxp = data["xp"]
                            currentlvl = data["level"]
                            stringcurrentlvl = str(currentxp)
                            liststringcurrentlvl = (list(stringcurrentlvl))
                        if currentxp >= 10:
                            if int(liststringcurrentlvl[1]) == 5:
                                boxxp = int(currentxp - 5)
                                bluebox = int(boxxp/10)
                                whitebox = int(20 - bluebox)
                            else:
                                bluebox = int(currentxp/10)
                                whitebox = int(20 - bluebox)
                        
                        else:
                            bluebox = 0
                            whitebox = 20

                        ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)
                        rank = 0
                        for level in ranking:
                            rank += 1
                            if data["user_id"] == level["user_id"]:
                                break

                        embed = discord.Embed(
                            title = f"เลเวลของ {ctx.author.name}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{ctx.author.name}",inline=True)
                        embed.add_field(name = "xp",value= f"{currentxp}",inline=True)
                        embed.add_field(name = "เลเวล",value= f"{currentlvl}",inline=True)
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "ความคืบหน้า",value= bluebox*":blue_square:"+whitebox*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}level on เพื่อเปิดใช้",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
            
            else:
                
                server = collection.find({"guild_id":ctx.guild.id})
                for data in server:
                    status = data["level_system"]
                if status != "NO":
                    user = collectionlevel.find_one({"user_id":member.id})
                    if user is None:
                        await ctx.send(f"เลเวลของ {member.name} คือ 0")
                
                    else:
                        userlevel = collectionlevel.find({"guild_id":ctx.guild.id , "user_id":member.id})
                        for data in userlevel:
                            currentxp = data["xp"]
                            currentlvl = data["level"]
                            stringcurrentlvl = str(currentxp)
                            liststringcurrentlvl = (list(stringcurrentlvl))
                        
                        if currentxp >= 10:
                            if int(liststringcurrentlvl[1]) == 5:
                                boxxp = int(currentxp - 5)
                                bluebox = int(boxxp/10)
                                whitebox = int(20 - bluebox)
                            else:
                                bluebox = int(currentxp/10)
                                whitebox = int(20 - bluebox)
                        
                        else:
                            bluebox = 0
                            whitebox = 20

                        ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("xp",-1)
                        rank = 0
                        for level in ranking:
                            rank += 1
                            if data["user_id"] == level["user_id"]:
                                break
                    
                        embed = discord.Embed(
                            title = f"เลเวลของ {member.name}"
                            )
                        embed.add_field(name = "ชื่อ",value= f"{member.name}",inline=True)
                        embed.add_field(name = "xp",value= f"{currentxp}",inline=True)
                        embed.add_field(name = "เลเวล",value= f"{currentlvl}",inline=True)
                        embed.add_field(name = "เเรงค์",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "ความคืบหน้า",value= bluebox*":blue_square:"+whitebox*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}level on เพื่อเปิดใช้",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('❌')

        if server_language == "English":
            if member is None:

                server = collection.find({"guild_id":ctx.guild.id})
                for data in server:
                    status = data["level_system"]
                if status != "NO":
                    user = collectionlevel.find_one({"user_id":ctx.author.id})
                    if user is None:
                        await ctx.send(f"{ctx.author.id} level is 0")
                
                    else:
                        userlevel = collectionlevel.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                        for data in userlevel:
                            currentxp = data["xp"]
                            currentlvl = data["level"]
                            stringcurrentlvl = str(currentxp)
                            liststringcurrentlvl = (list(stringcurrentlvl))
                        if currentxp >= 10:
                            if int(liststringcurrentlvl[1]) == 5:
                                boxxp = int(currentxp - 5)
                                bluebox = int(boxxp/10)
                                whitebox = int(20 - bluebox)
                            else:
                                bluebox = int(currentxp/10)
                                whitebox = int(20 - bluebox)
                        
                        else:
                            bluebox = 0
                            whitebox = 20

                        ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)
                        rank = 0
                        for level in ranking:
                            rank += 1
                            if data["user_id"] == level["user_id"]:
                                break

                        embed = discord.Embed(
                            title = f"{ctx.author.name} Level"
                            )
                        embed.add_field(name = "Name",value= f"{ctx.author.name}",inline=True)
                        embed.add_field(name = "XP",value= f"{currentxp}/200",inline=True)
                        embed.add_field(name = "Level",value= f"{currentlvl}",inline=True)
                        embed.add_field(name = "Rank",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "Progress",value= bluebox*":blue_square:"+whitebox*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}level on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
            
            else:
                
                server = collection.find({"guild_id":ctx.guild.id})
                for data in server:
                    status = data["level_system"]
                if status != "NO":
                    user = collectionlevel.find_one({"user_id":member.id})
                    if user is None:
                        await ctx.send(f"{member.name} level is 0")
                
                    else:
                        userlevel = collectionlevel.find({"guild_id":ctx.guild.id , "user_id":member.id})
                        for data in userlevel:
                            currentxp = data["xp"]
                            currentlvl = data["level"]
                            stringcurrentlvl = str(currentxp)
                            liststringcurrentlvl = (list(stringcurrentlvl))
                        
                        if currentxp >= 10:
                            if int(liststringcurrentlvl[1]) == 5:
                                boxxp = int(currentxp - 5)
                                bluebox = int(boxxp/10)
                                whitebox = int(20 - bluebox)
                            else:
                                bluebox = int(currentxp/10)
                                whitebox = int(20 - bluebox)
                        
                        else:
                            bluebox = 0
                            whitebox = 20

                        ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("xp",-1)
                        rank = 0
                        for level in ranking:
                            rank += 1
                            if data["user_id"] == level["user_id"]:
                                break
                    
                        embed = discord.Embed(
                            title = f"{member.name} Level"
                            )
                        embed.add_field(name = "Name",value= f"{member.name}",inline=True)
                        embed.add_field(name = "XP",value= f"{currentxp}",inline=True)
                        embed.add_field(name = "Level",value= f"{currentlvl}",inline=True)
                        embed.add_field(name = "Rank",value= f"{rank}/{ctx.guild.member_count}",inline=True)
                        embed.add_field(name = "Progress",value= bluebox*":blue_square:"+whitebox*":white_large_square:",inline=False)
                        embed.set_thumbnail(url=f"{member.avatar_url}")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message = await ctx.send(embed=embed)
                        await message.add_reaction("✅")

                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}level on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

@client.command()
async def leaderboard(ctx):
    server = collection.find({"guild_id":ctx.guild.id})
    first = []
    second = []
    third = [] 
    fourth = []
    fifth = []
    sixth = []
    seventh = [] 
    eighth = []
    ninth = []
    tenth = []
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            for data in server:
                status = data["level_system"]
                if status != "NO":
                    ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)
                
                    i = 1
                    for data in ranking:
                        try:
                            member =ctx.guild.get_member(data["user_id"])
                            memberlvl = data["level"]
                            member = member.name
                            if i == 1:
                                first.append(i)
                                first.append(member)
                                first.append(memberlvl)
                            
                            if i == 2:
                                second.append(i)
                                second.append(member)
                                second.append(memberlvl)
                            
                            if i == 3:
                                third.append(i)
                                third.append(member)
                                third.append(memberlvl)
                            
                            if i == 4:
                                fourth.append(i)
                                fourth.append(member)
                                fourth.append(memberlvl)
                            
                            if i == 5:
                                fifth.append(i)
                                fifth.append(member)
                                fifth.append(memberlvl)
                            
                            if i == 6:
                                sixth.append(i)
                                sixth.append(member)
                                sixth.append(memberlvl)
                            
                            if i == 7:
                                seventh.append(i)
                                seventh.append(member)
                                seventh.append(memberlvl)

                            if i == 8:
                                eighth.append(i)
                                eighth.append(member)
                                eighth.append(memberlvl)
                            
                            if i == 9:
                                ninth.append(i)
                                ninth.append(member)
                                ninth.append(memberlvl)
                            
                            if i == 10:
                                tenth.append(i)
                                tenth.append(member)
                                tenth.append(memberlvl)
                            
                            i = i + 1 

                        except:
                            pass
                    if i == 11:
                        break
                    
                    description = f"""```py
-----------------------------
อันดับ {first[0]} : {first[1]}
เลเวล :{first[2]}
-----------------------------
อันดับ {second[0]} : {second[1]}
เลเวล :{second[2]}
-----------------------------
อันดับ {third[0]} : {third[1]}
เลเวล :{third[2]}
-----------------------------
อันดับ {fourth[0]} : {fourth[1]}
เลเวล :{fourth[2]}
-----------------------------
อันดับ {fifth[0]} : {fifth[1]}
เลเวล :{fifth[2]}
-----------------------------
อันดับ {sixth[0]} : {sixth[1]}
เลเวล :{sixth[2]}
-----------------------------
อันดับ {seventh[0]} : {seventh[1]}
เลเวล :{seventh[2]}
-----------------------------
อันดับ {eighth[0]} : {eighth[1]}
เลเวล :{eighth[2]}
-----------------------------
อันดับ {ninth[0]} : {ninth[1]}
เลเวล :{ninth[2]}
-----------------------------
อันดับ {tenth[0]} : {tenth[1]}
เลเวล :{tenth[2]}```"""
                    
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
                            description = f"ใช้คําสั่ง {COMMAND_PREFIX}level on เพื่อเปิดใช้",
                            colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('❌')

        if server_language == "English":
            for data in server:
                status = data["level_system"]
                if status != "NO":
                    ranking = collectionlevel.find({"guild_id":ctx.guild.id}).sort("level",-1)
                
                    i = 1
                    for data in ranking:
                        try:
                            member =ctx.guild.get_member(data["user_id"])
                            memberlvl = data["level"]
                            member = member.name
                            if i == 1:
                                first.append(i)
                                first.append(member)
                                first.append(memberlvl)
                            
                            if i == 2:
                                second.append(i)
                                second.append(member)
                                second.append(memberlvl)
                            
                            if i == 3:
                                third.append(i)
                                third.append(member)
                                third.append(memberlvl)
                            
                            if i == 4:
                                fourth.append(i)
                                fourth.append(member)
                                fourth.append(memberlvl)
                            
                            if i == 5:
                                fifth.append(i)
                                fifth.append(member)
                                fifth.append(memberlvl)
                            
                            if i == 6:
                                sixth.append(i)
                                sixth.append(member)
                                sixth.append(memberlvl)
                            
                            if i == 7:
                                seventh.append(i)
                                seventh.append(member)
                                seventh.append(memberlvl)

                            if i == 8:
                                eighth.append(i)
                                eighth.append(member)
                                eighth.append(memberlvl)
                            
                            if i == 9:
                                ninth.append(i)
                                ninth.append(member)
                                ninth.append(memberlvl)
                            
                            if i == 10:
                                tenth.append(i)
                                tenth.append(member)
                                tenth.append(memberlvl)
                            
                            i = i + 1 

                        except:
                            pass
                    if i == 11:
                        break
                    
                    description = f"""```py
-----------------------------
Rank {first[0]} : {first[1]}
Level :{first[2]}
-----------------------------
Rank {second[0]} : {second[1]}
Level :{second[2]}
-----------------------------
Rank {third[0]} : {third[1]}
Level :{third[2]}
-----------------------------
Rank {fourth[0]} : {fourth[1]}
Level :{fourth[2]}
-----------------------------
Rank {fifth[0]} : {fifth[1]}
Level :{fifth[2]}
-----------------------------
Rank {sixth[0]} : {sixth[1]}
Level :{sixth[2]}
-----------------------------
Rank {seventh[0]} : {seventh[1]}
Level :{seventh[2]}
-----------------------------
Rank {eighth[0]} : {eighth[1]}
Level :{eighth[2]}
-----------------------------
Rank {ninth[0]} : {ninth[1]}
Level :{ninth[2]}
-----------------------------
Rank {tenth[0]} : {tenth[1]}
Level :{tenth[2]}```"""
                    
                    embed = discord.Embed(
                        title="Level leaderboard",
                        colour=0x00FFFF,
                        description = description
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                
                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}level on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

@client.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def level(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "ต้องระบุ ON / OFF"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "you need to specify on / off"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

@level.error
async def level_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@level.command(aliases=['on'])
@commands.has_permissions(administrator=True)
async def __on(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            status = "YES"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

        if server_language == "English":
            status = "YES"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

@__on.error
async def levelon_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@level.command(aliases=['off'])
@commands.has_permissions(administrator=True)
async def __off(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            status = "NO"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าเลเวล",
                            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

        if server_language == "English":
            status = "NO"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["level_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Level system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

@__off.error
async def leveloff_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def youtube(ctx, *, keywords):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        apikey = youtubeapi
        youtube = build('youtube', 'v3', developerKey=apikey)
        snippet = youtube.search().list(part='snippet', q=keywords,type='video',maxResults=50).execute()
        
        req = (snippet["items"][0])

        video_title = req["snippet"]["title"]
        video_id = req["id"]["videoId"]
        thumbnail = req["snippet"]["thumbnails"]["high"]["url"]
        channel_title = req["snippet"]["channelTitle"]
        description = req["snippet"]["description"]

        clip_url = "http://www.youtube.com/watch?v="+ video_id

        r = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={apikey}")
        r = r.json()
        stat = r["items"][0]
        view = stat["statistics"]["viewCount"]
        like = stat["statistics"]["likeCount"]
        dislike = stat["statistics"]["dislikeCount"]
        comment = stat["statistics"]["dislikeCount"]
        languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})

        if server_language == "Thai":
            embed = discord.Embed(
                title = video_title,
                colour = 0x00FFFF , 
                description = f"[ดูคลิปนี้]({clip_url})"
            )
            embed.add_field(name ="ชื่อช่อง" , value = f"{channel_title}", inline = True)
            embed.add_field(name ="วิวทั้งหมด" , value = f"{view}", inline = True)
            embed.add_field(name ="คอมเม้นทั้งหมด" , value = f"{comment}", inline = True)
            embed.add_field(name ="ไลค์" , value = f"{like}", inline = True)
            embed.add_field(name ="ดิสไลค์" , value = f"{dislike}", inline = True)
            embed.add_field(name ="คำอธิบาย" , value = f"{description}", inline = True)
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=thumbnail)
            message= await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        if server_language == "English":
            embed = discord.Embed(
                title = video_title,
                colour = 0x00FFFF , 
                description = f"[click here]({clip_url})"
            )
            embed.add_field(name ="Channel" , value = f"{channel_title}", inline = True)
            embed.add_field(name ="View" , value = f"{view}", inline = True)
            embed.add_field(name ="Comment" , value = f"{comment}", inline = True)
            embed.add_field(name ="Like" , value = f"{like}", inline = True)
            embed.add_field(name ="Dislike" , value = f"{dislike}", inline = True)
            embed.add_field(name ="Description" , value = f"{description}", inline = True)
            
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.set_image(url=thumbnail)
            message= await ctx.send(embed=embed)
            await message.add_reaction('✅')
                              
@youtube.error
async def youtube_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{COMMAND_PREFIX}youtube [ชื่อคลิป]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{COMMAND_PREFIX}youtube [ชื่อคลิป]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                        colour = 0x983925,
                        description = f" ⚠️``{ctx.author}`` need to specify what video to search on Youtube ``{COMMAND_PREFIX}youtube [video name]``"
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command()
async def ytsearch(ctx, *, keywords):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        apikey = youtubeapi
        youtube = build('youtube', 'v3', developerKey=apikey)
        snippet = youtube.search().list(part='snippet', q=keywords,type='video',maxResults=50).execute()
        i = 1
        if server_language == "Thai":
            embed = discord.Embed(
                    title = "ค้นหาวิดีโอจาก YouTube",
                    colour = 0x00FFFF , 
                    description = f"ค้นหา: {keywords}"
                )
            while i != 6:
                req = (snippet["items"][i])
                video_title = req["snippet"]["title"]
                video_id = req["id"]["videoId"]
                clip_url = "http://www.youtube.com/watch?v="+ video_id
                embed.add_field(name=f"{i}. {video_title}",value=f"{clip_url}", inline=False)
                i = i+1

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message= await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        if server_language == "English":
            embed = discord.Embed(
                    title = "Video from YouTube",
                    colour = 0x00FFFF , 
                    description = f"search: {keywords}"
                )
            while i != 6:
                req = (snippet["items"][i])
                video_title = req["snippet"]["title"]
                video_id = req["id"]["videoId"]
                clip_url = "http://www.youtube.com/watch?v="+ video_id
                embed.add_field(name=f"{i}. {video_title}",value=f"{clip_url}", inline=False)
                i = i+1

            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message= await ctx.send(embed=embed)
            await message.add_reaction('✅')
                              
@ytsearch.error
async def ytsearch_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour = 0x983925,
                description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{COMMAND_PREFIX}ytsearch [keywords]``"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหา ``{COMMAND_PREFIX}ytsearch [keywords]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    colour = 0x983925,
                    description = f" ⚠️``{ctx.author}`` need to specify what video to search ``{COMMAND_PREFIX}ytsearch [keywords]``"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def economy(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "ต้องระบุ ON / OFF"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
        if server_language == "English":
            embed = discord.Embed(
                colour = 0x00FFFF,
                description = "you need to specify on / off"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

@economy.command(aliases=['on'])
@commands.has_permissions(administrator=True)
async def ____on(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            status = "YES"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการเปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
    
        if server_language == "English":
            status = "YES"
            
            server = collection.find_one({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "YES"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "NO":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"level_systems":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been activated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

@____on.error
async def economyon_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
    
@economy.command(aliases=['off'])
@commands.has_permissions(administrator=True)
async def ____off(ctx):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]

        if server_language == "Thai":
            status = "NO"
            
            server = collection.find({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "YES":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งค่าห้องเเนะนําตัว",
                            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "YES":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "ตั้งระบบเศรษฐกิจ",
                            description= f"ได้ทําการปิดใช้งานระบบนี้"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
        
        if server_language == "English":
            status = "NO"
            
            server = collection.find({"guild_id":ctx.guild.id})
            if server is None:
                newserver = {"guild_id":ctx.guild.id,
                "welcome_id":"None",
                "leave_id":"None",
                "webhook_url":"None",
                "webhook_channel_id":"None",
                "webhook_status":"None",
                "introduce_channel_id":"None",
                "introduce_frame":"None",
                "introduce_role_give_id":"None",
                "introduce_role_remove_id":"None",
                "introduce_status":"YES",
                "level_system":"NO",
                "economy_system":"NO",
                "currency":"$",
                "verification_system":"NO",
                "verification_channel_id":"None",
                "verification_role_give_id":"None",
                "verification_role_remove_id":"None"
                }
                collection.insert_one(newserver)
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "YES":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
                
                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')
            else:
                status = "NO"
                results = collection.find({"guild_id":ctx.guild.id})
                for data in results:
                    if data["economy_system"] == "YES":
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

                    else:
                        collection.update_one({"guild_id":ctx.guild.id},{"$set":{"economy_system":status}})
                        embed = discord.Embed(
                            colour= 0x00FFFF,
                            title = "Economy system",
                            description= f"The level system have been deactivated"
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")

                        message = await ctx.send(embed=embed)
                        await message.add_reaction('✅')

@____off.error
async def economyoff_error(ctx, error):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour = 0x983925,
                title = "คุณไม่มีสิทธิ์ตั้งค่า",
                description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
            )

            embed.set_footer(text=f"┗Requested by {ctx.author}")

            message = await ctx.send(embed=embed ) 
            await message.add_reaction('⚠️')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "คุณไม่มีสิทธิ์ตั้งค่า",
                    description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')
        
        if server_language == "English":
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    colour = 0x983925,
                    title = "You don't have permission",
                    description = f"⚠️ ``{ctx.author}`` You must have ``Administrator`` to be able to use this command"
                )

                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed ) 
                await message.add_reaction('⚠️')

@client.command(aliases=['openbal'])
async def openbalance(ctx):
    server = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if server is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')
    
    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            guild = collection.find_one({"guild_id":ctx.guild.id})
            if not guild is None:
                status = collection.find({"guild_id":ctx.guild.id})
                for data in status:
                    if data["economy_system"] == "YES":
                        user = collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            newbalance = {"guild_id": ctx.guild.id, "user_id":ctx.author.id,"bank":0 , "wallet":0}
                            collectionmoney.insert_one(newbalance)
                            embed = discord.Embed(
                                title = f"ทําบัญชีสําเร็จ",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อดูเงินในบัญชี",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                        else:
                            embed = discord.Embed(
                                title = "มีบัญชีของคุณอยู่เเล้ว",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อดูเงินในบัญชี",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                    else:
                        embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

            else:
                embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')
        
        if server_language == "English":
            guild = collection.find_one({"guild_id":ctx.guild.id})
            if not guild is None:
                status = collection.find({"guild_id":ctx.guild.id})
                for data in status:
                    if data["economy_system"] == "YES":
                        user = collectionmoney.find_one({"user_id":ctx.author.id})
                        if user is None:
                            newbalance = {"guild_id": ctx.guild.id, "user_id":ctx.author.id,"bank":0 , "wallet":0}
                            collectionmoney.insert_one(newbalance)
                            embed = discord.Embed(
                                title = f"Open balance",
                                description = f"Use {COMMAND_PREFIX}bal to see your balance",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                        else:
                            embed = discord.Embed(
                                title = "You already have a balance",
                                description = f"Use {COMMAND_PREFIX}bal to see your balance",
                                colour = 0xB9E7A5
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                    else:
                        embed = discord.Embed(
                            title = "Command is disable",
                            description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')

            else:
                embed = discord.Embed(
                    title = "Command is disable",
                    description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')

@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if not member is None:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":member.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                for data in usermoney:
                                    bank = data["bank"]
                            
                                embed = discord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"จำนวนเงินของ {member.name}", icon_url=f"{member.avatar_url}") 
                            
                                embed.add_field(name=f'เงินในธนาคาร', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'เงินทั้งหมด', value=f' ?? {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    bank = data["bank"]
                                    wallet = data["wallet"]
                                    total = bank + wallet
                            
                                embed = discord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"จำนวนเงินของ {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}") 
                            
                                embed.add_field(name=f'เงินในธนาคาร', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'เงินในกระเป๋าตัง', value=f'{wallet} {currency}', inline = False)
                                embed.add_field(name=f'เงินทั้งหมด', value=f'{total} {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

        if server_language == "English":
            if not member is None:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":member.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                for data in usermoney:
                                    bank = data["bank"]
                            
                                embed = discord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"{member.name} balance", icon_url=f"{member.avatar_url}") 
                            
                                embed.add_field(name=f'Bank', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'Total money', value=f' ?? {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = discord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                        colour = 0x983925
                            )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    bank = data["bank"]
                                    wallet = data["wallet"]
                                    total = bank + wallet
                            
                                embed = discord.Embed(
                                    colour = 0xB9E7A5
                                )
                                embed.set_author(name=f"{ctx.author.name} balance", icon_url=f"{ctx.author.avatar_url}") 
                            
                                embed.add_field(name=f'Bank', value=f'{bank} {currency}', inline = False)
                                embed.add_field(name=f'Wallet', value=f'{wallet} {currency}', inline = False)
                                embed.add_field(name=f'Total money', value=f'{total} {currency}', inline = False)

                                embed.set_footer(text=f"┗Requested by {ctx.author}")

                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                        else:
                            embed = discord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                                colour = 0x983925
                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')

                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
    
@client.command()
async def deposit(ctx, amount : int):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if amount < 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')  
                
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                    )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')

                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    new_bank = amount + data["bank"]
                                    new_wallet = data["wallet"] - amount
                                if data["wallet"] >= amount:
                                    embed = discord.Embed(
                                        title = f"ฝากเงินเข้าบัญชีธนาคารสําเร็จ",
                                        description = f"ได้ทําการฝากเงินจํานวน {amount} {currency} เข้าธนาคาร",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = discord.Embed(
                                        title = "จํานวนเงินในกระเป๋าตังไม่พอ",
                                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                            
                    
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
        
        if server_language == "English":
            if amount < 0:
                embed = discord.Embed(
                    title = "Amount cannot be negative",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')  
                
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')

                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    new_bank = amount + data["bank"]
                                    new_wallet = data["wallet"] - amount
                                if data["wallet"] >= amount:
                                    embed = discord.Embed(
                                        title = f"Deposit",
                                        description = f"Deposit {amount} {currency} to the bank",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = discord.Embed(
                                        title = "Not enough money in the wallet",
                                        description = f"use {COMMAND_PREFIX}openbal to open balance",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                            
                    
                        else:
                            embed = discord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')      
                            
                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

@deposit.error
async def deposit_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "จํานวนเงินที่จะฝากเข้าธนาคาร",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะฝากเข้าธนาคาร ``{COMMAND_PREFIX}deposit (amount)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def withdraw(ctx, amount : int):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if amount <= 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')  
                
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                    )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    new_bank = data["bank"] - amount
                                    new_wallet = data["wallet"] + amount
                                if data["bank"] >= amount:
                                    embed = discord.Embed(
                                        title = f"ถอนเงินเสําเร็จ",
                                        description = f"ได้ทําการถอนเงินจํานวน {amount} {currency}",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = discord.Embed(
                                        title = "จํานวนเงินในกระเป๋าตังไม่พอ",
                                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                            
                    
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

        if server_language == "English":
            if amount < 0:
                embed = discord.Embed(
                    title = "Amount cannot be negative",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')    
                
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} don't have a balance",
                                    description = f"use {COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    new_bank = data["bank"] - amount
                                    new_wallet = data["wallet"] + amount
                                if data["bank"] >= amount:
                                    embed = discord.Embed(
                                        title = f"Withdraw",
                                        description = f"Withdraw {amount} {currency} from the bank",
                                        colour = 0xB9E7A5
                                    )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')

                                    collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":new_bank,"wallet":new_wallet}})
            
                                else:
                                    embed = discord.Embed(
                                        title = "Not enough money in the bank",
                                        description = f"use {COMMAND_PREFIX}openbal to open balance",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')                   
                    
                        else:
                            embed = discord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸') 

@withdraw.error
async def withdraw_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "จํานวนเงินที่จะถอนจากธนาคาร",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะถอนจากธนาคาร ``{COMMAND_PREFIX}withdraw (amount)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def addcredit(ctx ,amount : int , member: discord.Member = None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if amount <= 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸') 
            
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            receiver = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = discord.Embed(
                                    title = f"{member.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                for data in receivermoney:
                                    receivernew_bank = data["bank"] + amount

                                collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                embed = discord.Embed(
                                    title = f"โอนเงินสําเร็จ",
                                    description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                    colour = 0xB9E7A5
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')      
                    
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
        
        if server_language == "English":
            if amount <= 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸') 
            
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            receiver = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                            if receiver is None:
                                embed = discord.Embed(
                                    title = f"{member.name} don't have a balance",
                                    description = f"use {COMMAND_PREFIX}openbal to open balance",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                        
                            else:
                                receivermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                for data in receivermoney:
                                    receivernew_bank = data["bank"] + amount

                                collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                embed = discord.Embed(
                                    title = f"โอนเงินสําเร็จ",
                                    description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                    colour = 0xB9E7A5
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')      
                    
                        else:
                            embed = discord.Embed(
                                title = "Command is disable",
                                description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')      
                            
                else:
                    embed = discord.Embed(
                        title = "Command is disable",
                        description = f"This command is disable please use {COMMAND_PREFIX}economy on",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

@addcredit.error
async def addcredit_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์ให้ตัง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 
    
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{COMMAND_PREFIX}pay (amount) @member``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
        

@client.command()
async def pay(ctx ,amount : int , member: discord.Member = None):
    languageserver = collectionlanguage.find_one({"guild_id":ctx.guild.id})
    if languageserver is None:
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed)
        await message.add_reaction('👍')

    else:
        language = collectionlanguage.find({"guild_id":ctx.guild.id})
        for data in language:
            server_language = data["Language"]
        
        if server_language == "Thai":
            if amount <= 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸') 
            
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                    )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    usernew_bank = data["bank"] - amount
                            
                                if data["bank"] >= amount:
                                    receiver = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                                    if receiver is None:
                                        embed = discord.Embed(
                                            title = f"{member.name} ยังไม่มีบัญชี",
                                            description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')
                                
                                    else:
                                        receivermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                        for data in receivermoney:
                                            receivernew_bank = data["bank"] + amount

                                        collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":usernew_bank}})
                                        collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                        embed = discord.Embed(
                                            title = f"โอนเงินสําเร็จ",
                                            description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = discord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
                                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')    
                    
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
        
        if server_language == "English":
            if amount <= 0:
                embed = discord.Embed(
                    title = "จํานวนเงินไม่สามารถติดลบได้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸') 
            
            else:
                guild = collection.find_one({"guild_id":ctx.guild.id})
                if not guild is None:
                    status = collection.find({"guild_id":ctx.guild.id})
                    for data in status:
                        currency = data["currency"]
                        if data["economy_system"] == "YES":
                            user = collectionmoney.find_one({"user_id":ctx.author.id})
                            if user is None:
                                embed = discord.Embed(
                                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                    colour = 0x983925
                                    )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')
                            
                            else:
                                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                                for data in usermoney:
                                    usernew_bank = data["bank"] - amount
                            
                                if data["bank"] >= amount:
                                    receiver = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                                    if receiver is None:
                                        embed = discord.Embed(
                                            title = f"{member.name} ยังไม่มีบัญชี",
                                            description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                                            colour = 0x983925
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')
                                
                                    else:
                                        receivermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                                        for data in receivermoney:
                                            receivernew_bank = data["bank"] + amount

                                        collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"bank":usernew_bank}})
                                        collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank}})
                                        embed = discord.Embed(
                                            title = f"โอนเงินสําเร็จ",
                                            description = f"ได้ทําการโอนเงินให้ {member.name} จํานวน {amount} {currency} เข้าธนาคาร",
                                            colour = 0xB9E7A5
                                        )
                                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                                        message  = await ctx.send(embed=embed)
                                        await message.add_reaction('💸')

                                else:
                                    embed = discord.Embed(
                                        title = "จํานวนเงินในธนาคารไม่พอ",
                                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                        colour = 0x983925
                                        )
                                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                                    message  = await ctx.send(embed=embed)
                                    await message.add_reaction('💸')    
                    
                        else:
                            embed = discord.Embed(
                                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')       
                            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')

@pay.error
async def pay_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{COMMAND_PREFIX}pay (amount) @member``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def slot(ctx, amount:int):
    if amount <= 0:
        embed = discord.Embed(
            title = "จํานวนเงินไม่สามารถติดลบได้",
            colour = 0x983925
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message  = await ctx.send(embed=embed)
        await message.add_reaction('💸') 
    
    else:
        guild = collection.find_one({"guild_id":ctx.guild.id})
        if not guild is None:
            status = collection.find({"guild_id":ctx.guild.id})
            for data in status:
                currency = data["currency"]
                if data["economy_system"] == "YES":
                    user = collectionmoney.find_one({"user_id":ctx.author.id})
                    if user is None:
                        embed = discord.Embed(
                            title = f"{ctx.author.name} ยังไม่มีบัญชี",
                            description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                            colour = 0x983925
                            )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')
                    
                    else:
                        usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                        for data in usermoney:
                            money  = data["wallet"]

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
                                collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                embed = discord.Embed(
                                    title = f"คุณได้เงินจำนวน {amount} {currency}",
                                    description = f"{result}",
                                    colour = 0xB9E7A5
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar_url}") 
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')

                            else:
                                currentmoney = money - amount
                                collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":currentmoney}})
                                embed = discord.Embed(
                                    title = f"คุณเสียเงินจำนวน {amount} {currency}",
                                    description = f"{result}",
                                    colour = 0x983925
                                )
                                embed.set_footer(text=f"┗Requested by {ctx.author}")
                                embed.set_author(name=f"SLOT MACHINE", icon_url=f"{ctx.author.avatar_url}") 
                                message  = await ctx.send(embed=embed)
                                await message.add_reaction('💸')

                        else:
                            embed = discord.Embed(
                                title = "จํานวนเงินในธนาคารไม่พอ",
                                description = f"ใช้คําสั่ง {COMMAND_PREFIX}bal เพื่อเช็คเงิน",
                                colour = 0x983925
                                )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸')    

                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')  
        else:
            embed = discord.Embed(
                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                colour = 0x983925
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message  = await ctx.send(embed=embed)
            await message.add_reaction('💸')

@slot.error
async def slot_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "จํานวนเงินที่จะลงพนัน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนเงินที่จะลงพนัน``{COMMAND_PREFIX}slot (amount)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setcurrency(ctx, *, currency):
    guild = collection.find_one({"guild_id":ctx.guild.id})
    if not guild is None:
        status = collection.find({"guild_id":ctx.guild.id})
        for data in status:
            if data["economy_system"] == "YES":
                try:
                    collection.update_one({"guild_id":ctx.guild.id},{"$set":{"currency":currency}})
                    embed = discord.Embed(
                        colour= 0x00FFFF,
                        title = "ตั้งค่าค่าเงิน",
                        description= f"ตั้ง ``{currency}`` เป็นค่าเงินสําเร็จ"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
         
                except:
                    embed = discord.Embed(
                        colour= 0x983925,
                        title = "ตั้งค่าค่าเงิน",
                        description= f"ไม่สามารถตั้ง ``{currency}`` เป็นค่าเงิน"
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")

                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
            else:
                embed = discord.Embed(
                    title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')

    else:
        embed = discord.Embed(
            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
            description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
            colour = 0x983925
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message  = await ctx.send(embed=embed)
        await message.add_reaction('💸')

@setcurrency.error
async def setcurrency_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ค่าเงิน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ค่าเงินที่จะเปลี่ยน ``{COMMAND_PREFIX}setcurrency (currency)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์เเอดมิน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

@client.command()
async def rob(ctx , member: discord.Member):
    guild = collection.find_one({"guild_id":ctx.guild.id})
    if not guild is None:
        status = collection.find({"guild_id":ctx.guild.id})
        for data in status:
            currency = data["currency"]
            status = data["economy_system"]
        if status == "YES":
            user = collectionmoney.find_one({"user_id":ctx.author.id})
            if user is None:
                embed = discord.Embed(
                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')
                
            else:
                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                for data in usermoney:
                    user_wallet = data["wallet"] 

                taking = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                if taking is None:
                    embed = discord.Embed(
                        title = f"{member.name} ยังไม่มีบัญชี",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                        colour = 0x983925
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')
                    
                else:
                    takingmoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                    for data in takingmoney:
                        victimwallet = data["wallet"] 

                    if victimwallet > 0:
                        percent = (random.randint(1,101))
                        if percent >= 30:
                            percentmoney = (random.randint(60,101))
                            stolen = (victimwallet * (percentmoney/100))
                            stolen = round(stolen)
                            victimnew_wallet = victimwallet - stolen
                            stolernew_wallet = user_wallet + stolen
                            collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":stolernew_wallet}})
                            collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"wallet":victimnew_wallet}})
                            embed = discord.Embed(
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
                            embed = discord.Embed(
                                title = f"ปล้นเงินจาก {member.name} ไม่สําเร็จ",
                                description = f"เพราะว่า {member.name} {randomreason}",
                                colour = 0x983925

                            )
                            embed.set_footer(text=f"┗Requested by {ctx.author}")
                            message  = await ctx.send(embed=embed)
                            await message.add_reaction('💸') 

                    else:
                        embed = discord.Embed(
                            title = f"ปล้นเงินจาก {member.name} ไม่สําเร็จ",
                            description = f"เพราะว่า {member.name} ไม่มีเงินในกระเป๋าตังสักบาท",
                            colour = 0x983925

                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸') 

        else:
            embed = discord.Embed(
                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                colour = 0x983925
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message  = await ctx.send(embed=embed)
            await message.add_reaction('💸')       
                    
    else:
        embed = discord.Embed(
            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
            description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
            colour = 0x983925
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message  = await ctx.send(embed=embed)
        await message.add_reaction('💸')

@client.command()
async def work(ctx):
    guild = collection.find_one({"guild_id":ctx.guild.id})
    if not guild is None:
        status = collection.find({"guild_id":ctx.guild.id})
        for data in status:
            currency = data["currency"]
            status = data["economy_system"]
        if status == "YES":
            user = collectionmoney.find_one({"user_id":ctx.author.id})
            if user is None:
                embed = discord.Embed(
                    title = f"{ctx.author.name} ยังไม่มีบัญชี",
                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')
            
            else:
                usermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":ctx.author.id})
                for data in usermoney:
                    user_wallet = data["wallet"]
                
                money = (random.randint(1000,9500))
                usernew_wallet = user_wallet + money
                work = ["ล้างจาน","ถูพื้น","ขายตัว","ขับ taxi","ไปส่ง pizza","ขับ Grab"]
                num = (random.randint(0,5))
                ranwork = work[num]
                collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":ctx.author.id},{"$set":{"wallet":usernew_wallet}})
                embed = discord.Embed(
                    title = f"",
                    description = f"{ctx.author} ได้ {ranwork} เเละได้รับเงิน {money}{currency}",
                    colour = 0xB9E7A5
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')
        else:
            embed = discord.Embed(
                title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                colour = 0x983925
                )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message  = await ctx.send(embed=embed)
            await message.add_reaction('💸')       
            
    else:
        embed = discord.Embed(
            title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
            description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
            colour = 0x983925
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message  = await ctx.send(embed=embed)
        await message.add_reaction('💸')

@client.command()
@commands.has_permissions(administrator=True)
async def resetmoney(ctx , member: discord.Member = None):
    if member is None:
        try:
            embed = discord.Embed(
                colour = 0x00FFFF,
                title = f"คุณเเน่ในที่จะ reset เงินของ {ctx.author}",
                description = "พิม YES / NO")

            embed.set_footer(text=":")
            message = await ctx.send(embed=embed)

            choice = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
            userchoice = choice.content
            userchoice = userchoice.lower()
            await asyncio.sleep(1) 
            await choice.delete() 
            await asyncio.sleep(1) 
            await message.delete() 

        except asyncio.TimeoutError:
            await message.delete()
        
        if userchoice == "yes":
            guild = collection.find_one({"guild_id":ctx.guild.id})
            if not guild is None:
                status = collection.find({"guild_id":ctx.guild.id})
                for data in status:
                    currency = data["currency"]
                    status = data["economy_system"] 
                if status == "YES":
                    receiver = collectionmoney.find_one({"guild_id":ctx.guild.id , "user_id":member.id})
                    if receiver is None:
                        embed = discord.Embed(
                            title = f"{member.name} ยังไม่มีบัญชี",
                            description = f"ใช้คําสั่ง {COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                            colour = 0x983925
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')
                
                    else:
                        receivermoney = collectionmoney.find({"guild_id":ctx.guild.id , "user_id":member.id})
                        for data in receivermoney:
                            receivernew_bank = data["bank"] * 0
                            receivernew_wallet = data["bank"] * 0

                        collectionmoney.update_one({"guild_id":ctx.guild.id , "user_id":member.id},{"$set":{"bank":receivernew_bank,"wallet":receivernew_wallet}})
                        embed = discord.Embed(
                            title = f"โอนเงินสําเร็จ",
                            description = f"ได้ทําการ reset เงินของ {ctx.author}",
                            colour = 0xB9E7A5
                        )
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        message  = await ctx.send(embed=embed)
                        await message.add_reaction('💸')      
            
                else:
                    embed = discord.Embed(
                        title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                        colour = 0x983925
                        )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message  = await ctx.send(embed=embed)
                    await message.add_reaction('💸')       
                        
            else:
                embed = discord.Embed(
                    title = "คําสั่งนี้ถูกปิดใช้งานโดยเซิฟเวอร์",
                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}economy on เพื่อเปิดใช้",
                    colour = 0x983925
                    )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
                message  = await ctx.send(embed=embed)
                await message.add_reaction('💸')

@resetmoney.error
async def resetmoney_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์ให้ตัง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 
    
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อสมาชิกที่จะโอนเงินให้ เเละจํานวนเงินที่จะทําการโอน ``{COMMAND_PREFIX}pay (amount) @member``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command(aliases =["vfy"])
async def verify(ctx):
    guild = collection.find_one({"guild_id":ctx.guild.id})
    if not guild is None:
        results = collection.find({"guild_id":ctx.guild.id})
        for data in results:
            if data["verification_system"] == "YES":
                if data["verification_channel_id"] != "None":
                    channel_id = int(data["verification_channel_id"])
                    channel = client.get_channel(channel_id)

                    if int(ctx.channel.id) == data["verification_channel_id"]:
                        if not Path('arial.ttf').exists():
                            dirname = os.path.dirname(os.path.abspath(__file__))
                            fontfile = os.path.join(dirname, 'arial.ttf')
    
                        else:
                            fontfile = 'arial.ttf'

                        chars = 'abcdefghifklmnopqrstwxyzABCDEFGHIJKLMNOP12345678910'
                        text = ''
                        for i in range(6):
                            text = text + random.choice(chars)
                        img = Image.new('RGB', (200, 50))

                        font = ImageFont.truetype(fontfile, 40)
                        imgdraw = ImageDraw.Draw(img)
                        imgdraw.text((45,5), text, fill=(255,255,0) , font=font)
                        img.save('captcha.png')
                        file = discord.File("captcha.png", filename="captcha.png")

                        embed = discord.Embed(
                            colour  = 0x00FFFF,
                            title = "Captcha"
                        )
                        embed.set_image(url = "attachment://captcha.png")
                        embed.set_footer(text=f"┗Requested by {ctx.author}")
                        embed.set_author(name=f"กรุณาพิมพ์ข้อความตามภาพเพื่อยืนยันตัวตน", icon_url=f"{ctx.author.avatar_url}") 

                        message = await ctx.send(embed=embed , file=file)

                        try:
                            answer = await client.wait_for("message", check=lambda user:user.author.id == ctx.author.id, timeout=20)
                            answer = answer.content
                            if answer == text:
                                embed = discord.Embed(
                                description = f":white_check_mark: คุณได้รับการยืนยันแล้ว",
                                colour =  0xB9E7A5
                                )
                                embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
                                await message.edit(embed=embed)

                                if data["verification_role_give_id"] != "None":
                                    try:
                                        role = data["verification_role_give_id"]
                                        role = int(role)
                                        role = ctx.guild.get_role(role)
                                        await ctx.author.add_roles(role)

                                    except Exception:
                                        pass

                                else: 
                                    pass

                                if data["verification_role_remove_id"] != "None":
                                    try:
                                        role = data["verification_role_remove_id"]
                                        role = int(role)
                                        role = ctx.guild.get_role(role)
                                        await ctx.author.add_roles(role)

                                    except Exception:
                                        pass
                    
                                else:
                                    pass  
                    
                            else:
                                embed = discord.Embed(
                                    description = f":x: คุณพิมพ์ข้อความใน captcha ไม่ถูกต้องกรุณาพิมพ์ {COMMAND_PREFIX}verify บนห้อง {ctx.channel.mention} เพื่อยืนยันตัวตนใหม่อีกครั้ง",
                                    colour =  0x983925
                                )
                                embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
                                await message.edit(embed=embed)
                    
                        except asyncio.TimeoutError:
                            embed = discord.Embed(
                                description = f":x: คุณใช้เวลานานเกินไป {COMMAND_PREFIX}verify บนห้อง {ctx.channel.mention} เพื่อยืนยันตัวตนใหม่อีกครั้ง",
                                colour =  0x983925
                            )
                            embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
                            await message.edit(embed=embed)      

                    else:
                        embed = discord.Embed(
                            description = f":x: คุณสามารถใช้คําสั่งนี้ได้ในห้อง {channel}",
                            colour =  0x983925
                        )
                        embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
                        await ctx.send(embed=embed)  
                        
                else:
                    embed = discord.Embed(
                        title = f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                        description = f"ใช้คําสั่ง {COMMAND_PREFIX}setverification #channel",
                        colour =  0x983925
                    )
                    await ctx.send(embed=embed)          

            else:
                embed = discord.Embed(
                    title = f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
                    description = f"ใช้คําสั่ง {COMMAND_PREFIX}setverification #channel",
                    colour =  0x983925
                    )   
                await ctx.send(embed=embed)   
    
    else:
        embed = discord.Embed(
            title = f"เซิฟเวอร์น้ยังไม่ได้ตั้งค่าห้อง verify",
            description = f"ใช้คําสั่ง {COMMAND_PREFIX}setverification #channel",
            colour =  0x983925
        )   
        await ctx.send(embed=embed)

@client.group(invoke_without_command=True)
async def verifyrole(ctx):
    embed = discord.Embed(
        colour = 0x00FFFF,
        description = "ต้องระบุ give / remove"
    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@verifyrole.command(aliases=['give'])
@commands.has_permissions(administrator=True)
async def _give(ctx, role: discord.Role):
    server = collection.find_one({"guild_id":ctx.guild.id})
    if server is None:
        newserver = {"guild_id":ctx.guild.id,
        "welcome_id":"None",
        "leave_id":"None",
        "webhook_url":"None",
        "webhook_channel_id":"None",
        "webhook_status":"None",
        "introduce_channel_id":"None",
        "introduce_frame":"None",
        "introduce_role_give_id":"None",
        "introduce_role_remove_id":"None",
        "introduce_status":"YES",
        "level_system":"NO",
        "economy_system":"NO",
        "currency":"$",
        "verification_system":"NO",
        "verification_channel_id":"None",
        "verification_role_give_id":"None",
        "verification_role_remove_id":"None"
        }
        collection.insert_one(newserver)
        results = collection.find_one({"guild_id":ctx.guild.id})
        for data in results:
            if data["verification_role_give_id"] == "None": 
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_give_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title = "ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                    description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
        
            else:
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_give_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                    description= f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
    
    else:
        results = collection.find_one({"guild_id":ctx.guild.id})
        for data in results:
            if data["verification_role_give_id"] == "None": 
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_give_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title = "ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                    description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")

                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
        
            else:
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_give_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ได้หลังจากยืนยันตัวตน",
                    description= f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

@_give.error
async def verifygive_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุยศที่จะให้หลังจากยืนยันตัวตน",
            description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะให้หลังจากยืนยันตัวตน ``{COMMAND_PREFIX}setrole give @role``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@verifyrole.command(aliases=['remove'])
@commands.has_permissions(administrator=True)
async def _remove(ctx, role: discord.Role):
    server = collection.find_one({"guild_id":ctx.guild.id})
    if server is None:
        newserver = {"guild_id":ctx.guild.id,
        "welcome_id":"None",
        "leave_id":"None",
        "webhook_url":"None",
        "webhook_channel_id":"None",
        "webhook_status":"None",
        "introduce_channel_id":"None",
        "introduce_frame":"None",
        "introduce_role_give_id":"None",
        "introduce_role_remove_id":"None",
        "introduce_status":"YES",
        "level_system":"NO",
        "economy_system":"NO",
        "currency":"$",
        "verification_system":"NO",
        "verification_channel_id":"None",
        "verification_role_give_id":"None",
        "verification_role_remove_id":"None"
        }
        collection.insert_one(newserver)
        results = collection.find_one({"guild_id":ctx.guild.id})
        print(results)
        for data in results:
            if data["verification_role_remove_id"] == "None": 
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_remove_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                    description= f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
        
            else:
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_remove_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                    description= f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
    
    else:
        results = collection.find({"guild_id":ctx.guild.id})
        for data in results:
            if data["verification_role_remove_id"] == "None": 
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_remove_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                    description= f"ยศที่ลบถูกตั้งเป็นถูกตั้งเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
        
            else:
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_role_remove_id":role.id}})
                embed = discord.Embed(
                    colour= 0x00FFFF,
                    title= "ตั้งค่ายศที่ลบหลังจากยืนยันตัวตน",
                    description= f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
                )
                embed.set_footer(text=f"┗Requested by {ctx.author}")
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

@_remove.error
async def verifyremove_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุยศที่จะลบหลังจากยืนยันตัวตน",
            description = f" ⚠️``{ctx.author}`` จะต้องระบุยศที่จะลบหลังจากยืนยันตัวตน ``{COMMAND_PREFIX}setrole remove @role``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setverify(ctx , channel:discord.TextChannel):
     
    server = collection.find_one({"guild_id":ctx.guild.id})
    if server is None:
        newserver = {"guild_id":ctx.guild.id,
        "welcome_id":"None",
        "leave_id":"None",
        "webhook_url":"None",
        "webhook_channel_id":"None",
        "webhook_status":"None",
        "introduce_channel_id":"None",
        "introduce_frame":"None",
        "introduce_role_give_id":"None",
        "introduce_role_remove_id":"None",
        "introduce_status":"YES",
        "level_system":"NO",
        "economy_system":"NO",
        "currency":"$",
        "verification_system":"NO",
        "verification_channel_id":"None",
        "verification_role_give_id":"None",
        "verification_role_remove_id":"None"
        }
        collection.insert_one(newserver)
    results = collection.find({"guild_id":ctx.guild.id})
    for data in results:
        if data["verification_channel_id"] == "None":
            collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_channel_id":channel.id}})

            embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องยืนยันตัวตน",
            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
        )

            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

        else:
            collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_channel_id":channel.id}})

            embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่าห้องยืนยันตัวตน",
            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
        )
        
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')

    else:
        results = collection.find({"guild_id":ctx.guild.id})
        for data in results:
            if data["verification_channel_id"] == "None":
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_channel_id":channel.id}})

                embed = discord.Embed(
                colour= 0x00FFFF,
                title = "ตั้งค่าห้องยืนยันตัวตน",
                description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
            )

                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')

            else:
                collection.update_one({"guild_id":ctx.guild.id},{"$set":{"verification_channel_id":channel.id}})

                embed = discord.Embed(
                colour= 0x00FFFF,
                title= "ตั้งค่าห้องยืนยันตัวตน",
                description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
            )
        
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')         

@setverify.error
async def setverify_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ตั้งค่าห้องยืนยันตัวตน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือน ``{COMMAND_PREFIX}setverify #text-channel``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์ตั้งค่าห้อง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def join(ctx):
    await ctx.author.voice.channel.connect() #Joins author's voice channel

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@client.command()
async def play(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send('You are not connected to a voice channel')
        return
    else:
        await ctx.author.voice.channel.connect()
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            await ctx.send(f"Playing {song.name}")
        else:
            song = await player.queue(url, search=True)
            await ctx.send(f"Queued {song.name}")

@client.command()
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name}")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name}")

@client.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped")

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        await ctx.send(f"Enabled loop for {song.name}")
    else:
        await ctx.send(f"Disabled loop for {song.name}")

@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await ctx.send(f"{', '.join([song.name for song in player.current_queue()])}")

@client.command()
async def np(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
    else:
        await ctx.send(f"Skipped {data[0].name}")

@client.command()
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed {song.name} from queue")

@client.command()
async def cleancmd(ctx):
    clearcmd()
    print(ASCII_ART)
    print(f"BOT NAME : {client.user}")
    print(f"BOT ID : {client.user.id}")
    print("BOT STATUS : ONLINE")
    print("SERVER : " + str(len(client.guilds)))
    print("USER : " + str(len(client.users)))
    print("")
    print("CONSOLE : ")
    print("")

@client.command()
async def test(ctx):
    await ctx.send("Bot online เเล้ว")

###########################################################
#            /\                                           #
#/vvvvvvvvvvvv \--------------------------------------,   #
#`^^^^^^^^^^^^ /====================================="    #
#            \/                                           #
#REACT#1120 - Thailand                                    #
###########################################################
#https://github.com/reactxsw
    
#Bot login using token
client.run(TOKEN , bot = True)
