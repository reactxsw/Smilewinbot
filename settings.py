import requests
import motor.motor_asyncio
import json
import asyncpraw
import os
from pathlib import Path

directory = os.path.dirname(__file__)
folders = ["download", "data", "image", "logs"]
for folder in folders:
    try:
        if not Path(folder).exists():
            os.makedirs(f"{directory}/{folder}")

    except OSError:
        print(f"unable to create {folder}")

if Path("config.json").exists():
    with open("config.json") as setting:
        config = json.load(setting)

    developers = config.get("developers")
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
        user_agent=config.get("reddit_user_agent"),
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
    gear = config.get("emoji_:gear:_id")
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
    lavalinkip = config.get("Lavalink_IPv4")
    lavalinkport = config.get("Lavalink_Port")
    lavalinkpass = config.get("Lavalink_pass")
    lavalinkindentifier = config.get("Lavalink_identifier")
    lavalinkregion = config.get("Lavalink_region")
    lavalinkspotifyid = config.get("Lavalink_spotify_clientid")
    lavalinkspotifysecret = config.get("Lavalink_spotify_secret")
    with open("data/phishing.txt", "r", encoding="utf-8") as f:
        phishing = f.read().split("\n")

else:
    with open("config.json", "w") as setting:
        setting.write(
            requests.get(
                "https://raw.githubusercontent.com/reactxsw/Smilewinbot/main/config.example.json"
            ).text
        )

client = motor.motor_asyncio.AsyncIOMotorClient(mongodb)
db = client.Smilewin
collection = db.Data
collectionlevel = db.Level
collectionmoney = db.Money
collectionlanguage = db.Language
collectionrole = db.Role
collectionstatus = db.Status
collectionmusic = db.Music
collectiongamble = db.Gamble
collectiontictactoe = db.TicTacToe
collectiontictactoe_user = db.TicTacToe_user
collectionyoutube = db.Youtube
collectionblackjack = db.Blackjack