from discord import colour, embeds
from wavelink.node import Node
import settings
from discord.ext import commands, tasks
from utils.languageembed import languageEmbed
import discord
import wavelink
import settings
import re
import datetime
import asyncio


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
                "rest_uri": f"http://"+f"{settings.lavalinkip}:{settings.lavalinkport}",
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

    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node: wavelink.Node, payload:wavelink.events.TrackEnd):
        guild_id = payload.player.guild_id
        player = payload.player
        if payload.reason == "FINISHED":
            print(payload.player.channel_id)
            await self.do_next(guild_id,player)

    @commands.command(name='connect')
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        await player.connect(channel.id)
    
    @commands.command()
    async def skip(self,ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        data = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
        if data["Queue"] == []:
            await ctx.send("Queue is empty")
        else:
            data["Queue"] = data["Queue"][1:]
            await settings.collectionmusic.update_one({"guild_id": ctx.guild.id}, {'$pop': {'Queue': -1}})
            if data["Queue"] == []:
                await player.stop()
                await self.auto_disconnect(player)
            else:
                await player.stop()
                Song = data["Queue"][0]["song_id"]
                tracks = await self.bot.wavelink.build_track(Song)
                await player.play(tracks)
                await ctx.send("Skipped")

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
        if not server["mode"] == "Loop":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'mode': "Loop"}})
            await ctx.send("Loop mode activated")
        
        elif server["mode"] == "Loop":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'mode': "Default"}})
            await ctx.send("Loop mode deactivated")
    
    @commands.command()
    async def repeat(self,ctx):
        server = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
        if not server["mode"] == "Repeat":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'mode': "Repeat"}})
            await ctx.send("Repeat mode activated")
        
        elif server["mode"] == "Repeat":
            await settings.collectionmusic.update_one({"guild_id":ctx.guild.id}, {'$set': {'mode': "Default"}})
            await ctx.send("Repeat mode deactivated")
    
    async def do_next(self,guild_id,player):
        server = await settings.collectionmusic.find_one({"guild_id":guild_id})
        if server["Mode"] == "Default":
            await settings.collectionmusic.update_one({"guild_id": guild_id}, {'$pop': {'Queue': -1}})
            server["Queue"] = server["Queue"][1:]
            if server["Queue"] == []:
                await self.auto_disconnect(player)

            else:
                Song = server["Queue"][0]["song_id"]
                tracks = await self.bot.wavelink.build_track(Song)
                await player.play(tracks)
        
        elif server["Mode"] == "Repeat":
            Song = server["Queue"][0]["song_id"]
            tracks = await self.bot.wavelink.build_track(Song)
            await player.play(tracks)

        elif server["Mode"] == "Loop":
            pass
            



    async def build_embed(title,duration,thumbnail,next,author,requester):
        embed = discord.Embed(
            title = "Smilewin Music",
            description = f"Now playing {title}",
            colour = 0xFED000
        )
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name='Duration', value=str(datetime.timedelta(milliseconds=int(duration))))
        embed.add_field(name='Requested By', value=requester.mention)
        embed.add_field(name='Next', value=next)
        return embed

    @commands.command()
    async def play(self, ctx, *, query:str = None):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if query == None:
            if not player.is_playing:
                _data = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
                if _data != None and _data["Queue"] != []:
                    Song = _data["Queue"][0]["song_id"]
                    tracks = await self.bot.wavelink.build_track(Song)
                    if player.is_connected:
                        await player.play(tracks)
                        await ctx.send("Resuming")
                    else:
                        await ctx.invoke(self.connect_)
                        await player.play(tracks)
                        await ctx.send("Reconnected and playing")
                    return
                else:
                    await ctx.send("Please specify a song to play")
                    return
            else:
                await ctx.send("Please specify a song to play")
                return
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
        if tracks:
            song_id = tracks[0].id
            song_title = tracks[0].title
            song_duration = tracks[0].duration
            song_thumbnail = tracks[0].thumb
            song_author = tracks[0].author

            Queue = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
            if Queue is None and not player.is_playing:

                data = {
                    "guild_id":ctx.guild.id,
                    "Mode":"Default",
                    "Queue":[{"song_title":song_title,"song_id":song_id,"requester":ctx.author.id}]
                }
                await settings.collectionmusic.insert_one(data)
                player = self.bot.wavelink.get_player(ctx.guild.id)
                if not player.is_connected:
                    await ctx.invoke(self.connect_)
                embed = await Music.build_embed(song_title,song_duration,song_thumbnail,"-",song_author,ctx.author)
                await ctx.send(embed=embed)
                await ctx.send(f'Added {song_title} to the queue.')
                await player.play(tracks[0])
            
            else:
                if not len(Queue["Queue"]) > 25:
                    await settings.collectionmusic.update_one({'guild_id': ctx.guild.id}, {'$push': {'Queue': {"song_title":song_title,"song_id":song_id,"requester":ctx.author.id}}})
                    if not player.is_playing:
                        if Queue["Queue"] == []:
                            if player.is_connected:
                                await player.play(tracks[0])
                            else:
                                await ctx.invoke(self.connect_)
                                await player.play(tracks[0])
                        else:
                            Song = Queue["Queue"][0]["song_id"]
                            tracks = await self.bot.wavelink.build_track(Song)
                            if player.is_connected:
                                await player.play(tracks)
                            else:
                                await ctx.invoke(self.connect_)
                                await player.play(tracks)
                    await ctx.send(f'Added {song_title} to the queue.')
                else:
                    await ctx.send("คิวห้ามเกิน 25")
        else:        
            return await ctx.send('Could not find any songs with that query.')
    
    #auto disconnect for 5 minute after a bot is not playing
    async def auto_disconnect(self,player):
        while player.is_playing: #Checks if voice is playing
            await asyncio.sleep(1) #While it's playing it sleeps for 1 second
        else:
            await asyncio.sleep(30) #If it's not playing it waits 30 seconds
            while player.is_playing: #and checks once again if the bot is not playing
                break #if it's playing it breaks
            else:
                await player.destroy() #if not it disconnects

    async def disconnect_handler(self, guild_id):
        player = self.bot.wavelink.get_player(guild_id)
        await player.stop()
        await settings.collectionmusic.delete_one({"guild_id": guild_id})

def setup(bot):
    bot.add_cog(Music(bot))