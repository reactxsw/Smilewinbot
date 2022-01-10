# coding=utf-8
#import
import settings
import subprocess
import datetime  
import os
import platform
import logging
import asyncio
import sys
import traceback
import nextcord
from nextcord.ext import commands ,tasks
from datetime import date, timedelta
from itertools import cycle
from cogs.music import MusicButton

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/botlog.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intent = nextcord.Intents.default()
intent.members = True

developer = "REACT#1120"
PYTHON_VERSION = platform.python_version()
OS = platform.system()

status = cycle([f' S       | {settings.COMMAND_PREFIX}help ' 
              , f' Sm      | {settings.COMMAND_PREFIX}help ' 
              , f' Smi     | {settings.COMMAND_PREFIX}help '
              , f' Smil    | {settings.COMMAND_PREFIX}help '
              , f' Smile   | {settings.COMMAND_PREFIX}help '
              , f' Smilew  | {settings.COMMAND_PREFIX}help ' 
              , f' Smilewi | {settings.COMMAND_PREFIX}help '
              , f' Smilewin| {settings.COMMAND_PREFIX}help '
              , f' Smilewin| {settings.COMMAND_PREFIX}help '])

ASCII_ART = """
                                   ____            _ _               _       
                                  / ___| _ __ ___ (_) | _____      _(_)_ __  
                                  \___ \| '_ ` _ \| | |/ _ \ \ /\ / / | '_ \ 
                                    __) | | | | | | | |  __/\ V  V /| | | | |
                                  |____/|_| |_| |_|_|_|\___| \_/\_/ |_|_| |_|
                                                                   REACT#1120 
""" 

bot = commands.AutoShardedBot(command_prefix = ([settings.COMMAND_PREFIX,"/r "]),case_insensitive=True ,intents=intent , strip_after_prefix=True)
bot.remove_command('help')

start_time = datetime.datetime.utcnow()

async def clearcmd():
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

@tasks.loop(seconds=5)
async def change_status():
    await bot.wait_until_ready()
    await bot.change_presence(status = nextcord.Status.idle, activity=nextcord.Game(next(status)))


@tasks.loop(seconds=120)
async def serverstat():
    await bot.wait_until_ready()
    results = settings.collectionstatus.find({"status_system":"YES"})
    for data in await results.to_list(length=10000):
        if data["guild_id"] in bot.guilds:
            guild = bot.get_guild(data["guild_id"])
            print(data["guild_id"])
            memberonly = len([member for member in guild.members if not member.bot])
            botonly = int(guild.member_count) - int(memberonly)
            total_member_channel = bot.get_channel(data["status_total_id"])
            member_channel = bot.get_channel(data["status_members_id"])
            bot_channel = bot.get_channel(data["status_bots_id"])
            online_channel = bot.get_channel(data["status_online_id"])
            memberonline = len([member for member in guild.members if not member.bot and member.status is nextcord.Status.online])
            if total_member_channel:
                await total_member_channel.edit(name = f"︱👥 Total : {guild.member_count}")
            if member_channel:
                await member_channel.edit(name=f"︱👥 Members : {memberonly}")
            if bot_channel:
                await bot_channel.edit(name = f"︱👥 Bots : {botonly}")
            if online_channel:
                await online_channel.edit(name = f"︱🟢 Online {memberonline}")
        
        else:
            pass

async def checkMongo():                 
    try:
        await settings.client.admin.command('ismaster')
        print("Successfully connected to mongodb")
    except Exception:
        print("Unable to connect to mongodb")

def loadcogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Successfully loaded {filename}")
            
            except Exception as e:
                print(f"Failed to load {filename}")
                print(e)
                traceback.print_exc()
    
def unloadcogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{filename[:-3]}")
                print(f"Successfully unloaded {filename}")
            
            except Exception as e:
                print(f"Failed to unload {filename}")
                print(e)
                traceback.print_exc()

@bot.event
async def on_ready():
    await settings.collectionmusic.delete_many({})
    try:
        change_status.start()
        serverstat.start()
    except RuntimeError:
        pass
    print_ascii_art()
    bot.add_view(MusicButton())
    try:
        channel = bot.get_channel(int(settings.logchannel))
        embed = nextcord.Embed(
            title = f"Bot is online",
            colour = 0x56FF2D
        )
        await channel.send(embed=embed)

    except Exception as e: 
        print(e)
        pass

def print_ascii_art():
    server= (str(len(bot.guilds)))
    server_space = (27 - int(len(server)))*(" ")
    user = (str(len(bot.users)))
    user_space = (29 - int(len(user)))*(" ")
    print(f"{ASCII_ART}")
    print(f"                                   ╔══════════════════════════════════════╗")
    print(f"                                   ║  BOT NAME : {bot.user}            ║")
    print(f"                                   ║  BOT ID : {bot.user.id}         ║")
    print(f"                                   ║  BOT STATUS : ONLINE                 ║")
    print(f"                                   ║  SERVER : {server}{server_space}║")
    print(f"                                   ║  USER : {user}{user_space}║")
    print(f"                                   ║                                      ║")
    print(f"                                   ╚══════════════════════════════════════╝")  
    print("")

@bot.command(aliases=["reload"])
@commands.is_owner()
async def reloadcogs(ctx):
    await clearcmd()
    unloadcogs()
    await asyncio.sleep(2)
    loadcogs()
    await clearcmd()
    await asyncio.sleep(0.2)
    print_ascii_art()
    print("Reloaded all cogs!")
    await ctx.send("Reloaded all cogs successfully!")


@bot.command()
async def cleancmd(ctx):
    await clearcmd()
    await checkMongo()
    print_ascii_art()
    await ctx.send("Cmd cleared")

@bot.event
async def on_connect():
    print("Connected to discord API")

def main():
    loadcogs()
    try:
        bot.run(settings.TOKEN ,reconnect=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())