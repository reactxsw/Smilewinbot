from discord import colour, embeds
from wavelink.node import Node
from wavelink.player import Track
import settings
from discord.ext import commands
from utils.languageembed import languageEmbed
import discord
import wavelink
import settings
import re
import datetime



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
    async def play(self, ctx, *, query: str):
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
                if not len(Queue["Queue"]) > 20:
                    await settings.collectionmusic.update_one({'guild_id': ctx.guild.id}, {'$push': {'Queue': {"song_title":song_title,"song_id":song_id,"requester":ctx.author.id}}})

                else:
                    await ctx.send("คิวห้ามเกิน 20")
        else:        
            return await ctx.send('Could not find any songs with that query.')

def setup(bot):
    bot.add_cog(Music(bot))