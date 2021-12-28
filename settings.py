import motor.motor_asyncio
import json
import asyncpraw
import os
from pathlib import Path

if not Path("download").exists():
    directory = os.path.dirname(__file__) 
    folder = f"{directory}/download" 

    try:
        os.makedirs(folder)

    except OSError:
        pass

if not Path("data").exists():
    directory = os.path.dirname(__file__) 
    folder = f"{directory}/data" 

    try:
        os.makedirs(folder)
        
    except OSError:
        pass

if not Path("image").exists():
    directory = os.path.dirname(__file__) 
    folder = f"{directory}/image" 

    try:
        os.makedirs(folder)
        
    except OSError:
        pass

if not Path("logs").exists():
    directory = os.path.dirname(__file__) 
    folder = f"{directory}/logs" 

    try:
        os.makedirs(folder)
        
    except OSError:
        pass

if Path("config.json").exists():
    with open('config.json') as setting:
        config = json.load(setting)
    
    developerid = config.get("developer_user_id")
    TOKEN = config.get("bot_token")
    COMMAND_PREFIX = config.get("bot_prefix")
    phonenumber = config.get("phone_number")
    openweathermapAPI = config.get("openweathermap_api")
    faceitapi = config.get("faceit_serverside_api")
    reddit = asyncpraw.Reddit(
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
    logchannel = config.get("log_channel")
    partner_id = config.get("emoji_:partner:_id")
    verify_id = config.get("emoji_:verify:_id")
    boost_id = config.get("emoji_:boost:_id")
    member_id = config.get("emoji_:member:_id")
    channel_id = config.get("emoji_:channel:_id")
    role_id = config.get("emoji_:role:_id")
    emoji_id = config.get("emoji_:emoji:_id")
    online_id = config.get("emoji_:online:_id")
    offline_id = config.get("emoji_:offline:_id")
    idle_id = config.get("emoji_:idle:_id")
    busy_id = config.get("emoji_:busy:_id")
    faceitlogo = config.get("emoji_:faceitlogo:_id")
    faceitlvl1 = config.get("emoji_:faceitlvl1:_id")
    faceitlvl2 = config.get("emoji_:faceitlvl2:_id")
    faceitlvl3 = config.get("emoji_:faceitlvl3:_id")
    faceitlvl4 = config.get("emoji_:faceitlvl4:_id")
    faceitlvl5 = config.get("emoji_:faceitlvl5:_id")
    faceitlvl6 = config.get("emoji_:faceitlvl6:_id")
    faceitlvl7 = config.get("emoji_:faceitlvl7:_id")
    faceitlvl8 = config.get("emoji_:faceitlvl8:_id")
    faceitlvl9 = config.get("emoji_:faceitlvl9:_id")
    faceitlvl10 = config.get("emoji_:faceitlvl10:_id")
    faceitsea = config.get("emoji_:faceitsea:_id")
    faceiteu = config.get("emoji_:faceiteu:_id")
    faceitas = config.get("emoji_:faceitas:_id")
    faceitus = config.get("emoji_:faceitus:_id")

else: 
    with open("config.json", "w") as setting:
        setting.writelines(
            [
                "{",
                    "\n",
                    "    "+'"developer_user_id": "_____________________________________",',
                    "\n",
                    "    "+'"bot_token": "_____________________________________",',
                    "\n",
                    "    "+'"bot_prefix": "_____________________________________",',
                    "\n",
                    "    "+'"connect_mongodb": "_____________________________________",',
                    "\n",
                    "    "+'"support_channel": "_____________________________________",',
                    "\n",
                    "    "+'"log_channel": "_____________________________________",',
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
                    "    "+'"pastebin_api_dev_key": "_____________________________________",',
                    "\n",
                    "    "+'"youtube_api": "_____________________________________",',
                    "\n",
                    "\n",
                    "    "+'"emoji_:partner:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:verify:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:boost:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:member:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:channel:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:role:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:emoji:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:online:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:offline:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:idle:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:busy:_id": "_____________________________________"',
                    "\n",
                    "    "+'"emoji_:faceitlogo:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl1:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl2:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl3:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl4:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl5:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl6:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl7:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl8:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl9:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitlvl10:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitsea:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitus:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceitas:_id": "_____________________________________",',
                    "\n",
                    "    "+'"emoji_:faceiteu:_id": "_____________________________________",',
                    "\n",
                "}"
            ]
        )

client = motor.motor_asyncio.AsyncIOMotorClient(mongodb)
db = client['Smilewin']
collection = db["Data"]
collectionlevel = db["Level"]
collectionmoney = db["Money"]
collectionlanguage = db["Language"]
collectionrole = db["Role"]
collectionstatus = db["Status"]
collectioninvitecode = db["Invites"]
# collectioninvitestat = db[""]
