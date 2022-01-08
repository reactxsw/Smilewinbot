import nextcord
import datetime

from motor.metaprogramming import asynchronize
import settings
from nextcord.ext import commands
import wavelink
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
class Music(commands.Cog, wavelink.WavelinkMixin):

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        if self.bot.wavelink.nodes:
            previous = self.bot.wavelink.nodes.copy()
            for node in previous.values():
                await node.destroy()
        
        nodes = {
            "Node_1": {
                "host": settings.lavalinkip,
                "port": settings.lavalinkport,
                "rest_uri": f"http://{settings.lavalinkip}:{settings.lavalinkport}",
                "password": settings.lavalinkpass,
                "identifier": f"{settings.lavalinkindentifier}_1",
                "region": settings.lavalinkregion
            }
        }

        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready")

    async def do_next(self,guild_id,player,mode,tracks=None):
        server = await settings.collectionmusic.find_one({"guild_id":guild_id})
        if mode == "Default":
            await settings.collectionmusic.update_one({"guild_id": guild_id}, {'$pop': {'Queue': -1}})
            if server["Queue"] == []:
                return

            else:
                Song = server["Queue"][0]["song_id"]
                tracks = await self.bot.wavelink.build_track(Song)
                await player.play(tracks)
    
        if mode == "Repeat":
            tracks.play(tracks)
    
    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node: wavelink.Node, payload:wavelink.events.TrackEnd):
        guild_id = payload.player.guild_id
        player = payload.player
        track = payload.track
        server = await settings.collectionmusic.find_one({"guild_id":guild_id})
        if payload.reason == "FINISHED":
            if server["Mode"] != "Loop":
                await self.do_next(guild_id,player,server["Mode"],track)
            
            else:
                server["Queue"].index("")

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

    async def stop_music(self,guild_id):
        player = self.bot.wavelink.get_player(guild_id)
        if player.is_connected:
            await player.disconnect(True)
            await player.destroy()
            await settings.collectionmusic.delete_one({"guild_id":guild_id})

    async def pause_resume_music(self,guild_id):
        player = self.bot.wavelink.get_player(guild_id)
        if player.is_connected:
            if player.is_paused:
                await player.set_pause(False)
            
            else:
                await player.set_pause(True)

        else:
            pass
    
    async def mute_bot(self,guild_id):
        player = self.bot.wavelink.get_player(guild_id)
        if player.volumer == 0:
            player.set_volume(80)
        else:
            player.set_volume(0)

    async def build_embed(title,duration,thumbnail,next,author,requester,mode):
        embed = nextcord.Embed(
            title = "Smilewin Music",
            description = f"Now playing {title}",
            colour = 0xFED000
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(duration))))
        embed.add_field(name='Requested By', value=requester.mention)
        embed.add_field(name='Next', value="-" if next is None else next)
        embed.set_footer(text=f"┗Requested by {requester}")

        return embed

    @commands.command()
    async def stop(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await settings.collectionmusic.delete_one({"guild_id":ctx.guild.id})
        await player.destroy()

    @commands.command()
    async def pause(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_paused:
            await player.set_pause(True)
            await ctx.send("Paused")
        else:
            await ctx.send(f"Not playing use `{settings.COMMAND_PREFIX} resume` to resume")

    @commands.command()
    async def resume(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.is_paused:
            await player.set_pause(False)
            await ctx.send("Resumed")
        else:
            await ctx.send(f"Song has not been paused. Use `{settings.COMMAND_PREFIX} pause` to pause the song")

    @commands.command()
    async def loop(self,ctx):
        server = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
        if not server["Mode"] == "Loop":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'Mode': "Loop"}})
            await ctx.send("Loop mode activated")
        
        elif server["Mode"] == "Loop":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'Mode': "Default"}})
            await ctx.send("Loop mode deactivated")
        
    @commands.command()
    async def repeat(self,ctx):
        server = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
        if not server["Mode"] == "Repeat":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'Mode': "Repeat"}})
            await ctx.send("Repeat mode activated")
        
        elif server["Mode"] == "Repeat":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'Mode': "Default"}})
            await ctx.send("Repeat mode deactivated")

    @commands.command()
    async def volmusic(self, ctx, volume : int):
        default_volume = 100    
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if isinstance(volume, int):
            await player.set_volume(int(volume))
            embed = nextcord.Embed(title=f'Successfully, Set volume into `{volume}`',color=nextcord.Colour.green())
            embed.add_field(name=f'Current volume : {volume}',value=f'Default volume : `100`')
            emoji = '\N{THUMBS UP SIGN}'
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(emoji)
        else:
            await ctx.send("Please input only numbers")

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: nextcord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise nextcord.nextcordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        await player.connect(channel.id)
    
    @commands.command(name='disconnect')
    async def disconnect_(self, ctx, *, channel: nextcord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise nextcord.nextcordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        await player.disconnect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        if ctx.author.voice is not None:
            tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
            player = self.bot.wavelink.get_player(ctx.guild.id)
            if tracks:
                song_id = tracks[0].id
                song_title = tracks[0].title
                song_duration = tracks[0].duration
                song_thumbnail = tracks[0].thumb
                song_author = tracks[0].author

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
                        "Queue":[{
                            "position":1,
                            "song_title":song_title,
                            "song_id":song_id,
                            "requester":ctx.author.id}]
                    }
                    await settings.collectionmusic.insert_one(data)
                    player = self.bot.wavelink.get_player(ctx.guild.id)
                    if not player.is_connected:
                        await ctx.invoke(self.connect_)
                    embed = await Music.build_embed(song_title,song_duration,song_thumbnail,None,song_author,ctx.author,"Default")
                    await message.edit(embed=embed)
                    await player.play(tracks[0])
                
                else:
                    if not len(Queue["Queue"]) > 20:
                        await settings.collectionmusic.update_one({'guild_id': ctx.guild.id}, {'$push': {'Queue': {"position":len(Queue["Queue"])+1,"song_title":song_title,"song_id":song_id,"requester":ctx.author.id}}})
                        if len(Queue["Queue"]) == 1:
                            message = await self.bot.get_channel(Queue["Request_channel"]).fetch_message(Queue["Message_id"]) # the message's channel
                            embed = await Music.build_embed(Queue["Queue"][0]["song_title"],song_duration,song_thumbnail,song_title,song_author,ctx.author,Queue["Mode"])
                            await message.edit(embed=embed)
                    else:
                        await ctx.send("คิวห้ามเกิน 20")
            else:        
                return await ctx.send('Could not find any songs with that query.')
        else:
            await ctx.send('No channel to join. Please either specify a valid channel or join one.')

    
    @commands.command()
    async def musicsetup(self,ctx):
        data = await settings.collection.find_one({"guild_id":ctx.guild.id})
        if data is None:
            newserver = await Music.setnewserver(self,ctx)
            await settings.collection.insert_one(newserver)
            channel = await ctx.guild.create_text_channel(name = '😁│Smilewin Music',topic= ":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง:arrows_counterclockwise: เริ่มเพลงที่กำลังเล่นใหม่:repeat: เปลี่ยนโหมดการวนเล่นเพลง:twisted_rightwards_arrows: สุ่มเพลงในคิว:sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง")

            embed=nextcord.Embed(description="[❯ Invite](https://smilewinnextcord-th.web.app/invitebot.html) | [❯ Website](https://smilewinnextcord-th.web.app) | [❯ Support](https://nextcord.com/invite/R8RYXyB4Cg)",
                                colour = 0xffff00)
            embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar_url)
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
                embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar_url)
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
                    embed.set_author(name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้", icon_url=self.bot.user.avatar_url)
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
