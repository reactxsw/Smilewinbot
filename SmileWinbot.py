#import
import discord , asyncio , datetime , itertools , os , praw , requests , random , urllib , aiohttp , bs4 ,json ,humanize , time , platform
#from
from discord.ext import commands, tasks
from discord.utils import get
from datetime import date, timedelta
from itertools import cycle
from bs4 import BeautifulSoup,element
from bs4 import BeautifulSoup as bs4

#INFORMATION THAT CAN TO BE CHANGE
TOKEN = '___________________________'
COMMAND_PREFIX = "/r "

developer = "REACT#1120"
WELCOME_ID = ___________________________
LEAVE_ID = ___________________________
PERSONAL_GUILD_ID = ___________________________
CLIENTID = ___________________________
PYTHON_VERSION = platform.python_version()
OS = platform.system()

reddit = praw.Reddit(client_id="___________________________",
                     client_secret="___________________________8",
                     username="___________________________",
                     password="___________________________",
                     user_agent="___________________________")

status = cycle([' REACT' , ' R ' , ' RE ', ' REA ', ' REAC ', ' REACT ' , ' REACT ! '])

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
client = commands.Bot(command_prefix = COMMAND_PREFIX, intents=intents)
start_time = datetime.datetime.utcnow()
client.remove_command('help')

print(ASCII_ART)
print("BOT STATUS : OFFLINE")

@client.event
async def on_ready():
    change_status.start()
    clearcmd()
    print(ASCII_ART)
    print(f"BOT NAME : {client.user}")
    print("BOT STATUS : ONLINE")
    print("SERVER : " + str(len(client.guilds)))
    print("")
    print("CONSOLE : ")
    print("")

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

    channel = client.get_channel(WELCOME_ID)

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
    if member.guild.id == PERSONAL_GUILD_ID:
        await channel.send(embed=embed)
    
@client.event
async def on_member_remove(member):

    channel = client.get_channel(LEAVE_ID)

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
    if member.guild.id == PERSONAL_GUILD_ID:
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

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/394451338140057610/4061ac5c08f6fa045dca6b3d2ba5cb63.webp?size=1024")
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
        title='Smilewin bot',
        description = "ข้อมูลของบอ"
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
    embed.add_field(name='``rule 1 :``',value='```ห้ามเป็นสลิ่ม```' , inline=False)
    embed.add_field(name='``rule 2 :``',value='```เคารพคนที่มีอายุมากกว่า```' , inline=False)
    embed.add_field(name='``rule 3 :``',value='```ห้ามทำการสแปมข้อความ```' , inline=False)
    embed.add_field(name='``rule 4 :``',value='```ไม่ก่อกวนผู้อื่นขณะกำลังเล่นเกม```' , inline=False)
    embed.add_field(name='``rule 5 :``',value='```ห้ามเเบ่งปันhack ต่างๆสําหรับเกม```' , inline=False)
    embed.add_field(name='``rule 6 :``',value='```เเบ่งกันใช้ bot```' , inline=False)
    embed.add_field(name='``rule 7 :``',value='```อย่าสร้างปัญหาให้กับคนในดิส```' , inline=False)
    embed.add_field(name='``rule 8 :``',value='```หากไม่ทําตามกฏที่ได้กล่าวไว้ยศ admin สามารถเเตะได้ทันที```',inline=False)

    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')



@client.command()
async def ping(ctx):

    embed = discord.Embed(
        color = 0xffff00,
        title = 'Smilewin bot ping',
        description = f'``⌛ Ping`` : ``{round(client.latency * 1000)}ms``', 
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/394451338140057610/4061ac5c08f6fa045dca6b3d2ba5cb63.webp?size=1024")
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
async def sreddit(ctx, subreddit):
    subreddit=reddit.subreddit(subreddit)
    all_subs = []
    top = subreddit.top(limit = 100)
    for submission in top:
        all_subs.append(submission) 
    random_sub = random.choice(all_subs)
    name=random_sub.title
    url = random_sub.url
    embed = discord.Embed(
        colour = 0x00FFFF,
        title = name,
        description = f"ที่มาของรูปคือ subreddit r/{subreddit}"
        )

    embed.set_image(url=url)
    embed.set_footer(text=f"┗Requested by {ctx.author}")
    embed.timestamp = datetime.datetime.utcnow()

    message= await ctx.send(embed=embed)
    await message.add_reaction('✨')

@client.command()
async def dota2now(ctx):
    url = "https://steamcharts.com/app/570"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soupObject = BeautifulSoup(await response.text(), "html.parser")
            div = soupObject.find_all('div', class_='app-stat')[0]
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น dota2 ในตอนนี้",
                description = f"Online player : ``{player}`` "
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
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น CS:GO",
                description = 
                f"จํานวนคนที่เล่น CS:GO ในตอนนี้ : ``{player}``"

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
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น PUBG ในตอนนี้",
                description = f"Online player : ``{player}`` "
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
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น RB6 ในตอนนี้",
                description = f"Online player : ``{player}`` "
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
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น APEX LEGEND ในตอนนี้",
                description = f"Online player : ``{player}`` "
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
            online = div.contents[1].string
            player = humanize.intcomma(online)
            embed = discord.Embed(
                color=0x75ff9f,
                title = "จํานวนคนที่เล่น GTAV ในตอนนี้",
                description = f"Online player : ``{player}`` "
            )

            embed.set_image(url="https://steamcdn-a.akamaihd.net/steam/apps/271590/header.jpg?t=1592866696")
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            embed.timestamp = datetime.datetime.utcnow()
            message = await ctx.send(embed=embed)
            await message.add_reaction('🎮')

@client.command()
async def botinvite(ctx):

    await ctx.send(f"https://discord.com/api/oauth2/authorize?client_id={CLIENTID}&permissions=8&scope=bot")


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
        return
    await ctx.send(f"```{r}```")

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
async def dmall(ctx, message):
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
            await member.dm_channel.send(message)
            print(f"Message from {ctx.author} has been sent to "+ member.name)
            sent = sent + 1
        except:
            print(f"Message from {ctx.author} failed to sent to "+ member.name)
            fail = fail + 1
        
    print(f"Message has been sent to {sent} users and failed to sent to {fail} users")

@dmall.error
async def dmall_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุสิ่งที่จะส่ง",
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
async def covid19(ctx):
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

    embed.add_field(name=f'``{COMMAND_PREFIX}helpbot``',value='คําสั่งเกี่ยวกับตัวบอท' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpfun``',value='คําสั่งบรรเทิง' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpgeneral``',value='คําสั่งทั่วไป' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpgame``',value='คําสั่งเกี่ยวกับเกม' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpadmin``',value='คําสั่งของเเอดมิน' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpinfo``',value='คําสั่งเกี่ยวกับข้อมูล' , inline=True)
    embed.add_field(name=f'``{COMMAND_PREFIX}helpnsfw``',value='คําสั่ง 18 + ' , inline=True)
    embed.set_image(url='https://cdn.discordapp.com/icons/394451338140057610/4061ac5c08f6fa045dca6b3d2ba5cb63.webp?size=1024')
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
    embed.add_field(name=f'``{COMMAND_PREFIX}ping``', value='ส่ง ping ของบอท', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}uptime``', value ='ส่ง เวลาทำงานของบอท', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}botinvite``', value = 'ส่งลิงค์เชิญบอท',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}credit``',value='เครดิตคนทําบอท',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}botinfo``', value = 'ข้อมูลเกี่ยวกับตัวบอท',inline=False)
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
    embed.add_field(name=f'``{COMMAND_PREFIX}coinflip``', value='ทอยเหรียญ', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}rps``', value = 'เป่ายิ้งฉับเเข่งกับบอท',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}csgonow``', value = 'จํานวนคนที่เล่น CSGO ขณะนี้',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}apexnow``', value = 'จํานวนคนที่เล่น APEX ขณะนี้',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}rb6now``', value = 'จํานวนคนที่เล่น RB6 ขณะนี้',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}pubgnow``', value = 'จํานวนคนที่เล่น PUBG ขณะนี้',inline=False )
    embed.add_field(name=f'``{COMMAND_PREFIX}gtanow``', value = 'จํานวนคนที่เล่น GTA V ขณะนี้',inline=False )
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
    embed.add_field(name=f'``{COMMAND_PREFIX}serverinfo``', value='ข้อมูลเกี่ยวกับเซิฟเวอร์', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}membercount``', value='จํานวนสมาชิกในเซิฟเวอร์', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}userinfo @member``', value ='ข้อมูลเกี่ยวกับสมาชิก', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}covid19``', value = 'ข้อมูลเกี่ยวกับcovid19 ในไทย',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}btc``',value='ข้อมูลเกี่ยวกับราคา Bitcoin',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}eth``',value='ข้อมูลเกี่ยวกับราคา Ethereum ',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}rule``',value='กฎของเซิฟ smilewin',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}avatar @member``',value='ดูรูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}searchavatar @member``',value='search หารูปโปรไฟล์ของสมาชิก และ ตัวเอง',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}guildicon``',value='ดูรูปโปรไฟล์ของเซิฟเวอร์',inline=False)
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
    embed.add_field(name=f'``{COMMAND_PREFIX}kick @member``', value='เเตะสมาชิก', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}ban @member``', value ='เเบนสมาชิก', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}clear (จํานวน) ``', value = 'เคลียข้อความตามจํานวน',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}dmall (ข้อความ)``', value = 'ส่งข้อความให้ทุกคนในเซิฟผ่านบอท',inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}dm @member``' ,value = 'ส่งข้อความหาสมาชิกโดยผ่านบอท', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}disconnect @member``' ,value = 'disconnect สมาชิกที่อยู่ในห้องพูด', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}movetome @member``' ,value = 'ย้ายสมาชิกมาห้องของเรา', inline=False)
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
    embed.add_field(name=f'``{COMMAND_PREFIX}sreddit (subreddit)``', value='ส่งรูปจาก subreddit', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}qr (message)``', value='สร้าง qr code', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}meme``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}tweet (username) (message)``', value='สร้างรูปจาก twitter โดยใช้ชื่อ twitterคนอื่น', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}wasted @member``', value='ใส่filter "wasted" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}gay @member``', value='ใส่filterสีรุ้งให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline=False)
    embed.add_field(name=f'``{COMMAND_PREFIX}trigger @member``', value='ใส่filter "triggered" ให้กับรูปโปรไฟล์ของสมาชิก และ ตัวเอง', inline=False)
    embed.set_footer(text=f"┗Requested by {ctx.author}")

    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')


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
async def dm(ctx, member: discord.Member, message):

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
            title = "ระบุสิ่งที่จะส่ง",
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
                description = "😄 คุณชนะ"
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
                description = "😭 คุณเเพ้"
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
        description = f"ลิงค์ : [คลิกที่นี้](https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={data}link)"
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



@qr.error
async def qr(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุสิ่งที่จะเขียนใน QR code",
            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}qr [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')


@tweet.error
async def tweet(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุสิ่งชื่อเเละสิ่งที่จะเขียนในโพส twitter",
            description = f" ⚠️``{ctx.author}`` จะต้องพิมสิ่งที่จะส่ง ``{COMMAND_PREFIX}tweet [username] [message]``"
        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")

        message = await ctx.send(embed=embed ) 
        await message.add_reaction('⚠️')
    
@movetome.error
async def movetome(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            colour = 0x983925,
            title = "ระบุสิ่งชื่อของสมาชิกที่ต้องการจะย้ายมาหา",
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
    await message.add_reaction('✅')

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
    await message.add_reaction('✅')

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
    await message.add_reaction('✅')

#Bot login using token
client.run(TOKEN, bot = True)
