# coding=utf-8
#import
import settings
import subprocess
import discord  
import datetime  
import os
import platform
import logging
import asyncio
import sys
import traceback

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

intent = discord.Intents.all()

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

bot = commands.AutoShardedBot(command_prefix = commands.when_mentioned_or(settings.COMMAND_PREFIX),case_insensitive=True ,intents=intent , strip_after_prefix=True)
bot.remove_command('help')

start_time = datetime.datetime.utcnow()

async def clearcmd():
    subprocess.call('cls' if os.name == 'Windows' else 'clear', shell=False)

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
                print(f"Successfully loaded {filename}")
            
            except Exception as e:
                print(f"Failed to load {filename}")
                print(e)
                traceback.print_exc()
    
async def unloadcogs():
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
    await loadcogs()
    await checkMongo()
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

@bot.command()
@commands.is_owner()
async def restartbot(ctx):
    await clearcmd()
    await ctx.send("Restarting...")
    await asyncio.sleep(5)
    await restart_program()
    await clearcmd()

@bot.command()
@commands.is_owner()
async def reloadcogs(ctx):
    await clearcmd()
    await unloadcogs()
    await asyncio.sleep(2)
    await loadcogs()
    await clearcmd()

@bot.command()
async def cleancmd(ctx):
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

@bot.event
async def on_connect():
    print("Connected to discord API")

def main():
    try:
        bot.run(settings.TOKEN , bot = True,reconnect=True)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
