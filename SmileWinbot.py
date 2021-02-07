#import
import discord , asyncio , datetime , itertools , os , praw , requests , random , urllib , aiohttp , bs4 ,json ,humanize , time , platform , re ,sqlite3
#from
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands, tasks
from discord.utils import get
from datetime import date, timedelta
from itertools import cycle
from bs4 import BeautifulSoup,element
from bs4 import BeautifulSoup as bs4
from urllib.parse import urlencode
from captcha.image import ImageCaptcha
from threading import Thread


#INFORMATION THAT CAN TO BE CHANGE
TOKEN = '______________________________'
COMMAND_PREFIX = "/r "

developer = "REACT#1120"
CLIENTID = ______________________________
PYTHON_VERSION = platform.python_version()
OS = platform.system()
#tracker.gg api key
headers = {
        'TRN-Api-Key': '______________________________'
    }

openweathermapAPI = "______________________________"

reddit = praw.Reddit(client_id="______________________________",
                     client_secret="______________________________",
                     username="______________________________",
                     password="______________________________",
                     user_agent="Smilewin")


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

#I don't even know what is this but if it work it work
intents = discord.Intents.default()
intents.members = True
client = discord.Client()
client = commands.Bot(command_prefix = COMMAND_PREFIX,  case_insensitive=True ,intents=intents)
start_time = datetime.datetime.utcnow()
client.remove_command('help')

print(ASCII_ART)
print("BOT STATUS : OFFLINE")

@client.event
async def on_ready():
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Main(
        guild_id TEXT,
        welcome_id TEXT,
        leave_id TEXT
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhook(
        guild_id TEXT,
        webhook_url TEXT,
        channel_id TEXT,
        status TEXT
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Introduce(
        guild_id TEXT,
        channel_id TEXT,
        boarder TEXT,
        giverole_id TEXT,
        removerole_id TEXT,
        status TEXT
        )
        ''')
    change_status.start()
    clearcmd()
    clearcmd()
    print(ASCII_ART)
    print(f"BOT NAME : {client.user}")
    print("BOT STATUS : ONLINE")
    print("SERVER : " + str(len(client.guilds)))
    print("")
    print("CONSOLE : ")
    print("")

@client.group(invoke_without_command=True)
async def setrole(ctx):
    embed = discord.Embed(
        colour = 0x00FFFF,
        description = "ต้องระบุ give / remove"
    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@setrole.command()
@commands.has_permissions(administrator=True)
async def give(ctx, role: discord.Role):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT giverole_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Introduce(guild_id, giverole_id) VALUES(?,?)")
        val = (ctx.guild.id , role.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
            description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Introduce SET giverole_id = ? WHERE guild_id = ?")
        val = (role.id , ctx.guild.id)
        
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
            description= f"ยศที่ได้ถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
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

@setrole.command()
@commands.has_permissions(administrator=True)
async def remove(ctx, role: discord.Role):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT removerole_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Introduce(guild_id, removerole_id) VALUES(?,?)")
        val = (ctx.guild.id , role.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่ายศที่ได้หลังเเนะนําตัว",
            description= f"ยศที่ได้ถูกตั้งเป็น {role.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Introduce SET removerole_id = ? WHERE guild_id = ?")
        val = (role.id , ctx.guild.id)
        
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่ายศที่ลบหลังเเนะนําตัว",
            description= f"ยศที่ลบถูกตั้งเป็นถูกอัพเดตเป็น {role.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
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

@client.command()
@commands.has_permissions(administrator=True)
async def setintroduce(ctx, channel:discord.TextChannel):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT channel_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        status = "yes"
        sql = ("INSERT INTO Introduce(guild_id, channel_id , status) VALUES(?,?,?)")
        val = (ctx.guild.id , channel.id , status)

        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเนะนําตัว",
            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Introduce SET channel_id = ? WHERE guild_id = ?")
        val = (channel.id , ctx.guild.id)
        
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่าห้องเเนะนําตัว",
            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@setintroduce.error
async def setintroduce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setboarder(ctx, *,boarder):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT boarder FROM Introduce WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Introduce(guild_id, boarder) VALUES(?,?)")
        val = (ctx.guild.id , boarder)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่ากรอบเเนะนําตัว",
            description= f"กรอบได้ถูกตั้งเป็น {boarder}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    elif result is not None:
        sql = ("UPDATE Introduce SET boarder = ? WHERE guild_id = ?")
        val = (boarder , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่ากรอบเเนะนําตัว",
            description= f"กรอบได้ถูกอัพเดตเป็น {boarder}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@setboarder.error
async def setboarder_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.group(invoke_without_command=True)
async def introduce(ctx):
    embed = discord.Embed(
        colour = 0x00FFFF,
        description = "ต้องระบุ ON / OFF"
    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@introduce.command()
@commands.has_permissions(administrator=True)
async def on(ctx):
    status = "yes"
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT status FROM Introduce Where guild_id = {ctx.guild.id} ")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Introduce(guild_id, status) VALUES(?,?)")
        val = (ctx.guild.id , status)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเนะนําตัว",
            description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Introduce SET status = ? WHERE guild_id = ?")
        val = (status , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเนะนําตัว",
            description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@on.error
async def on_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
@introduce.command()
@commands.has_permissions(administrator=True)
async def off(ctx):
    status = "no"
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT status FROM Introduce WHERE guild_id = {ctx.guild.id} ")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Introduce(guild_id, status) VALUES(?,?)")
        val = (ctx.guild.id , status)  
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเนะนําตัว",
            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Introduce SET status = ? WHERE guild_id = ?")
        val = (status , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเนะนําตัว",
            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@off.error
async def off_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setwebhook(ctx , channel:discord.TextChannel):
    webhook = await ctx.channel.create_webhook(name='Smilewin')
    webhook = webhook.url
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT webhook_url FROM webhook WHERE guild_id = {ctx.guild.id} ")
    result = cursor.fetchone()
    if result is None:
        status = "yes"
        sql = ("INSERT INTO webhook(guild_id, webhook_url , channel_id , status) VALUES(?,?,?,?)")
        val = (ctx.guild.id , webhook ,channel.id, status)  
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE webhook SET webhook_url = ? , channel_id = ? WHERE guild_id = ?")
        val = (webhook , channel.id ,ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@setwebhook.error
async def setwebhook_error(ctx, error):
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
            title = "คุณจำไม่มีสิทธิ์ตั้ง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.group(invoke_without_command=True)
@commands.has_permissions(administrator=True)
async def chat(ctx):
    embed = discord.Embed(
        colour = 0x00FFFF,
        description = "ต้องระบุ ON / OFF"
    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@chat.error
async def chat_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@chat.command(aliases=['on'])
@commands.has_permissions(administrator=True)
async def _on(ctx):
    status = "yes"
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT status FROM webhook Where guild_id = {ctx.guild.id} ")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO webhook(guild_id, status) VALUES(?,?)")
        val = (ctx.guild.id , status)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE webhook SET status = ? WHERE guild_id = ?")
        val = (status , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ได้ทําการเปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@_on.error
async def _on_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@chat.command(aliases=['off'])
@commands.has_permissions(administrator=True)
async def _off(ctx):
    status = "no"
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT status FROM webhook WHERE guild_id = {ctx.guild.id} ")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO webhook(guild_id, status) VALUES(?,?)")
        val = (ctx.guild.id , status)  
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE webhook SET status = ? WHERE guild_id = ?")
        val = (status , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องคุยกับคนเเปลกหน้า",
            description= f"ได้ทําการปิดใช้งานคําสั่งนี้"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
    
    cursor.execute(sql, val)
    db.commit() 
    cursor.close()
    db.close()

@_off.error
async def _off_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่า",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx , channel:discord.TextChannel):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT welcome_id FROM Main WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Main(guild_id, welcome_id) VALUES(?,?)")
        val = (ctx.guild.id , channel.id)

        embed = discord.Embed(
            colour= 0x00FFFF,
            title = "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Main SET welcome_id = ? WHERE guild_id = ?")
        val = (channel.id , ctx.guild.id)
        
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์",
            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
        )
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@setwelcome.error
async def setwelcome_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุห้องที่จะตั้งเเจ้งเตือนคนเข้า",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือน ``{COMMAND_PREFIX}setwelcome #text-channel``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่าห้อง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def setleave(ctx , channel:discord.TextChannel):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT leave_id FROM Main WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO Main(guild_id, leave_id) VALUES(?,?)")
        val = (ctx.guild.id , channel.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
            description= f"ห้องได้ถูกตั้งเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    elif result is not None:
        sql = ("UPDATE Main SET leave_id = ? WHERE guild_id = ?")
        val = (channel.id , ctx.guild.id)
        embed = discord.Embed(
            colour= 0x00FFFF,
            title= "ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์",
            description= f"ห้องได้ถูกอัพเดตเป็น {channel.mention}"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@setleave.error
async def setleave_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุห้องที่จะตั้งเเจ้งเตือนคนออก",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ระบุห้องที่จะตั้งเป็นห้องเเจ้งเตือน ``{COMMAND_PREFIX}setleave #text-channel``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ตั้งค่าห้อง",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@tasks.loop(seconds=1)
async def change_status():
    await client.change_presence(status = discord.Status.idle, activity=discord.Game(next(status)))

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
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
        print(f"{ctx.author} try to clear {amount} of messages but it is more than 2000")

@clear.error
async def clear_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "จํานวนข้อความที่ต้องการที่จะลบ",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่จํานวนของข้อความที่จะลบหลังจากคําสั่ง ``{COMMAND_PREFIX}clear [จํานวน]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
        print(f"{ctx.author} try to clear message but is missing argument")

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ลบข้อความ",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``ลบข้อความ`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
        print(f"{ctx.author} try to clear message but is missing permission")

@client.event
async def on_member_join(member):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT welcome_id FROM Main WHERE guild_id = {member.guild.id}")
    result =cursor.fetchone()
    if result is None:
        return

    embed = discord.Embed(
        colour = 0x99e68b,
        title ='ยินดีต้อนรับเข้าสู่ smilewin !',
        description = 'กรุณาอ่านกฏเเละเคารพกันเเละกันด้วยนะครับ'
        )

    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    embed.set_footer(text='┗Powered by REACT')

    print(f"{member.name} have joined the server {member.guild.name}")
    channel = client.get_channel(id=int(result[0]))

    await channel.send(embed=embed)
    
@client.event
async def on_member_remove(member):
    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT leave_id FROM Main WHERE guild_id = {member.guild.id}")
    result =cursor.fetchone()
    if result is None:
        return

    embed = discord.Embed(
        colour=0x983925, 
        title = "Member leave",
        description= f"{member.name}ได้ออกจากเซิฟเวอร์"
        )

    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}") 
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    embed.set_footer(text='┗Powered by REACT')

    print(f"{member.name} have left the server {member.guild.name}")
    channel = client.get_channel(id=int(result[0]))

    await channel.send(embed=embed)

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
async def on_command_error(ctx, error):
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

@client.command()
async def membercount(ctx):
    totalmember =ctx.guild.member_count
    memberonly = len([member for member in ctx.guild.members if not member.bot])
    botonly = int(totalmember) - int(memberonly)
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

@client.command()
async def uptime(ctx): 
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]

    embed = discord.Embed(
        color = 0xffff00,
        title =  "เวลาทำงานของบอท Smilewin",
        description = "```🕒 " + uptime +"```",
    )

    embed.set_thumbnail(url="https://i.imgur.com/rPfYXGs.png")
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    embed.timestamp = datetime.datetime.utcnow()

    message = await ctx.send(embed=embed)
    await message.add_reaction('🕒')

@client.command(aliases=['stat'])
async def botinfo(ctx):
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]

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
    embed.add_field(name='📁 ``คําสั่งทั้งหมด``', value=f'{len(client.all_commands)}',inline =True)
    embed.add_field(name='🤖 ``คําสั่งช่วยเหลือ``', value=f'{COMMAND_PREFIX}help',inline =True)
    embed.add_field(name='🤖 ``เวลาทำงาน``', value=f'{uptime}',inline =True)
    embed.add_field(name='🤖 ``Ping ของบอท``', value=f'{round(client.latency * 1000)}ms',inline =True)
    embed.add_field(name='💻 ``ระบบปฏิบัติการ``', value=f'{OS}',inline =True)
    embed.add_field(name='🤖 ``ภาษาที่ใช้เขียนบอท``', value=f'Python {PYTHON_VERSION}',inline =True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    embed.set_thumbnail(url="https://i.imgur.com/rPfYXGs.png")

    message = await ctx.send(embed=embed)
    await message.add_reaction('🤖')

@client.command()
async def serverinfo(ctx):
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

@client.command()
async def userinfo(ctx, member: discord.Member = None):

    roles = [role for role in member.roles]
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

@client.command(aliases=['rules,Rule'])
async def rule(ctx):
    embed=discord.Embed(
        color=0x00FFFF,
        title=f'📑 กฏของเซิฟเวอร์ {ctx.guild.name}',
        description=f'{ctx.author.mention} นี้คือกฎของเซิฟ {ctx.guild.name}',
        )

    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.set_footer(text='┗Powered by REACT')
    embed.add_field(name='``rule 1 :``',value='```ห้ามเป็นสลิ่ม```' , inline = False)
    embed.add_field(name='``rule 2 :``',value='```เคารพคนที่มีอายุมากกว่า```' , inline = False)
    embed.add_field(name='``rule 3 :``',value='```ห้ามทำการสแปมข้อความ```' , inline = False)
    embed.add_field(name='``rule 4 :``',value='```ไม่ก่อกวนผู้อื่นขณะกำลังเล่นเกม```' , inline=False)
    embed.add_field(name='``rule 5 :``',value='```ห้ามเเบ่งปันhack ต่างๆสําหรับเกม```' , inline=False)
    embed.add_field(name='``rule 6 :``',value='```เเบ่งกันใช้ bot```' , inline=False)
    embed.add_field(name='``rule 7 :``',value='```อย่าสร้างปัญหาให้กับคนในดิส```' , inline=False)
    embed.add_field(name='``rule 8 :``',value='```หากไม่ทําตามกฏที่ได้กล่าวไว้ยศ admin สามารถเเตะได้ทันที```',inline=False)

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@client.command()
async def ping(ctx):
    latency = requests.get("https://discord.com/").elapsed.total_seconds()
  

    embed = discord.Embed(
        color = 0xffff00,
        title = 'Smilewin bot ping',
        description = f"""
```⌛ Ping : {round(client.latency * 1000)}ms
⌛ Discord Latency : {latency}ms```
        
        """, 

    )

    embed.set_thumbnail(url="https://i.imgur.com/rPfYXGs.png")
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    embed.timestamp = datetime.datetime.utcnow()
    
    message = await ctx.send(embed=embed)
    await message.add_reaction('⌛')
    print(f"{ctx.author} ping bot and the latency is {round(client.latency * 1000)}ms")

@client.command()
async def hastebin(ctx, *, message): 
    r = requests.post("https://hastebin.com/documents", data=message).json()
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

@client.command()
async def pastebin(ctx, *,message):
    data = {
    'api_option': 'paste',
    'api_dev_key':"COIhrBM2YSIba0PWpq4RGdqEH0KUkhHw",
    'api_paste_code':message,
    'api_paste_name':"Smilewinbot",
    'api_paste_expire_date': 'N',
    'api_user_key': None,
    'api_paste_format': 'python'
    }
    r = requests.post("https://pastebin.com/api/api_post.php", data=data)
    r = r.text
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

@client.command()
async def sreddit(ctx, subreddit):
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

@sreddit.error
async def sreddit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` กรุณาระบุsubreddit ที่ต้องการ ``{COMMAND_PREFIX}sreddit (subreddit)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def dota2now(ctx):
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

@client.command()
async def csgonow(ctx):
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

@client.command()
async def pubgnow(ctx):
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

@client.command()
async def rb6now(ctx):
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

@client.command()
async def apexnow(ctx):
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

@client.command()
async def gtanow(ctx):
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
ผู้เล่นออนไลน์ขณะนี้ : {player}
ผู้เล่นออนไลน์สูงสุดใน 24 ชั่วโมง : {player24}
ผู้เล่นออนไลน์สูงสุดตลอดกาล {playerall}``` """
            )

            embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1592866696")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
            message = await ctx.send(embed=embed)
            await message.add_reaction('🎮')

@client.command()
async def botinvite(ctx):

    invitelink = str(f"https://discord.com/api/oauth2/authorize?client_id={CLIENTID}&permissions=8&scope=bot")
    embed = discord.Embed(  
        colour = 0x00FFFF,
        title = f"ลิงค์เชิญบอท SmileWin : ",
        description = f"[คลิกที่นี้]({invitelink})"

    )
    
    message = await ctx.send(embed=embed)
    await message.add_reaction('💖')

@client.command(aliases=['bitcoin'])
async def btc(ctx): 
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
    r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
    if len('```'+r+'```') > 2000:
        embed = discord.Embed(
           colour = 0x983925,
           description = f" ⚠️``{ctx.author}`` ตัวอักษรมากเกินไป ``"
        )
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
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
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` กรุณาระบุลิงค์ที่ต้องการสร้าง ascii art ``{COMMAND_PREFIX}ascii (word)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command(aliases=['coin'])
async def coinflip(ctx):
    responses = ['https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png','https://i.imgur.com/Jeeym59.png','https://i.imgur.com/Pq8ntth.png']
    flip = random.choice(responses)

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

#moderator
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

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

    print(f"{ctx.author} have kicked {member} with reason {reason}")

@kick.error
async def kick_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะเเตะ",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเตะ ``{COMMAND_PREFIX}kick [@user]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

        print(f"{ctx.author} try to ban member but is missing argument")


    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์เเตะ",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเตะ`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

        print(f"{ctx.author} try to kick member but is missing permission")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
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

    print(f"{ctx.author} have ban {member} with reason {reason}")

@ban.error
async def ban_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะเเบน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}ban [@user]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

        print(f"{ctx.author} try to ban member but is missing argument")

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์เเตะ",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเบน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 
        
        print(f"{ctx.author} try to ban member but is missing permission")

@client.command()
@commands.has_permissions(administrator=True)
async def disconnect(ctx, member : discord.Member):
    embed = discord.Embed(
        colour = 0x983925,
        title = f'สมาชิก {member} ได้ถูกดีดออกจาก voice chat โดย {ctx.author}'
    )

    message = await ctx.send(embed=embed)
    await message.add_reaction('😤')
    await member.move_to(channel=None)

@disconnect.error
async def disconnect_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ชื่อสมาชิกที่จะdisconnect",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของสมาชิกที่จะเเบน ``{COMMAND_PREFIX}disconnect [@user]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
 
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

        print(f"{ctx.author} try to disconnect member but is missing argument")

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ย้ายสมาชิก",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 
        
        print(f"{ctx.author} try to disconnect member but is missing permission")

@client.command(name="dmall")
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message):
    fail = 0
    sent = 0 

    embed = discord.Embed(
        color = 0x00FFFF,
        title = f"ส่งข้อความหาทุกคนในดิสคอร์ด {ctx.guild.name}",
        description = (f"""
        กําลังส่งข้อความ : 
        ```{message}```

        ไปยังสมาชิกทั้งหมด ``{ctx.guild.member_count}`` คน""")
    )
    ctx.send(embed=embed)
    
    for member in ctx.guild.members:
        try:
            await member.create_dm()
            time.sleep(1.01)
            await member.dm_channel.send(message)
            print(f"Message from {ctx.author} has been sent to "+ member.name)
            sent = sent + 1
        except:
            print(f"Message from {ctx.author} failed to sent to "+ member.name)
            fail = fail + 1
        
    print(f"Message has been sent to {sent} users and failed to sent to {fail} users")

@dmall.error
async def dmall_error(ctx ,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}dmall [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

        print(f"{ctx.author} try to dmall member but is missing argument")

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์เเอดมิน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

        print(f"{ctx.author} try to dmall member but is missing permission")

@client.command()
async def covid19th(ctx):
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


    embed = discord.Embed(
		title="💊 ข้อมูล COVID-19",
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

@client.command()
async def help(ctx):
    embed=discord.Embed(
        title='คำสั่งสำหรับใช้งานบอท',
        description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
        color=0x00FFFF   
        )

    embed.add_field(name=f'``{COMMAND_PREFIX}helpbot``',value='คําสั่งเกี่ยวกับตัวบอท' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpfun``',value='คําสั่งบรรเทิง' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpgeneral``',value='คําสั่งทั่วไป' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpgame``',value='คําสั่งเกี่ยวกับเกม' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpadmin``',value='คําสั่งของเเอดมิน' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpsetup``',value='คําสั่งเกี่ยวกับตั้งค่า' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpinfo``',value='คําสั่งเกี่ยวกับข้อมูล' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpimage``',value='คําสั่งเกี่ยวกับรูป' , inline = False)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpnsfw``',value='คําสั่ง 18 + ' , inline = False)
    embed.set_thumbnail(url='https://i.imgur.com/rPfYXGs.png')
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpbot(ctx):
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
    embed.add_field(name=f'``{COMMAND_PREFIX}botcode``', value = 'ดูโค้ดที่ผมใช้ในการเขียนบอทตัวนี้',inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpsetup(ctx):
    embed=discord.Embed(
        title='คําสั่งเกี่ยวกับตั้งค่า',
        description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
        color=0x00FFFF   
        )
    embed.add_field(name=f'``{COMMAND_PREFIX}welcomeset #text-channel``', value='ตั้งค่าห้องเเจ้งเตือนคนเข้าเซิฟเวอร์', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}leaveset #text-channel``', value ='ตั้งค่าห้องเเจ้งเตือนคนออกจากเซิฟเวอร์', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}setwebhook #text-channel``', value =f'ตั้งค่าห้องที่จะใช้คําสั่ง {COMMAND_PREFIX}anon (message) เพื่อคุยกับคนเเปลกหน้าโดยทมี่ไม่เปิดเผยตัวตนกับเซิฟเวอร์ที่เปิดใช้คําสั่งนี้', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}setintroduce #text-channel``', value =f'ตั้งค่าห้องที่จะให้ส่งข้อมูลของสมาชิกหลังจากเเนะนําตัวเสร็จ *พิม {COMMAND_PREFIX}ind เพื่อเเนะนําตัว', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}setrole give/remove @role``', value =f'ตั้งค่าที่จะ ให้/ลบหลังจากเเนะนําตัว', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}setboarder``', value ='ตั้งกรอบที่ใส่ข้อมูลของสมาชิกจากปกติเป็น ``☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆``', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}chat on/off``', value ='เปิด / ปิดใช้งานห้องคุยกับคนเเปลกหน้า', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}introduce on/off``', value ='เปิด / ปิดการใช้งานคําสั่งเเนะนําตัว', inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpgame(ctx):
    embed=discord.Embed(
        title='คําสั่งเกี่ยวกับเกม',
        description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
        color=0x00FFFF   
        )
    embed.add_field(name=f'``{COMMAND_PREFIX}coinflip``', value='ทอยเหรียญ', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}rps``', value = 'เป่ายิ้งฉับเเข่งกับบอท',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}roll ``', value='ทอยลูกเต๋า', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}8ball (question) ``', value='ดูว่าควรจะทําสิงๆนั้นไหม', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}csgonow``', value = 'จํานวนคนที่เล่น CSGO ขณะนี้',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}apexnow``', value = 'จํานวนคนที่เล่น APEX ขณะนี้',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}rb6now``', value = 'จํานวนคนที่เล่น RB6 ขณะนี้',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}pubgnow``', value = 'จํานวนคนที่เล่น PUBG ขณะนี้',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}gtanow``', value = 'จํานวนคนที่เล่น GTA V ขณะนี้',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}apexstat (user)``', value = 'ดูข้อมูลเกม apex ของคนๆนั้น',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}rb6rank (user)``', value = 'ดูเเรงค์เเละmmrของคนๆนั้น',inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpinfo(ctx):
    embed=discord.Embed(
        title='คําสั่งเกี่ยวกับข้อมูล',
        description=f'{ctx.author.mention},เครื่องหมายหน้าคำสั่งคือ ``{COMMAND_PREFIX}``',
        color=0x00FFFF   
        )
    embed.add_field(name=f'``{COMMAND_PREFIX}ind``', value='เเนะนําตัว', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}serverinfo``', value='ข้อมูลเกี่ยวกับเซิฟเวอร์', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}membercount``', value='จํานวนสมาชิกในเซิฟเวอร์', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}userinfo @member``', value ='ข้อมูลเกี่ยวกับสมาชิก', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}covid19th``', value = 'ข้อมูลเกี่ยวกับcovid19 ในไทย',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}covid19``', value = 'ข้อมูลเกี่ยวกับcovid19ทั่วโลก',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}geoip (ip)``', value = 'ข้อมูลเกี่ยว IP นั้น',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}weather (city)``', value = 'ดูสภาพอากาศของจังหวัด',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}country (country)``', value = 'ดูข้อมูลของประเทศทั่วโลก',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}btc``',value='ข้อมูลเกี่ยวกับราคา Bitcoin',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}eth``',value='ข้อมูลเกี่ยวกับราคา Ethereum ',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}github (username)``',value='ดูข้อมูลในของคนใน Github',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}rule``',value='กฎของเซิฟ smilewin',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}avatar @member``',value='ดูรูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}searchavatar @member``',value='search หารูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}guildicon``',value='ดูรูปโปรไฟล์ของเซิฟเวอร์',inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpadmin(ctx):
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
    embed.add_field(name=f'``{COMMAND_PREFIX}changenick @member newnick``', value = 'เปลี่ยนชื่อของสมาชิก',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}clear (จํานวน) ``', value = 'เคลียข้อความตามจํานวน',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}dmall (ข้อความ)``', value = 'ส่งข้อความให้ทุกคนในเซิฟผ่านบอท',inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}dm @member``' ,value = 'ส่งข้อความหาสมาชิกโดยผ่านบอท', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}disconnect @member``' ,value = 'disconnect สมาชิกที่อยู่ในห้องพูด', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}movetome @member``' ,value = 'ย้ายสมาชิกมาห้องของเรา', inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpfun(ctx):
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
    embed.add_field(name=f'``{COMMAND_PREFIX}captcha (text)``', value='ทํา captcha จากคําที่ใส่', inline = True)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpgeneral(ctx):
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
    embed.add_field(name=f'``{COMMAND_PREFIX}calculator a (symbol) b``', value= 'คํานวน + - * / ^ ', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}embed (message)``', value= 'สร้าง embed (ใส่//เพื่อเริ่มบรรทัดต่อไป)', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}length (text)``', value= 'นับจำนวนตัวอักษร', inline = True)
    embed.add_field(name=f'``{COMMAND_PREFIX}reverse (message)``', value= 'กลับหลังประโยค', inline = True)

    embed.set_footer(text=f"┗Requested by {ctx.author}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')

@client.command()
async def helpimage(ctx):
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

@client.command()
async def covid19(ctx):
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

@client.command()
async def lmgtfy(ctx, *, message): 
    r = urlencode({"q": message})
    url = (f'<https://lmgtfy.com/?{r}>')
    embed= discord.Embed(
        colour =0x00FFFF,
        title= f"ลิงค์ lmgtfy ของคุณ {ctx.author}",
        description = f"{url}"
    )

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    
@lmgtfy.error
async def lmgtfy_error(ctx, error):
    embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะค้นหาใน lmgtfy ``{COMMAND_PREFIX}lmgtfy [message]``"
        )
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed ) 
    await message.add_reaction('⚠️')

    
@client.command()
async def tweet(ctx, username: str, *, message: str): 
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
    
@client.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, message):

    embed = discord.Embed(
        color = 0x00FFFF,
        title = f"ส่งข้อความหาคนในดิสคอร์ด {ctx.guild.name}",
        description = (f"""
        กําลังส่งข้อความหา {member} : 
        ```{message}```""")

    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    msg = await ctx.send(embed=embed)
    time.sleep(2)
    
    try:
        await member.create_dm()
        await member.dm_channel.send(message)
        print(f"Message from {ctx.author} has been sent to "+ member.name)

        embed = discord.Embed(
            colour = 0x00FFFF,
            title = f'ข้อความได้ส่งไปถึง {member}',
            description =f'ข้อความ ```{message}```'

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await msg.edit(embed=embed)
  
    except:
        print(f"Message from {ctx.author} failed to sent to "+ member.name)

        embed = discord.Embed(
            colour = 0x983925,
            title = f'ไม่สามารถส่งข้อความถึง {member} ได้'

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await msg.edit(embed=embed)

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}dm [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

        print(f"{ctx.author} try to dm member but is missing argument")

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณไม่มีสิทธิ์เเอดมิน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )
        
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️') 

        print(f"{ctx.author} try to dm member but is missing permission")

@client.command()
async def rps(ctx):
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

@client.command()
@commands.has_permissions(administrator=True)

async def movetome(ctx, member : discord.Member):
    await member.move_to(channel=ctx.author.voice.channel)

    embed = discord.Embed(
        colour = 0x00FFFF,
        title = f"{member}ได้ถูกย้ายไปที่ห้องของ {ctx.author}"

    )
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@client.command()
async def guildicon(ctx): 
    embed = discord.Embed(
        colour = 0x00FFFF,
        title=f"เซิฟเวอร์: {ctx.guild.name}")
    embed.set_image(url=ctx.guild.icon_url)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.reaction("✅")

@client.command()
async def avatar(ctx , member : discord.Member=None): 

    if member is None:
        member = ctx.author

    embed = discord.Embed(
        colour = 0x00FFFF,
        title=f"รูปของสมาชิก: {member}",
        description = f"ลิงค์ : [คลิกที่นี้]({member.avatar_url})")
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

@client.command()
async def searchavatar(ctx, member: discord.Member=None): 
    if member is None:
        member = ctx.author

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
    
@client.command()
async def qr(ctx , data):
    url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={data}"
    embed = discord.Embed(
        colour = 0x00FFFF,
        title = "💻 QR CODE GENERATOR",
        description = f"ลิงค์ : [คลิกที่นี้](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={data})"
    )
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def meme(ctx): 
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
    ip = str(ip)
    r = requests.get(f'http://extreme-ip-lookup.com/json/{ip}')
    r = r.json()
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

@geoip.error
async def geoip_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` กรุณาระบุ IP ที่ต้องการที่จะค้นหา ``{COMMAND_PREFIX}geoip [IP]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
        

@qr.error
async def qr_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งที่จะเขียนใน QR code ``{COMMAND_PREFIX}qr [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')


@tweet.error
async def tweet(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` กรุณาระบุสิ่งชื่อเเละสิ่งที่จะเขียนในโพส twitter ``{COMMAND_PREFIX}tweet [username] [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
@movetome.error
async def movetome_error(ctx, error):
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


@client.command()
async def wasted(ctx, member: discord.Member=None): 
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

@client.command()
async def gay(ctx, member: discord.Member=None): 
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

@client.command()
async def trigger(ctx, member: discord.Member=None): 
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

@client.command()
async def timer(ctx, second : int):

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

@timer.error
async def timer_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับถอยหลัง ``{COMMAND_PREFIX}timer (second)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def count(ctx, second : int):

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

@upper.error
async def upper_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมใหญ่ ``{COMMAND_PREFIX}upper (message)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def lower(ctx, *, message): 
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

@lower.error
async def lower_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะทําเป็นพิมเล็ก ``{COMMAND_PREFIX}lower (message)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def reverse(ctx, *, message): 

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

@reverse.error
async def reverse_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะกลับด้าน ``{COMMAND_PREFIX}reverse (message)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@count.error
async def count_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมวินาทีที่ต้องการจะนับ ``{COMMAND_PREFIX}count (second)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def apexstat(ctx, username):

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

@apexstat.error
async def apexstat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมใส่ชื่อของผู้เล่น ``{COMMAND_PREFIX}apexstat (username)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def captcha(ctx, *, text):
    image = ImageCaptcha()
    data = image.generate(text)
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
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมคําที่จะทําเป็น captcha ``{COMMAND_PREFIX}captcha (word)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
 
@client.command()
async def anal(ctx): 
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
async def botcode(ctx):
    embed = discord.Embed(
        colour = 0x00FFFF,
        title = "โค้ดของบอท SmileWin",
        description = f"[คลิกที่นี้](https://github.com/reactxsw/Smilewinbot)"

    )
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    message = await ctx.send(embed=embed)
    await message.add_reaction('❤️')

@client.command()
async def weather(ctx, *, city):
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

@weather.error
async def weather_error(ctx, error):
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
    r = requests.get("https://some-random-api.ml/img/birb")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพนก"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🐦')

@client.command()
async def panda(ctx):
    r = requests.get("https://some-random-api.ml/img/panda")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพเเพนด้า"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🐼')

@client.command()
async def cat(ctx):
    r = requests.get("https://some-random-api.ml/img/cat")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพเเมว"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🐱')

@client.command()
async def dog(ctx):
    r = requests.get("https://some-random-api.ml/img/dog")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพหมา"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🐶')

@client.command()
async def fox(ctx):
    r = requests.get("https://some-random-api.ml/img/fox")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพสุนัขจิ้งจอก"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🦊')

@client.command()
async def koala(ctx):
    r = requests.get("https://some-random-api.ml/img/koala")
    r = r.json()
    url = r['link']

    embed = discord.Embed(
        colour = 0x00FFFF,
        title="ภาพหมีโคอาล่า"

    )
    embed.set_image(url=url)
    message = await ctx.send(embed= embed)
    await message.add_reaction('🐨')

@client.command()
async def country(ctx, *, country):
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

@country.error
async def country_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องพิมชื่อประเทศที่จะดู ``{COMMAND_PREFIX}country (country)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def pingweb(ctx, website = None): 

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
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้อง text ที่จะใส่ใน comment``{COMMAND_PREFIX}phcomment (text)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def slim(ctx):
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
                 "แล้วที่หลานทำไม่เรียกว่าคุกคามสถาบันหรือ",
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
                 "เรียกร้องทุกอย่างจากกษัตริย์ขนาดนี้ เอาระบอบสมบูรณาญาสิทธิราชย์เลยไหม ไม่ต้องมีละนักการเมือง ไม่ต้องระบอบประชาธิปไตย"]
    
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
async def calculator(ctx , right:int ,symbol , left:int):

    if "+" in symbol:
        product = (right+left)
        product = humanize.intcomma(product)
        a = str(right)
        b = str(symbol)
        c = str(left)
        equation = (a + b + c)
        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "เครื่องคิดเลข",
            description = f"""```
โจทย์ : {equation}
คําตอบ : {product}
```""")
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)

    elif "*" in symbol:
        product = (right*left)
        product = humanize.intcomma(product)
        a = str(right)
        b = str(symbol)
        c = str(left)
        equation = (a + b + c)
        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "📚เครื่องคิดเลข",
            description = f"""```
โจทย์ : {equation}
คําตอบ : {product}
```""")
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)
    
    elif "/" in symbol:
        product = (right/left)
        product = humanize.intcomma(product)
        a = str(right)
        b = str(symbol)
        c = str(left)
        equation = (a + b + c)
        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "📚เครื่องคิดเลข",
            description = f"""```
โจทย์ : {equation}
คําตอบ : {product}
```""")
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)
    
    elif "-" in symbol:
        product = (right-left)
        product = humanize.intcomma(product)
        a = str(right)
        b = str(symbol)
        c = str(left)
        equation = (a + b + c)
        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "📚เครื่องคิดเลข",
            description = f"""```
โจทย์ : {equation}
คําตอบ : {product}
```""")
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)

    elif "^" in symbol:
        product = (right**left)
        product = humanize.intcomma(product)
        a = str(right)
        b = str(symbol)
        c = str(left)
        equation = (a + b + c)
        embed = discord.Embed(
            colour = 0x00FFFF,
            title = "📚เครื่องคิดเลข",
            description = f"""```
โจทย์ : {equation}
คําตอบ : {product}
```""")
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        await ctx.send(embed=embed)

@calculator.error
async def calculator_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ข้อผิดพลาดในการคํานวน",
            description = f" ⚠️``{ctx.author}`` จะต้องใส่เว้นวรรคหลังจากตัวเลขเเละไม่สามารถคํานวนนอกเหนือจาก + - * / ^ ``{COMMAND_PREFIX}calculator a (symbol) b``"
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def length(ctx, *, text):
    num = len(text)

    embed = discord.Embed(
        colour = 0x00FFFF,
        title = "LENGTH COUNTER",
        description = f"""```
ข้อความ : {text}
ความยาว : {num}```"""

    )

    embed.set_footer(text=f"┗Requested by {ctx.author}")
    await ctx.send(embed=embed)

@length.error
async def length_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะนับตัวอักษร ``{COMMAND_PREFIX}length (text)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def github(ctx, *, user=None):    
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

@client.command()
async def roll(ctx):
    num = ["1","2","3","4 ","5","6","1","2","3","4","5","6","1","2","3","4","5","6"]
    x = random.choice(num)
    url = (f"https://www.calculator.net/img/dice{x}.png")

    embed = discord.Embed(
        colour = 0x00FFFF,
        title = "🎲 ทอยลูกเต่า"
    )
    embed.set_image(url = url)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    message.add_reaction("🎲")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *,question):

    r = requests.get(f"https://8ball.delegator.com/magic/JSON/{question}")
    r = r.json()

    answer = r['magic']['answer']
    ask = r['magic']['question']
    percent = r['magic']['type']

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

@client.command()
async def embed(ctx,*,message):

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
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ประโยคหรือคําที่ต้องการที่จะนับตัวอักษร ``{COMMAND_PREFIX}length (text)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
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

@unban.error
async def unban_error(ctx, error):
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
            title = "คุณจำไม่มีสิทธิ์ปลดเเบน",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def webhook(ctx , webhook ,* , message):
    WEBHOOK_URL = webhook
    WEBHOOK_USERNAME = "Smilewinbot"
    WEBHOOK_AVATAR = "https://i.imgur.com/rPfYXGs.png"
    WEBHOOK_CONTENT = message
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

@client.command()
@commands.has_permissions(administrator=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    try:
        await user.add_roles(role)
        embed = discord.Embed(
            colour = 0x00FFFF,
            description = f"ได้ทําการเพิ่มยศ{role}ให้กับ{user}"
        )

        message = await ctx.send(embed = embed)
        await message.add_reaction('✅')

    except:
        embed = discord.Embed(
            colour = 0x983925,
            description = f"ไม่มียศ{role}"
        )
        message = await ctx.send(embed = embed)
        await message.add_reaction('⚠️')

@giverole.error
async def giverole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ชื่อของคนที่ต้องการจะให้ยศเเละยศที่จะให้ ``{COMMAND_PREFIX}giverole @role``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณจำไม่มีสิทธิ์ให้ยศ",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    try:
        await user.remove_roles(role)
        embed = discord.Embed(
            colour = 0x00FFFF,
            description = f"ได้ทําการเอายศ{role}ออกให้กับ{user}"
        )

        message = await ctx.send(embed = embed)
        await message.add_reaction('✅')

    except:
        embed = discord.Embed(
            colour = 0x983925,
            description = f"{user}ไม่มียศ{role}"
        )
        message = await ctx.send(embed = embed)
        await message.add_reaction('⚠️')

@removerole.error
async def removerole_error(ctx, error):
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
            title = "คุณจำไม่มีสิทธิ์เอายศออก",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def changenick(ctx, user: discord.Member, Change):
    await user.edit(nick=Change)
    embed = discord.Embed(
            colour = 0x00FFFF,
            description = f"ได้ทําการเปลี่ยนชื่อ {user.mention}เป็น {Change}"
        )

    message = await ctx.send(embed = embed)
    await message.add_reaction('✅')

@changenick.error
async def changenick_error(ctx, error):
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
            title = "คุณจำไม่มีสิทธิ์เปลี่ยนชื่อ",
            description = f"⚠️ ``{ctx.author}`` ไม่สามารถใช้งานคำสั่งนี้ได้ คุณจำเป็นต้องมีสิทธิ์ ``เเอดมิน`` ก่อนใช้งานคำสั่งนี้"
        )

        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed) 
        await message.add_reaction('⚠️')

@client.command()
async def anon(ctx, *,message):
    username = "Smilewin"
    space = " "
    avatar = "https://i.imgur.com/rPfYXGs.png"

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

    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT webhook_url FROM webhook WHERE status = ?", ('yes',))

    cursor2 = db.cursor()
    cursor2.execute(f"SELECT status FROM webhook WHERE guild_id = {ctx.guild.id}")

    cursor3 = db.cursor()
    cursor3.execute(f"SELECT webhook_url FROM webhook WHERE guild_id = {ctx.guild.id}")

    result = cursor.fetchall()
    result2 = cursor2.fetchone()
    result2 = result2[0]
    result3 = cursor3.fetchone()
    result3 = result3[0]
    
    if result2 == "yes":
        if result3 is not None:
            for webhook in result:
                webhook = space.join(webhook)
                requests.post(webhook,data=payload)
                time.sleep(0.005)
    
        else:
            embed = discord.Embed(
                colour = 0x983925,
                title = "ไม่พบ webhook ของคุณ",
                description = f"คุณต้องตั้งค่าห้องคุยกับคนเเปลกหน้าก่อน ใช้คําสั่ง {COMMAND_PREFIX}helpsetup เพื่อดูข้อมูลเพิ่มเติม"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            message = await ctx.send(embed = embed)
            await message.add_reaction('⚠️')
    
    else:
        embed = discord.Embed(
            colour = 0x983925,
            title = "คุณได้ปิดคําสั่งนี้ไว้",
            description = f"คุณต้องเปิดคําสั่ง {COMMAND_PREFIX}chat on เพื่อใช้คําสั่งนี้ , พิม {COMMAND_PREFIX}helpsetup เพื่อดูข้อมูลเพิ่มเติม"
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed = embed)
        await message.add_reaction('⚠️')

@anon.error
async def anon_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            description = f" ⚠️``{ctx.author}`` จะต้องใส่ข้อความที่จะส่ง ``{COMMAND_PREFIX}anon (message)``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')

@client.command()
async def enbinary(ctx, *, text): 

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

@client.command()
async def debinary(ctx, *,text): 

    r = requests.get(f"https://some-random-api.ml/binary?decode={text}")
    r = r.json()

    binary = r['text']

    embed = discord.Embed(
        colour=0x00FFFF,
        title= "Encode Binary",
        description = f"""```
Binary : {text}
คําปกติ : {binary}```"""
        )
    
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    message =await ctx.send(embed=embed)
    await message.add_reaction('💻')

@client.command(aliases=['ind'])
async def introduction(ctx):

    db = sqlite3.connect('Smilewin.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT status FROM Introduce WHERE guild_id = {ctx.guild.id}")
    result = cursor.fetchone()
    if result is not None:
        result = result[0]

    if result != "no":
        cursor1 = db.cursor()
        cursor1.execute(f"SELECT boarder FROM Introduce WHERE guild_id = {ctx.guild.id}")
        result1 = cursor1.fetchone()
        
        try:
            board = result1[0]

            if board is None:
                board = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"
            
            if board == "None":
                board = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

            if board == "none":
                board = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

        except:
            board = "☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆ﾟ ゜ﾟ☆"

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
{board}
ชื่อ : {name}
อายุ : {age}
เพศ : {sex}
{board}```""")
            )

        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}") 
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text = ctx.author.id)
        cursor2 = db.cursor()
        cursor2.execute(f"SELECT channel_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
        result2 = cursor2.fetchone()

        cursor3 = db.cursor()
        cursor3.execute(f"SELECT giverole_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
        result3 = cursor3.fetchone()

        cursor4 = db.cursor()
        cursor4.execute(f"SELECT removerole_id FROM Introduce WHERE guild_id = {ctx.guild.id}")
        result4 = cursor4.fetchone()

        try:
            channel = client.get_channel(id=int(result2[0]))
            await message.delete()
            await ctx.send(ctx.author.mention)
            await channel.send(embed=embed)

        except:
            await message.delete()
            await ctx.send(ctx.author.mention)
            await ctx.send(embed=embed)

        if result3 is not None:

            try:
                role = result3[0]
                role = int(role)
                role = ctx.guild.get_role(role)
                await ctx.author.add_roles(role)
            except Exception:
                pass
                
        if result4 is not None:
            try:
                role = result4[0]
                role = int(role)
                role = ctx.guild.get_role(role)
                await ctx.author.remove_roles(role)         
            except Exception:
                pass

    else:
        embed =discord.Embed(
           colour = 0x983925,
           description = f"คําสั่งน้ีได้ถูกปิดใช้งาน ใช้คําสั่ง {COMMAND_PREFIX} เพื่อเปิดใช้งาน"
            )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
        await asyncio.sleep(3) 
        await message.delete()

@client.listen()
async def on_message(message):
    channel = message.channel
    if message.author == client.user:
        return
    if'ด่าบอท' in message.content:
        await channel.send("ใครด่ากูวะลูกพี่กูฟ้องละ")

@client.command()
async def test(ctx):
    await ctx.send("Bot online เเล้ว")

#            /\
#/vvvvvvvvvvvv \--------------------------------------,
#`^^^^^^^^^^^^ /====================================="
#            \/
#REACT#1120 - Thailand
    
#Bot login using token
client.run(TOKEN, bot = True)



