import settings
from discord.ext import commands
from utils.languageembed import languageEmbed
import discord
import wavelink
import settings
import re

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
                "region": settings.lavalinkregion,
            }
        }

        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready")

    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node: wavelink.Node, payload:wavelink.events.TrackEnd):
        if payload.reason == "FINISHED":
            pass
        print(payload.reason)
        print(node)

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
        pass

    @commands.command()
    async def pause(self,ctx):
        pass

    @commands.command()
    async def resume(self,ctx):
        pass

    @commands.command()
    async def loop(self,ctx):
        pass
    
    async def do_next(self,ctx):
        pass

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not tracks:
            return await ctx.send('Could not find any songs with that query.')
        Queue = await settings.collectionmusic.find_one({"guild_id":ctx.guild.id})
        if Queue is None and not player.is_playing:
            data = {
                "guild_id":ctx.guild.id,
                "Queue":[str(tracks[0])]
            }
            await settings.collectionmusic.insert_one(data)
        
        else:
            if len(Queue["Queue"]) > 24 :
                return

            else:
                await settings.collectionmusic.update({'guild_id': ctx.guild.id}, {'$push': {'Queue': tracks[0]}})

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(tracks[0])



def setup(bot):
    bot.add_cog(Music(bot))