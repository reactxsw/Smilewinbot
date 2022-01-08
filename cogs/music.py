import pomice
import datetime
import asyncio
from contextlib import suppress
from motor.metaprogramming import asynchronize
from pomice.objects import Playlist
import settings
from nextcord.ext import commands
import nextcord
import math
import random
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
class Player(pomice.Player):
    """Custom pomice Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        self.queue = asyncio.Queue()
        self.controller: nextcord.Message = None
        # Set context here so we can send a now playing embed
        self.context: commands.Context = None
        self.dj: nextcord.Member = None
        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def do_next(self) -> None:
        # Clear the votes for a new song
        self.pause_votes.clear()
        self.resume_votes.clear()
        self.skip_votes.clear()
        self.shuffle_votes.clear()
        self.stop_votes.clear()
        

        # Check if theres a controller still active and deletes it
        if self.controller:
            with suppress(nextcord.HTTPException):
                await self.controller.delete()
            
       # Queue up the next track, else teardown the player
        try:
            track: pomice.Track = self.queue.get_nowait()
        except asyncio.queues.QueueEmpty:  
            return await self.teardown()
        
        await self.play(track)

        # Call the controller (a.k.a: The "Now Playing" embed) and check if one exists

        if track.is_stream:
            embed = nextcord.Embed(title="Now playing", description=f":red_circle: **LIVE** [{track.title}]({track.uri}) [{track.requester.mention}]")
            self.controller = await self.context.send(embed=embed)

        else:
            embed = nextcord.Embed(
                title=f"Smilewin Music", 
                description=f"Now playing [{track.title}]({track.uri})",
                colour = 0xFED000)

            embed.set_thumbnail(url=track.thumbnail)
            embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(track.length))))
            embed.add_field(name='Requested By', value=track.requester.mention)
            embed.add_field(name='Next', value="-")
            self.controller = await self.context.send(embed=embed)


    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        with suppress((nextcord.HTTPException), (KeyError)):
            await self.destroy()
            if self.controller:
                await self.controller.delete() 

    async def set_context(self, ctx: commands.Context):
        """Set context for the player"""
        self.context = ctx 
        self.dj = ctx.author 




class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        # In order to initialize a node, or really do anything in this library,
        # you need to make a node pool
        self.pomice = pomice.NodePool()

        # Start the node
        bot.loop.create_task(self.start_nodes())
    
    async def setnewserver(self,ctx):
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
                    "verification_time":10,
                    "verification_channel_id":"None",
                    "verification_role_give_id":"None",
                    "verification_role_remove_id":"None",
                    "log_voice_system":"NO",
                    "log_delete_system":"NO",
                    "log_name_system":"NO",
                    "log_channel_id":"None",
                    "scam":"warn",
                    "Music_channel_id":"None",
                    "Embed_message_id":"None",
                    "Music_message_id":"None"
                    }
        return newserver

    async def start_nodes(self):
        # Waiting for the bot to get ready before connecting to nodes.
        await self.bot.wait_until_ready()
        
        # You can pass in Spotify credentials to enable Spotify querying.
        # If you do not pass in valid Spotify credentials, Spotify querying will not work 
        await self.pomice.create_node(
            bot=self.bot,
            host=settings.lavalinkip,
            port=settings.lavalinkport,
            password=settings.lavalinkpass,
            identifier=settings.lavalinkindentifier,
            region=settings.lavalinkregion
        )
        print(f"Node is ready!")

    async def required(self, ctx: commands.Context):
        """Method which returns required votes based on amount of members in a channel."""
        player: Player = ctx.voice_client
        channel = self.bot.get_channel(int(player.channel.id))
        required = math.ceil((len(channel.members) - 1) / 2.5)

        if ctx.command.name == 'stop':
            if len(channel.members) == 3:
                required = 2

        return required

    async def is_privileged(self, ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        player: Player = ctx.voice_client

        return player.dj == ctx.author or ctx.author.guild_permissions.kick_members

    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: Player, track, _):
        await player.do_next()

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: Player, track, _):
        await player.do_next()

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: Player, track, _):
        await player.do_next()
        
    @commands.command(aliases=['joi', 'j', 'summon', 'su', 'con'])
    async def join(self, ctx: commands.Context, *, channel: nextcord.VoiceChannel = None) -> None:
        if not channel:
            channel = getattr(ctx.author.voice, "channel", None)
            if not channel:
                return await ctx.send("You must be in a voice channel in order to use this command!")

        await ctx.author.voice.channel.connect(cls=Player)
        player: Player = ctx.voice_client
        await player.set_context(ctx=ctx)
        await ctx.send(f"Joined the voice channel `{channel.name}`")

    @commands.command(aliases=['disconnect', 'dc', 'disc', 'lv'])
    async def leave(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        await player.destroy()
        await ctx.send("Player has left the channel.")
        
    @commands.command(aliases=['pla', 'p'])
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        if ctx.author.voice is not None:
            player = self.pomice._nodes[settings.lavalinkindentifier].get_player(ctx.guild.id)
            if player is None:
                await ctx.invoke(self.join)   
                player = ctx.voice_client
            results = await player.get_tracks(search, ctx=ctx)     
            if not results:
                return await ctx.send("No results were found for that search term", delete_after=7)
            
            track = results[0]
            s_title = track.title
            s_id = track.id
            Queue = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id}) 
            if Queue is None and not player.is_playing:
                embed = nextcord.Embed(
                    title = "Searching ..",
                    colour = 0xFED000
                )
                message = await ctx.send(embed=embed)
                data = {
                    "guild_id":ctx.guild.id,
                    "Mode":"Default",
                    "Request_channel":ctx.channel.id,
                    "Message_id":message.id,
                    "Queue":[]
                }
                data["Queue"].append({
                        "position":1,
                        "song_title":s_title,
                        "song_id":s_id,
                        "requester":ctx.author.id})

                await settings.collectionmusic.insert_one(data)

            else:
                if not len(Queue["Queue"]) > 20:
                    await settings.collectionmusic.update_one({
                        'guild_id': ctx.guild.id}, {
                            '$push': {
                                'Queue': {
                                    "position":len(Queue["Queue"])+1,
                                    "song_title":s_title,
                                    "song_id":s_id,
                                    "requester":ctx.author.id}}})

                    if len(Queue["Queue"]) == 1:
                        message = await self.bot.get_channel(Queue["Request_channel"]).fetch_message(Queue["Message_id"]) # the message's channel
                        embed = await Music.build_embed(Queue["Queue"][0]["song_title"],track,Queue["Mode"])
                        await message.edit(embed=embed)

            if isinstance(results, pomice.Playlist):
                Queue = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id}) 
                if Queue is None and not player.is_playing:
                    if len(results.tracks) > 20:
                        results.tracks = results.tracks[:21]

                    embed = nextcord.Embed(
                        title = "Searching ..",
                        colour = 0xFED000
                    )
                    message = await ctx.send(embed=embed)
                    data = {
                        "guild_id":ctx.guild.id,
                        "Mode":"Default",
                        "Request_channel":ctx.channel.id,
                        "Message_id":message.id,
                        "Queue":[]
                    }
                    num = 0
                    for track in results.tracks:
                        data["Queue"].append({
                                "position":num+1,
                                "song_title":track.title,
                                "song_id":track.id,
                                "requester":ctx.author.id})

                    await settings.collectionmusic.insert_one(data)
                
                else:
                    if not len(Queue["Queue"]) > 20:
                        availble = 21 - len(Queue["Queue"])
                        if len(results.tracks) > availble:
                            results.tracks = results.tracks[:availble]
                        num = len(Queue["Queue"]) + 1
                        for track in results.tracks:
                            await settings.collectionmusic.update_one({
                                'guild_id': ctx.guild.id}, {
                                    '$push': {
                                        'Queue': {
                                            "position":num+1,
                                            "song_title":s_title,
                                            "song_id":s_id,
                                            "requester":ctx.author.id
                                            }
                                        }
                                    })
                                                             
            if not player.is_playing:
                await player.do_next()



    @commands.command(aliases=['pau', 'pa'])
    async def pause(self, ctx: commands.Context):
        """Pause the currently playing song."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send('An admin or DJ has paused the player.', delete_after=10)
            player.pause_votes.clear()

            return await player.set_pause(True)

        required = self.required(ctx)
        player.pause_votes.add(ctx.author)

        if len(player.pause_votes) >= required:
            await ctx.send('Vote to pause passed. Pausing player.', delete_after=10)
            player.pause_votes.clear()
            await player.set_pause(True)
        else:
            await ctx.send(f'{ctx.author.mention} has voted to pause the player. Votes: {len(player.pause_votes)}/{required}', delete_after=15)

    @commands.command(aliases=['res', 'r'])
    async def resume(self, ctx: commands.Context):
        """Resume a currently paused player."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if not player.is_paused or not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send('An admin or DJ has resumed the player.', delete_after=10)
            player.resume_votes.clear()

            return await player.set_pause(False)

        required = self.required(ctx)
        player.resume_votes.add(ctx.author)

        if len(player.resume_votes) >= required:
            await ctx.send('Vote to resume passed. Resuming player.', delete_after=10)
            player.resume_votes.clear()
            await player.set_pause(False)
        else:
            await ctx.send(f'{ctx.author.mention} has voted to resume the player. Votes: {len(player.resume_votes)}/{required}', delete_after=15)

    @commands.command(aliases=['n', 'nex', 'next', 'sk'])
    async def skip(self, ctx: commands.Context):
        """Skip the currently playing song."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send('An admin or DJ has skipped the song.', delete_after=10)
            player.skip_votes.clear()

            return await player.stop()

        if ctx.author == player.current.requester:
            await ctx.send('The song requester has skipped the song.', delete_after=10)
            player.skip_votes.clear()

            return await player.stop()

        required = self.required(ctx)
        player.skip_votes.add(ctx.author)

        if len(player.skip_votes) >= required:
            await ctx.send('Vote to skip passed. Skipping song.', delete_after=10)
            player.skip_votes.clear()
            await player.stop()
        else:
            await ctx.send(f'{ctx.author.mention} has voted to skip the song. Votes: {len(player.skip_votes)}/{required} ', delete_after=15)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop the player and clear all internal states."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if not player.is_connected:
            return

        if self.is_privileged(ctx):
            await ctx.send('An admin or DJ has stopped the player.', delete_after=10)
            return await player.teardown()

        required = self.required(ctx)
        player.stop_votes.add(ctx.author)

        if len(player.stop_votes) >= required:
            await ctx.send('Vote to stop passed. Stopping the player.', delete_after=10)
            await player.teardown()
        else:
            await ctx.send(f'{ctx.author.mention} has voted to stop the player. Votes: {len(player.stop_votes)}/{required}', delete_after=15)

    @commands.command(aliases=['mix', 'shuf'])
    async def shuffle(self, ctx: commands.Context):
        """Shuffle the players queue."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if not player.is_connected:
            return

        if player.queue.qsize() < 3:
            return await ctx.send('The queue is empty. Add some songs to shuffle the queue.', delete_after=15)

        if self.is_privileged(ctx):
            await ctx.send('An admin or DJ has shuffled the queue.', delete_after=10)
            player.shuffle_votes.clear()
            return random.shuffle(player.queue._queue)

        required = self.required(ctx)
        player.shuffle_votes.add(ctx.author)

        if len(player.shuffle_votes) >= required:
            await ctx.send('Vote to shuffle passed. Shuffling the queue.', delete_after=10)
            player.shuffle_votes.clear()
            random.shuffle(player.queue._queue)
        else:
            await ctx.send(f'{ctx.author.mention} has voted to shuffle the queue. Votes: {len(player.shuffle_votes)}/{required}', delete_after=15)

    @commands.command(aliases=['v', 'vol'])
    async def volume(self, ctx: commands.Context, *, vol: int):
        """Change the players volume, between 1 and 100."""
        if not (player := ctx.voice_client):
            return await ctx.send("You must have the bot in a channel in order to use this command", delete_after=7)

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send('Only the DJ or admins may change the volume.')

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        await player.set_volume(vol)
        await ctx.send(f'Set the volume to **{vol}**%', delete_after=7)

    
    @commands.command()
    async def musicsetup(self,ctx):
        data = await settings.collection.find_one({"guild_id":ctx.guild.id})
        if data is None:
            newserver = await Music.setnewserver(self,ctx)
            await settings.collection.insert_one(newserver)
            channel = await ctx.guild.create_text_channel(name = '😁│Smilewin Music',topic= ":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง:arrows_counterclockwise: เริ่มเพลงที่กำลังเล่นใหม่:repeat: เปลี่ยนโหมดการวนเล่นเพลง:twisted_rightwards_arrows: สุ่มเพลงในคิว:sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง")

            embed=nextcord.Embed(description="[❯ Invite](https://smilewinnextcord-th.web.app/invitebot.html) | [❯ Website](https://smilewinnextcord-th.web.app) | [❯ Support](https://nextcord.com/invite/R8RYXyB4Cg)",
                                colour = 0xffff00)
            embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar.url)
            embed.set_image(url ="https://i.imgur.com/XwFF4l6.png")
            embed.set_footer(text=f"server : {ctx.guild.name}")
            try:
                embed_message = await channel.send(content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ " ,embed=embed , components=[
                    [

                        Button(label=" ⏯ ",style=ButtonStyle.green,custom_id="pause_stop",disabled = True),
                        Button(label=" ⏭ ",style=ButtonStyle.gray,custom_id="skip",disabled = True),
                        Button(label=" ⏹ ",style=ButtonStyle.red ,custom_id="stop",disabled = True),
                        Button(label=" 🔂 ",style=ButtonStyle.gray ,custom_id="repeat",disabled = True),
                        Button(label=" 🔁 ",style=ButtonStyle.gray ,custom_id="loop",disabled = True),
                        ],

                    [
                        Button(label=" 🔊 เพิ่มเสียง ",style=ButtonStyle.blue ,custom_id="decrease_volume",disabled = True),
                        Button(label=" 🔈 ลดเสียง ",style=ButtonStyle.blue ,custom_id="increase_volume",disabled = True),
                        Button(label=" 🔇 เปิด/ปิดเสียง ",style=ButtonStyle.blue ,custom_id="mute_volume",disabled = True)    
                        ]
                    ])
            except Exception as e:
                print(e)
            music_message = await channel.send("กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง")
            await settings.collection.update_one({"guild_id":ctx.guild.id},{"$set":{"Music_channel_id":channel.id,"Embed_message_id":embed_message.id,"Music_message_id":music_message.id}})

        else:
            if data["Music_channel_id"] == "None":
                channel = await ctx.guild.create_text_channel(name = '😁│Smilewin Music',topic= ":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง:arrows_counterclockwise: เริ่มเพลงที่กำลังเล่นใหม่:repeat: เปลี่ยนโหมดการวนเล่นเพลง:twisted_rightwards_arrows: สุ่มเพลงในคิว:sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง")

                embed=nextcord.Embed(description="[❯ Invite](https://smilewinnextcord-th.web.app/invitebot.html) | [❯ Website](https://smilewinnextcord-th.web.app) | [❯ Support](https://nextcord.com/invite/R8RYXyB4Cg)",
                                    colour = 0xffff00)
                embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar.url)
                embed.set_image(url ="https://i.imgur.com/XwFF4l6.png")
                embed.set_footer(text=f"server : {ctx.guild.name}")
                embed_message = await channel.send(content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ " ,embed=embed, components=[
                [
                    Button(label="⏯",style=ButtonStyle.green,custom_id="pause_stop",disabled = True),
                    Button(label="⏭",style=ButtonStyle.gray,custom_id="skip",disabled = True),
                    Button(label="⏹",style=ButtonStyle.red ,custom_id="stop",disabled = True),
                    Button(label="🔂",style=ButtonStyle.gray ,custom_id="repeat",disabled = True),
                    Button(label="🔁",style=ButtonStyle.gray ,custom_id="loop",disabled = True),
                    ],

                [
                    Button(label="🔊 เพิ่มเสียง",style=ButtonStyle.blue ,custom_id="decrease_volume",disabled = True),
                    Button(label="🔈 ลดเสียง",style=ButtonStyle.blue ,custom_id="increase_volume",disabled = True),
                    Button(label="🔇 เปิด/ปิดเสียง",style=ButtonStyle.blue ,custom_id="mute_volume",disabled = True)    
                    ]
                ])
                music_message = await channel.send("กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง")
                await settings.collection.update_one({"guild_id":ctx.guild.id},{"$set":{"Music_channel_id":channel.id,"Embed_message_id":embed_message.id,"Music_message_id":music_message.id}})

            else:
                if data["Music_channel_id"] not in ctx.guild.text_channels:
                    channel = await ctx.guild.create_text_channel(name = '😁│Smilewin Music',topic= ":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง:arrows_counterclockwise: เริ่มเพลงที่กำลังเล่นใหม่:repeat: เปลี่ยนโหมดการวนเล่นเพลง:twisted_rightwards_arrows: สุ่มเพลงในคิว:sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง")

                    embed=nextcord.Embed(description="[❯ Invite](https://smilewinnextcord-th.web.app/invitebot.html) | [❯ Website](https://smilewinnextcord-th.web.app) | [❯ Support](https://nextcord.com/invite/R8RYXyB4Cg)",
                                        colour = 0xffff00)
                    embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar.url)
                    embed.set_image(url ="https://i.imgur.com/XwFF4l6.png")
                    embed.set_footer(text=f"server : {ctx.guild.name}")
                    embed_message = await channel.send(content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ " ,embed=embed, components=[
                [
                    Button(label="⏯",style=ButtonStyle.green,custom_id="pause_stop",disabled = True),
                    Button(label="⏭",style=ButtonStyle.gray,custom_id="skip",disabled = True),
                    Button(label="⏹",style=ButtonStyle.red ,custom_id="stop",disabled = True),
                    Button(label="🔂",style=ButtonStyle.gray ,custom_id="repeat",disabled = True),
                    Button(label="🔁",style=ButtonStyle.gray ,custom_id="loop",disabled = True),
                    ],

                [
                    Button(label="🔊 เพิ่มเสียง",style=ButtonStyle.blue ,custom_id="decrease_volume",disabled = True),
                    Button(label="🔈 ลดเสียง",style=ButtonStyle.blue ,custom_id="increase_volume",disabled = True),
                    Button(label="🔇 เปิด/ปิดเสียง",style=ButtonStyle.blue ,custom_id="mute_volume",disabled = True)    
                    ]
                ])
                    music_message = await channel.send("กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง")
                    await settings.collection.update_one({"guild_id":ctx.guild.id},{"$set":{"Music_channel_id":channel.id,"Embed_message_id":embed_message.id,"Music_message_id":music_message.id}})

                else:
                    channel = self.bot.get_channel(data["Music_channel_id"])
                    try:
                        embed_message = await channel.fetch_message(data["Embed_message_id"])
                        music_message = await channel.fetch_message(data["Music_message_id"])



                    except nextcord.NotFound:
                        pass

def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
