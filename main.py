# coding=utf-8
#import
import settings

import discord  
import datetime  
import os
import platform
import logging
import asyncio
import sys
import traceback
import asyncpraw

#from
from discord.channel import StoreChannel
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands, tasks
from discord.utils import get
from datetime import date, timedelta
from itertools import cycle

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/botlog.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


os.system("title Smilewin#0644")

developer = "REACT#1120"
PYTHON_VERSION = platform.python_version()
OS = platform.system()

status = cycle([f' REACT  | {settings.COMMAND_PREFIX}help ' 
              , f' R      | {settings.COMMAND_PREFIX}help ' 
              , f' RE     | {settings.COMMAND_PREFIX}help '
              , f' REA    | {settings.COMMAND_PREFIX}help '
              , f' REAC   | {settings.COMMAND_PREFIX}help '
              , f' REACT  | {settings.COMMAND_PREFIX}help ' 
              , f' REACT! | {settings.COMMAND_PREFIX}help '])

ASCII_ART = """
                                   ____            _ _               _       
                                  / ___| _ __ ___ (_) | _____      _(_)_ __  
                                  \___ \| '_ ` _ \| | |/ _ \ \ /\ / / | '_ \ 
                                    __) | | | | | | | |  __/\ V  V /| | | | |
                                  |____/|_| |_| |_|_|_|\___| \_/\_/ |_|_| |_|
                                                                   REACT#1120
""" 

async def clearcmd():
    if platform.system() == ("Windows"):
        os.system("cls")
    
    else:
        os.system("clear")

bot = commands.AutoShardedBot(command_prefix = settings.COMMAND_PREFIX,case_insensitive=True ,intents=discord.Intents.all() , strip_after_prefix=True)
bot.remove_command('help')

start_time = datetime.datetime.utcnow()

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(status = discord.Status.idle, activity=discord.Game(next(status)))

async def checkMongo():
    try:
        await settings.client.admin.command('ismaster')
        print("Successfully connected to mongodb")
    except Exception:
        print("Unable to connect to mongodb")

async def loadcogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Successfully loaded {filename}.py")
            
            except:
                print(f"Failed to load {filename}.py")
                traceback.print_exc()
    
async def unloadcogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                bot.unload_extension(f"cogs.{filename[:-3]}")
                print(f"Successfully loaded {filename}")
            
            except:
                print(f"Failed to unload {filename}")
                traceback.print_exc()

@bot.event
async def on_ready():
    await loadcogs()
    await checkMongo()
    await clearcmd()
    space = (" ")
    server= (str(len(bot.guilds)))
    server_space = (27 - int(len(server)))*space
    user = (str(len(bot.users)))
    user_space = (29 - int(len(user)))*space
    change_status.start()
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
    channel = bot.get_channel(id = int(settings.logchannel))
    embed = discord.Embed(
        title = f"Bot is online",
        colour = 0x56FF2D
    )
    await channel.send(embed=embed)

async def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
async def clearcmd():
    if platform.system() == ("Windows"):
        os.system("cls")
    
    else:
        os.system("clear")



@bot.command()
@commands.is_owner()
async def restart(ctx):
    await clearcmd()
    await ctx.send("Restarting...")
    await asyncio.sleep(5)
    await restart_program()

@bot.command()
async def howmanycommand(ctx):
    for command in bot.commands:
        print(command)

@bot.command()
@commands.is_owner()
async def reloadcogs(ctx):
    await clearcmd()
    await unloadcogs()
    await asyncio.sleep(2)
    await loadcogs()

@bot.command()
async def cleancmd(ctx):
    await clearcmd()
    print(ASCII_ART)
    print(f"BOT NAME : {bot.user}")
    print(f"BOT ID : {bot.user.id}")
    print("BOT STATUS : ONLINE")
    print("SERVER : " + str(len(bot.guilds)))
    print("USER : " + str(len(bot.users)))
    print("")
    print("CONSOLE : ")
    print("")

    
def main():
    try:
        bot.run(settings.TOKEN , bot = True,reconnect=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    asyncio.run(main())