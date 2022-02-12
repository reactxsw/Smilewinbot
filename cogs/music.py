from contextvars import Context
from traceback import print_tb
from unittest import result
import pomice
import datetime
import asyncio
from contextlib import suppress
import settings
from nextcord.ext import commands
import nextcord
import math
import random
from utils.languageembed import languageEmbed


async def time_format(seconds: int):
    if seconds is not None:
        seconds = int(seconds)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if h > 0:
            return f"[{h:02d}:{m:02d}:{s:02d}]"
        elif m > 0:
            return f"[{m:02d}:{s:02d}]"
        elif s > 0:
            return "[00:{s:02d}]"

        else:
            return "[0:00]"


class MusicButton(nextcord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label=" ⏯ ", style=nextcord.ButtonStyle.green, custom_id="pause_stop", row=0
    )
    async def pause_stop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" ⏭ ", style=nextcord.ButtonStyle.secondary, custom_id="skip_song", row=0
    )
    async def skip_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" ⏹ ", style=nextcord.ButtonStyle.red, custom_id="stop_song", row=0
    )
    async def stop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" 🔂 ",
        style=nextcord.ButtonStyle.secondary,
        custom_id="repeat_song",
        row=0,
    )
    async def repeat_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" 🔁 ",
        style=nextcord.ButtonStyle.secondary,
        custom_id="loop_playlist",
        row=0,
    )
    async def loop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" 🔊 เพิ่มเสียง ",
        style=nextcord.ButtonStyle.primary,
        custom_id="increase_volume",
        row=1,
    )
    async def vol_up_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" 🔈 ลดเสียง  ",
        style=nextcord.ButtonStyle.primary,
        custom_id="decrease_volume",
        row=1,
    )
    async def vol_down_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" 🔇    เปิด / ปิดเสียง     ",
        style=nextcord.ButtonStyle.primary,
        custom_id="mute_unmute_volume",
        row=1,
    )
    async def vol_mute_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Music.handle_click(self, button, interaction)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.pomice = pomice.NodePool()
        bot.loop.create_task(self.start_nodes())

    async def build_spotify_track(self, identifier, guild):
        player: pomice.Player = self.pomice._nodes[
            settings.lavalinkindentifier
        ].get_player(guild)
        results = await player.get_tracks(
            f"https://open.spotify.com/track/{identifier}"
        )
        return results[0]

    async def setnewserver(self, ctx):
        newserver = {
            "guild_id": ctx.guild.id,
            "welcome_id": "None",
            "leave_id": "None",
            "webhook_url": "None",
            "webhook_channel_id": "None",
            "webhook_status": "None",
            "introduce_channel_id": "None",
            "introduce_frame": "None",
            "introduce_role_give_id": "None",
            "introduce_role_remove_id": "None",
            "introduce_status": "YES",
            "level_system": "NO",
            "economy_system": "NO",
            "currency": "$",
            "verification_system": "NO",
            "verification_time": 10,
            "verification_channel_id": "None",
            "verification_role_give_id": "None",
            "verification_role_remove_id": "None",
            "log_voice_system": "NO",
            "log_delete_system": "NO",
            "log_name_system": "NO",
            "log_channel_id": "None",
            "scam": "warn",
            "Music_channel_id": "None",
            "Embed_message_id": "None",
            "Music_message_id": "None",
        }
        return newserver

    async def start_nodes(self):
        await self.bot.wait_until_ready()
        await self.pomice.create_node(
            bot=self.bot,
            host=settings.lavalinkip,
            port=settings.lavalinkport,
            password=settings.lavalinkpass,
            identifier=settings.lavalinkindentifier,
            region=settings.lavalinkregion,
            spotify_client_id=settings.lavalinkspotifyid,
            spotify_client_secret=settings.lavalinkspotifysecret,
        )
        print(f"Node is ready!")

    @commands.Cog.listener()
    async def on_pomice_track_end(self, player: pomice.player, track, _):
        await Music.do_next(self, player)

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: pomice.player, track, _):
        await Music.do_next(self, player)

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, player: pomice.player, track, _):
        await Music.do_next(self, player)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if (
            member.guild.voice_client != None
            and len(member.guild.voice_client.channel.members) == 1
        ):
            data = await settings.collection.find_one({"guild_id": member.guild.id})
            player = member.guild.voice_client
            if player != None:
                await player.destroy()
            await settings.collectionmusic.delete_one({"guild_id": member.guild.id})
            message = await self.bot.get_channel(
                data["Music_channel_id"]
            ).fetch_message(data["Embed_message_id"])
            embed = nextcord.Embed(
                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                colour=0xFFFF00,
            )
            embed.set_author(
                name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                icon_url=self.bot.user.avatar.url,
            )
            embed.set_image(
                url="https://smilewinbot.web.app/assets/image/host/music.png"
            )
            embed.set_footer(text=f"server : {member.guild.name}")
            await message.edit(
                content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ", embed=embed
            )

        else:
            if after.channel is None and member == self.bot.user:
                player: pomice.player = self.pomice._nodes[
                    settings.lavalinkindentifier
                ].get_player(member.guild.id)
                if player != None:
                    await player.destroy()
                await settings.collectionmusic.delete_one({"guild_id": member.guild.id})
                data = await settings.collection.find_one({"guild_id": member.guild.id})
                message = await self.bot.get_channel(
                    data["Music_channel_id"]
                ).fetch_message(data["Embed_message_id"])
                embed = nextcord.Embed(
                    description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                    colour=0xFFFF00,
                )
                embed.set_author(
                    name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                    icon_url=self.bot.user.avatar.url,
                )
                embed.set_image(
                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                )
                embed.set_footer(text=f"server : {member.guild.name}")
                await message.edit(
                    content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                    embed=embed,
                )

    async def do_next(self, player: pomice.Player):
        data = await settings.collection.find_one({"guild_id": player.guild.id})
        message = await self.bot.get_channel(data["Music_channel_id"]).fetch_message(
            data["Embed_message_id"]
        )
        server = await settings.collectionmusic.find_one({"guild_id": player.guild.id})
        if server != None:
            if server["Mode"] == "Default":
                await settings.collectionmusic.update_one(
                    {"guild_id": player.guild.id}, {"$pop": {"Queue": -1}}
                )
                server = await settings.collectionmusic.find_one(
                    {"guild_id": player.guild.id}
                )
                if server["Queue"] == []:
                    await settings.collectionmusic.delete_one(
                        {"guild_id": player.guild.id}
                    )
                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                        icon_url=self.bot.user.avatar.url,
                    )
                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/music.png"
                    )
                    embed.set_footer(text=f"server : {player.guild.name}")
                    await message.edit(
                        content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                        embed=embed,
                    )
                    await player.destroy()

                else:
                    queue = len(server["Queue"])
                    list_song = []
                    num = 1
                    for song in server["Queue"]:
                        list_song.append(
                            f"**{num}.** "
                            + song["song_title"]
                            + " -"
                            + player.guild.get_member(song["requester"]).mention
                            + "\n"
                        )
                        num = num + 1
                        if num > 20:
                            list_song.append(f"เเละอีก {queue-20} เพลง")
                            break
                    list_song = "".join(list_song)
                    if server["Queue"][0]["source"] == "Spotify":
                        tracks: pomice.Track = await Music.build_spotify_track(
                            self, server["Queue"][0]["song_id"], player.guild.id
                        )
                    else:
                        tracks: pomice.Track = await self.pomice._nodes[
                            settings.lavalinkindentifier
                        ].build_track(server["Queue"][0]["song_id"])
                    time = await time_format(tracks.length / 1000)
                    nu = (
                        None
                        if len(server["Queue"]) == 1
                        else server["Queue"][1]["song_title"]
                    )
                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name=f"กําลังเล่น {time}" + tracks.title,
                        icon_url=self.bot.user.avatar.url,
                        url=tracks.uri,
                    )
                    embed.add_field(
                        name="``📞`` ช่องเสียง",
                        value=player.guild.me.voice.channel.mention,
                    )
                    embed.add_field(name="``🔊`` ระดับเสียงเพลง", value=player.volume)
                    embed.add_field(name="``🔁`` โหมด", value="Default")
                    embed.add_field(
                        name="``🍬`` ผู้ขอเพลง",
                        value=player.guild.get_member(
                            server["Queue"][0]["requester"]
                        ).mention,
                    )
                    if not tracks.thumbnail is None:
                        embed.set_image(url=tracks.thumbnail)
                    else:
                        embed.set_image(
                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                        )
                    if nu is None:
                        embed.set_footer(
                            text=f"server : {player.guild.name} | เพลงในคิว : 1"
                        )
                    else:
                        embed.set_footer(text=f"next up : {nu} | เพลงในคิว : {queue}")
                    await message.edit(
                        content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                    )
                    await player.play(tracks)

            elif server["Mode"] == "Repeat":
                if server["Queue"] != []:
                    if server["Queue"][0]["source"] == "Spotify":
                        tracks: pomice.Track = await Music.build_spotify_track(
                            self, server["Queue"][0]["song_id"], player.guild.id
                        )
                    else:
                        tracks: pomice.Track = await self.pomice._nodes[
                            settings.lavalinkindentifier
                        ].build_track(server["Queue"][0]["song_id"])
                    await player.play(tracks)

                else:
                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                        icon_url=self.bot.user.avatar.url,
                    )
                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/music.png"
                    )
                    embed.set_footer(text=f"server : {player.guild.name}")
                    await message.edit(
                        content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                        embed=embed,
                    )

            else:
                queue = len(server["Queue"])
                if server["Queue"] != []:
                    await settings.collectionmusic.update_one(
                        {"guild_id": player.guild.id}, {"$pop": {"Queue": -1}}
                    )
                    await settings.collectionmusic.update_one(
                        {"guild_id": player.guild.id},
                        {
                            "$push": {
                                "Queue": {
                                    "source": server["Queue"][0]["source"],
                                    "song_title": server["Queue"][0]["song_title"],
                                    "song_id": server["Queue"][0]["song_id"],
                                    "requester": server["Queue"][0]["requester"],
                                }
                            }
                        },
                    )
                    server = await settings.collectionmusic.find_one(
                        {"guild_id": player.guild.id}
                    )
                    list_song = []
                    num = 1
                    for song in server["Queue"]:
                        list_song.append(
                            f"**{num}.** "
                            + song["song_title"]
                            + " -"
                            + player.guild.get_member(song["requester"]).mention
                            + "\n"
                        )
                        num = num + 1
                        if num > 20:
                            list_song.append(f"เเละอีก {queue-20} เพลง")
                            break
                    list_song = "".join(list_song)
                    if server["Queue"][0]["source"] == "Spotify":
                        tracks: pomice.Track = await Music.build_spotify_track(
                            self, server["Queue"][0]["song_id"], player.guild.id
                        )
                    else:
                        tracks: pomice.Track = await self.pomice._nodes[
                            settings.lavalinkindentifier
                        ].build_track(server["Queue"][0]["song_id"])
                    time = await time_format(tracks.length / 1000)
                    nu = (
                        "None"
                        if len(server["Queue"]) == 1
                        else server["Queue"][1]["song_title"]
                    )
                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name=f"กําลังเล่น {time}" + tracks.title,
                        icon_url=self.bot.user.avatar.url,
                        url=tracks.uri,
                    )
                    embed.add_field(
                        name="``📞`` ช่องเสียง",
                        value=player.guild.me.voice.channel.mention,
                    )
                    embed.add_field(name="``🔊`` ระดับเสียงเพลง", value=player.volume)
                    embed.add_field(name="``🔁`` โหมด", value="Loop")
                    embed.add_field(
                        name="``🍬`` ผู้ขอเพลง",
                        value=player.guild.get_member(
                            server["Queue"][0]["requester"]
                        ).mention,
                    )
                    if not tracks.thumbnail is None:
                        embed.set_image(url=tracks.thumbnail)
                    else:
                        embed.set_image(
                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                        )
                    embed.set_footer(text=f"next up : {nu} | เพลงในคิว : {queue}")
                    await message.edit(
                        content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                    )
                    await player.play(tracks)

                else:
                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                        icon_url=self.bot.user.avatar.url,
                    )
                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/music.png"
                    )
                    embed.set_footer(text=f"server : {player.guild.name}")
                    await message.edit(
                        content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                        embed=embed,
                    )

        else:
            embed = nextcord.Embed(
                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                colour=0xFFFF00,
            )
            embed.set_author(
                name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                icon_url=self.bot.user.avatar.url,
            )
            embed.set_image(
                url="https://smilewinbot.web.app/assets/image/host/music.png"
            )
            embed.set_footer(text=f"server : {player.guild.name}")
            await message.edit(
                content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ", embed=embed
            )

    @commands.command(aliases=["joi", "j", "summon", "su", "con"])
    async def join(
        self, ctx: commands.Context, *, channel: nextcord.VoiceChannel = None
    ) -> None:
        if not channel:
            channel = getattr(ctx.author.voice, "channel", None)
            if not channel:
                return await ctx.send(
                    "You must be in a voice channel in order to use this command!",
                    delete_after=3,
                )

        await ctx.author.voice.channel.connect(cls=pomice.Player)
        await ctx.send(f"Joined the voice channel `{channel.name}`", delete_after=3)

    @commands.command(aliases=["disconnect", "dc", "disc", "lv"])
    async def leave(self, ctx: commands.Context):
        if not (player := ctx.voice_client):
            return await ctx.send(
                "You must have the bot in a channel in order to use this command",
                delete_after=3,
            )

        await player.destroy()
        await ctx.send("Player has left the channel.")

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        data = await settings.collectionmusic.find_one(
            {"guild_id": interaction.guild.id}
        )
        server = await settings.collection.find_one({"guild_id": interaction.guild.id})
        num = 1
        list_song = []
        player: pomice.Player = interaction.guild.voice_client
        if not player is None and not data is None:
            nu = None if len(data["Queue"]) < 2 else data["Queue"][1]["song_title"]
            queue = len(data["Queue"])
            if (
                interaction.user.id == data["Queue"][0]["requester"]
                or interaction.user.guild_permissions.administrator
            ):
                if button.custom_id == "pause_stop":
                    if player.is_paused and player.is_connected:
                        await player.set_pause(False)
                        embed = nextcord.Embed(title="เล่นเพลงต่อ", colour=0xFED000)

                        await interaction.channel.send(embed=embed, delete_after=2)

                    elif not player.is_paused and player.is_connected:
                        await player.set_pause(True)
                        embed = nextcord.Embed(title="หยุดเล่นพลง", colour=0xFED000)
                        await interaction.channel.send(embed=embed, delete_after=2)

                elif button.custom_id == "increase_volume":
                    if player.volume < 90:
                        await player.set_volume(player.volume + 10)
                        embed = nextcord.Embed(
                            title=f"ตั้งระดับเสียง : {player.volume}", colour=0xFED000
                        )
                        await interaction.channel.send(embed=embed, delete_after=2)
                        for song in data["Queue"]:
                            list_song.append(
                                f"**{num}.** "
                                + song["song_title"]
                                + " -"
                                + player.guild.get_member(song["requester"]).mention
                                + "\n"
                            )
                            num = num + 1
                            if num > 20:
                                list_song.append(f"เเละอีก {queue-20} เพลง")
                                break
                        list_song = "".join(list_song)
                        time = await time_format(player.current.length / 1000)
                        embed = nextcord.Embed(
                            description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                            colour=0xFFFF00,
                        )
                        embed.set_author(
                            name=f"กําลังเล่น {time}" + player.current.title,
                            icon_url=self.bot.user.avatar.url,
                            url=player.current.uri,
                        )
                        embed.add_field(
                            name="``📞`` ช่องเสียง",
                            value=player.guild.me.voice.channel.mention,
                        )
                        embed.add_field(
                            name="``🔊`` ระดับเสียงเพลง", value=player.volume
                        )
                        embed.add_field(name="``🔁`` โหมด", value=data["Mode"])
                        embed.add_field(
                            name="``🍬`` ผู้ขอเพลง",
                            value=player.guild.get_member(
                                data["Queue"][0]["requester"]
                            ).mention,
                        )
                        if not player.current.thumbnail is None:
                            embed.set_image(url=player.current.thumbnail)
                        else:
                            embed.set_image(
                                url="https://smilewinbot.web.app/assets/image/host/music.png"
                            )
                        if nu == None:
                            embed.set_footer(
                                text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                            )
                        else:
                            embed.set_footer(
                                text=f"next up : {nu} | เพลงในคิว : {queue}"
                            )
                        message = await self.bot.get_channel(
                            server["Music_channel_id"]
                        ).fetch_message(server["Embed_message_id"])
                        await message.edit(
                            content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                        )

                    else:
                        embed = nextcord.Embed(
                            title=f"ระดับเสียงสูงสุดเเล้ว", colour=0xFED000
                        )
                        await interaction.channel.send(embed=embed, delete_after=2)

                elif button.custom_id == "stop_song":
                    embed = nextcord.Embed(title="หยุดเล่นเพลง", colour=0xFED000)
                    await interaction.channel.send(embed=embed, delete_after=2)
                    await player.destroy()

                elif button.custom_id == "decrease_volume":
                    if player.volume > 10:
                        await player.set_volume(player.volume - 10)
                        embed = nextcord.Embed(
                            title=f"ตั้งระดับเสียง : {player.volume}", colour=0xFED000
                        )
                        await interaction.channel.send(embed=embed, delete_after=2)
                        for song in data["Queue"]:
                            list_song.append(
                                f"**{num}.** "
                                + song["song_title"]
                                + " -"
                                + player.guild.get_member(song["requester"]).mention
                                + "\n"
                            )
                            num = num + 1
                            if num > 20:
                                list_song.append(f"เเละอีก {queue-20} เพลง")
                                break
                        list_song = "".join(list_song)
                        time = await time_format(player.current.length / 1000)
                        embed = nextcord.Embed(
                            description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                            colour=0xFFFF00,
                        )
                        embed.set_author(
                            name=f"กําลังเล่น {time}" + player.current.title,
                            icon_url=self.bot.user.avatar.url,
                            url=player.current.uri,
                        )
                        embed.add_field(
                            name="``📞`` ช่องเสียง",
                            value=player.guild.me.voice.channel.mention,
                        )
                        embed.add_field(
                            name="``🔊`` ระดับเสียงเพลง", value=player.volume
                        )
                        embed.add_field(name="``🔁`` โหมด", value=data["Mode"])
                        embed.add_field(
                            name="``🍬`` ผู้ขอเพลง",
                            value=player.guild.get_member(
                                data["Queue"][0]["requester"]
                            ).mention,
                        )
                        if not player.current.thumbnail is None:
                            embed.set_image(url=player.current.thumbnail)
                        else:
                            embed.set_image(
                                url="https://smilewinbot.web.app/assets/image/host/music.png"
                            )
                        if nu == None:
                            embed.set_footer(
                                text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                            )
                        else:
                            embed.set_footer(
                                text=f"next up : {nu} | เพลงในคิว : {queue}"
                            )
                        message = await self.bot.get_channel(
                            server["Music_channel_id"]
                        ).fetch_message(server["Embed_message_id"])
                        await message.edit(
                            content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                        )

                    else:
                        embed = nextcord.Embed(
                            title=f"ระดับเสียงตํ่าสุดเเล้ว", colour=0xFED000
                        )
                        await interaction.channel.send(embed=embed, delete_after=2)

                elif button.custom_id == "mute_unmute_volume":
                    if player.volume == 0:
                        await player.set_volume(80)
                        embed = nextcord.Embed(title=f"เปิดเสียง", colour=0xFED000)
                        await interaction.channel.send(embed=embed, delete_after=2)

                    else:
                        await player.set_volume(0)
                        embed = nextcord.Embed(title=f"ปิดเสียง", colour=0xFED000)
                        await interaction.channel.send(embed=embed, delete_after=2)

                elif button.custom_id == "skip_song":
                    if player.is_connected and player.is_playing:
                        embed = nextcord.Embed(title="ข้ามเพลง", colour=0xFED000)
                        await interaction.channel.send(embed=embed, delete_after=2)
                        await player.stop()

                elif button.custom_id == "repeat_song":
                    if player.is_connected and player.is_playing:
                        if not data["Mode"] == "Repeat":
                            await settings.collectionmusic.update_one(
                                {"guild_id": interaction.guild.id},
                                {"$set": {"Mode": "Repeat"}},
                            )
                            embed = nextcord.Embed(
                                title="เปิดการเล่นซ้ำ 1 เพลง", colour=0xFED000
                            )
                            await interaction.channel.send(embed=embed, delete_after=2)
                            for song in data["Queue"]:
                                list_song.append(
                                    f"**{num}.** "
                                    + song["song_title"]
                                    + " -"
                                    + player.guild.get_member(song["requester"]).mention
                                    + "\n"
                                )
                                num = num + 1
                                if num > 20:
                                    list_song.append(f"เเละอีก {queue-20} เพลง")
                                    break
                            list_song = "".join(list_song)
                            time = await time_format(player.current.length / 1000)
                            embed = nextcord.Embed(
                                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                colour=0xFFFF00,
                            )
                            embed.set_author(
                                name=f"กําลังเล่น {time}" + player.current.title,
                                icon_url=self.bot.user.avatar.url,
                                url=player.current.uri,
                            )
                            embed.add_field(
                                name="``📞`` ช่องเสียง",
                                value=player.guild.me.voice.channel.mention,
                            )
                            embed.add_field(
                                name="``🔊`` ระดับเสียงเพลง", value=player.volume
                            )
                            embed.add_field(name="``🔁`` โหมด", value="Repeat")
                            embed.add_field(
                                name="``🍬`` ผู้ขอเพลง",
                                value=player.guild.get_member(
                                    data["Queue"][0]["requester"]
                                ).mention,
                            )
                            if not player.current.thumbnail is None:
                                embed.set_image(url=player.current.thumbnail)
                            else:
                                embed.set_image(
                                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                                )
                            if nu == None:
                                embed.set_footer(
                                    text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                                )
                            else:
                                embed.set_footer(
                                    text=f"next up : {nu} | เพลงในคิว : {queue}"
                                )
                            message = await self.bot.get_channel(
                                server["Music_channel_id"]
                            ).fetch_message(server["Embed_message_id"])
                            await message.edit(
                                content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                            )

                        elif data["Mode"] == "Repeat":
                            await settings.collectionmusic.update_one(
                                {"guild_id": interaction.guild.id},
                                {"$set": {"Mode": "Default"}},
                            )
                            embed = nextcord.Embed(
                                title="ปิดการเล่นซ้ำ 1 เพลง", colour=0xFED000
                            )
                            await interaction.channel.send(embed=embed, delete_after=2)
                            for song in data["Queue"]:
                                list_song.append(
                                    f"**{num}.** "
                                    + song["song_title"]
                                    + " -"
                                    + player.guild.get_member(song["requester"]).mention
                                    + "\n"
                                )
                                num = num + 1
                                if num > 20:
                                    list_song.append(f"เเละอีก {queue-20} เพลง")
                                    break
                            list_song = "".join(list_song)
                            time = await time_format(player.current.length / 1000)
                            embed = nextcord.Embed(
                                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                colour=0xFFFF00,
                            )
                            embed.set_author(
                                name=f"กําลังเล่น {time}" + player.current.title,
                                icon_url=self.bot.user.avatar.url,
                                url=player.current.uri,
                            )
                            embed.add_field(
                                name="``📞`` ช่องเสียง",
                                value=player.guild.me.voice.channel.mention,
                            )
                            embed.add_field(
                                name="``🔊`` ระดับเสียงเพลง", value=player.volume
                            )
                            embed.add_field(name="``🔁`` โหมด", value="Default")
                            embed.add_field(
                                name="``🍬`` ผู้ขอเพลง",
                                value=player.guild.get_member(
                                    data["Queue"][0]["requester"]
                                ).mention,
                            )
                            if not player.current.thumbnail is None:
                                embed.set_image(url=player.current.thumbnail)
                            else:
                                embed.set_image(
                                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                                )
                            if nu == None:
                                embed.set_footer(
                                    text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                                )
                            else:
                                embed.set_footer(
                                    text=f"next up : {nu} | เพลงในคิว : {queue}"
                                )
                            message = await self.bot.get_channel(
                                server["Music_channel_id"]
                            ).fetch_message(server["Embed_message_id"])
                            await message.edit(
                                content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                            )

                elif button.custom_id == "loop_playlist":
                    if player.is_connected and player.is_playing:
                        if not data["Mode"] == "Loop":
                            await settings.collectionmusic.update_one(
                                {"guild_id": interaction.guild.id},
                                {"$set": {"Mode": "Loop"}},
                            )
                            embed = nextcord.Embed(
                                title="เปิดการเล่นซ้ำทั้งเพลย์ลิส", colour=0xFED000
                            )
                            await interaction.channel.send(embed=embed, delete_after=2)
                            for song in data["Queue"]:
                                list_song.append(
                                    f"**{num}.** "
                                    + song["song_title"]
                                    + " -"
                                    + player.guild.get_member(song["requester"]).mention
                                    + "\n"
                                )
                                num = num + 1
                                if num > 20:
                                    list_song.append(f"เเละอีก {queue-20} เพลง")
                                    break
                            list_song = "".join(list_song)
                            time = await time_format(player.current.length / 1000)
                            embed = nextcord.Embed(
                                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                colour=0xFFFF00,
                            )
                            embed.set_author(
                                name=f"กําลังเล่น {time}" + player.current.title,
                                icon_url=self.bot.user.avatar.url,
                                url=player.current.uri,
                            )
                            embed.add_field(
                                name="``📞`` ช่องเสียง",
                                value=player.guild.me.voice.channel.mention,
                            )
                            embed.add_field(
                                name="``🔊`` ระดับเสียงเพลง", value=player.volume
                            )
                            embed.add_field(name="``🔁`` โหมด", value="Loop")
                            embed.add_field(
                                name="``🍬`` ผู้ขอเพลง",
                                value=player.guild.get_member(
                                    data["Queue"][0]["requester"]
                                ).mention,
                            )
                            if not player.current.thumbnail is None:
                                embed.set_image(url=player.current.thumbnail)
                            else:
                                embed.set_image(
                                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                                )
                            if nu == None:
                                embed.set_footer(
                                    text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                                )
                            else:
                                embed.set_footer(
                                    text=f"next up : {nu} | เพลงในคิว : {queue}"
                                )
                            message = await self.bot.get_channel(
                                server["Music_channel_id"]
                            ).fetch_message(server["Embed_message_id"])
                            await message.edit(
                                content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                            )

                        elif data["Mode"] == "Loop":
                            await settings.collectionmusic.update_one(
                                {"guild_id": interaction.guild.id},
                                {"$set": {"Mode": "Default"}},
                            )
                            embed = nextcord.Embed(
                                title="ปิดการเล่นซ้ำทั้งเพลย์ลิส", colour=0xFED000
                            )
                            await interaction.channel.send(embed=embed, delete_after=2)
                            for song in data["Queue"]:
                                list_song.append(
                                    f"**{num}.** "
                                    + song["song_title"]
                                    + " -"
                                    + player.guild.get_member(song["requester"]).mention
                                    + "\n"
                                )
                                num = num + 1
                                if num > 20:
                                    list_song.append(f"เเละอีก {queue-20} เพลง")
                                    break
                            list_song = "".join(list_song)
                            time = await time_format(player.current.length / 1000)
                            embed = nextcord.Embed(
                                description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                colour=0xFFFF00,
                            )
                            embed.set_author(
                                name=f"กําลังเล่น {time}" + player.current.title,
                                icon_url=self.bot.user.avatar.url,
                                url=player.current.uri,
                            )
                            embed.add_field(
                                name="``📞`` ช่องเสียง",
                                value=player.guild.me.voice.channel.mention,
                            )
                            embed.add_field(
                                name="``🔊`` ระดับเสียงเพลง", value=player.volume
                            )
                            embed.add_field(name="``🔁`` โหมด", value="Default")
                            embed.add_field(
                                name="``🍬`` ผู้ขอเพลง",
                                value=player.guild.get_member(
                                    data["Queue"][0]["requester"]
                                ).mention,
                            )
                            if not player.current.thumbnail is None:
                                embed.set_image(url=player.current.thumbnail)
                            else:
                                embed.set_image(
                                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                                )
                            if nu == None:
                                embed.set_footer(
                                    text=f"server : {player.guild.name} | เพลงในคิว : {queue}"
                                )
                            else:
                                embed.set_footer(
                                    text=f"next up : {nu} | เพลงในคิว : {queue}"
                                )
                            message = await self.bot.get_channel(
                                server["Music_channel_id"]
                            ).fetch_message(server["Embed_message_id"])
                            await message.edit(
                                content=f"__รายการเพลง:__🎵\n {list_song} ", embed=embed
                            )

            else:
                embed = nextcord.Embed(
                    description=f"{interaction.user.mention} ไม่มีสิทธิ์ตั้งค่า",
                    colour=0x983925,
                )
                await interaction.channel.send(embed=embed, delete_after=2)
        else:
            embed = nextcord.Embed(
                description=f"{interaction.user.mention} ไม่มีเพลงเล่นอยู่",
                colour=0x983925,
            )
            await interaction.channel.send(embed=embed, delete_after=2)

    @commands.command(aliases=["pla", "p"])
    async def play(self, ctx: commands.Context, *, search: str):
        server = await settings.collection.find_one({"guild_id": ctx.guild.id})
        if server is not None:
            music_channel = server["Music_channel_id"]
            music_embed = server["Embed_message_id"]
            music_message = server["Music_message_id"]
            if music_channel != "None":
                if music_embed != "None" and music_message != "None":
                    if ctx.channel.id == music_channel:
                        player: pomice.Player = self.pomice._nodes[
                            settings.lavalinkindentifier
                        ].get_player(ctx.guild.id)
                        if player is None:
                            await ctx.invoke(self.join)
                            player = ctx.voice_client
                        results = await player.get_tracks(search, ctx=ctx)
                        if not results:
                            return await ctx.send(
                                "No results were found for that search term",
                                delete_after=7,
                            )

                        Queue = await settings.collectionmusic.find_one(
                            {"guild_id": ctx.guild.id}
                        )
                        if isinstance(results, pomice.Playlist):
                            if Queue is None and not player.is_playing:
                                if len(results.tracks) > 50:
                                    tracks = results.tracks[:50]
                                else:
                                    tracks = results.tracks
                                num = 1
                                list_song = []
                                data = {
                                    "guild_id": ctx.guild.id,
                                    "Mode": "Default",
                                    "Request_channel": ctx.channel.id,
                                    "Queue": [],
                                }
                                for track in tracks:
                                    list_song.append(
                                        f"**{num}.** "
                                        + track.title
                                        + " -"
                                        + ctx.guild.get_member(ctx.author.id).mention
                                        + "\n"
                                    )
                                    data["Queue"].append(
                                        {
                                            "source": "Spotify"
                                            if "open.spotify.com" in track.uri
                                            else track.info["sourceName"],
                                            "song_title": track.title,
                                            "song_id": track.track_id,
                                            "requester": ctx.author.id,
                                        }
                                    )
                                    num = num + 1
                                if num > 20:
                                    list_song = list_song[:20]
                                    list_song.append(f"เเละอีก {num-20} เพลง")
                                list_song = "".join(list_song)
                                await player.play(tracks[0])
                                nu = tracks[1] if len(tracks) > 1 else None
                                time = await time_format(tracks[0].length)
                                embed = nextcord.Embed(
                                    description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                    colour=0xFFFF00,
                                )

                                embed.set_author(
                                    name=f"กําลังเล่น {time} {tracks[0]}",
                                    icon_url=self.bot.user.avatar.url,
                                    url=tracks[0].uri,
                                )
                                embed.add_field(
                                    name="``📞`` ช่องเสียง",
                                    value=ctx.author.voice.channel.mention,
                                )
                                embed.add_field(
                                    name="``🔊`` ระดับเสียงเพลง", value=player.volume
                                )
                                embed.add_field(name="``🔁`` โหมด", value="Default")
                                embed.add_field(
                                    name="``🍬`` ผู้ขอเพลง", value=ctx.author.mention
                                )
                                if not tracks[0].thumbnail is None:
                                    embed.set_image(url=tracks[0].thumbnail)
                                else:
                                    embed.set_image(
                                        url="https://smilewinbot.web.app/assets/image/host/music.png"
                                    )
                                if nu is None:
                                    embed.set_footer(
                                        text=f"server : {player.guild.name} | เพลงในคิว : 1"
                                    )
                                else:
                                    embed.set_footer(
                                        text=f"server : {ctx.guild.name} | เพลงในคิว : {len(tracks)}"
                                    )
                                message = await self.bot.get_channel(
                                    music_channel
                                ).fetch_message(music_embed)
                                await message.edit(
                                    content=f"__รายการเพลง:__🎵\n{list_song} ",
                                    embed=embed,
                                )
                                await settings.collectionmusic.insert_one(data)

                            else:
                                queue = len(Queue["Queue"])
                                if not queue > 50:
                                    availble = 50 - len(Queue["Queue"])
                                    if len(results.tracks) > availble:
                                        results = results.tracks[:availble]

                                    else:
                                        results = results.tracks

                                    left = queue + len(results)
                                    nu = (
                                        track
                                        if queue < 2
                                        else Queue["Queue"][1]["song_title"]
                                    )
                                    num = 1
                                    list_song = []
                                    for track in results:
                                        Queue["Queue"].append(
                                            {
                                                "source": "Spotify"
                                                if "open.spotify.com" in track.uri
                                                else track.info["sourceName"],
                                                "song_title": track.title,
                                                "song_id": track.track_id,
                                                "requester": ctx.author.id,
                                            }
                                        )
                                        await settings.collectionmusic.update_one(
                                            {"guild_id": ctx.guild.id},
                                            {
                                                "$push": {
                                                    "Queue": {
                                                        "source": "Spotify"
                                                        if "open.spotify.com"
                                                        in track.uri
                                                        else track.info["sourceName"],
                                                        "song_title": track.title,
                                                        "song_id": track.track_id,
                                                        "requester": ctx.author.id,
                                                    }
                                                }
                                            },
                                        )

                                    for data in Queue["Queue"]:
                                        list_song.append(
                                            f"**{num}.** "
                                            + data["song_title"]
                                            + " -"
                                            + ctx.guild.get_member(
                                                data["requester"]
                                            ).mention
                                            + "\n"
                                        )
                                        num = num + 1
                                        if num > 20:
                                            list_song = list_song[:20]
                                            list_song.append(f"เเละอีก {left-20} เพลง")

                                    list_song = "".join(list_song)
                                    nu = (
                                        track
                                        if len(Queue["Queue"]) < 2
                                        else Queue["Queue"][1]["song_title"]
                                    )
                                    embed = nextcord.Embed(
                                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                        colour=0xFFFF00,
                                    )
                                    embed.set_author(
                                        name=f"กําลังเล่น {player.current.title}",
                                        icon_url=self.bot.user.avatar.url,
                                        url=player.current.uri,
                                    )
                                    embed.set_footer(
                                        text=f"next up : {nu} | เพลงในคิว : {left}"
                                    )

                                    if not player.current.thumbnail is None:
                                        embed.set_image(url=player.current.thumbnail)
                                    else:
                                        embed.set_image(
                                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                                        )
                                    message = await self.bot.get_channel(
                                        music_channel
                                    ).fetch_message(music_embed)
                                    await message.edit(
                                        content=f"__รายการเพลง:__🎵\n{list_song} ",
                                        embed=embed,
                                    )

                        else:
                            track: pomice.Track = results[0]
                            s_title = track.title
                            s_id = track.track_id
                            s_source = (
                                "Spotify"
                                if "open.spotify.com" in track.uri
                                else track.info["sourceName"]
                            )
                            s_len = track.length / 1000
                            if Queue is None and not player.is_playing:
                                try:
                                    time = await time_format(s_len)
                                    embed = nextcord.Embed(
                                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                        colour=0xFFFF00,
                                    )

                                    embed.set_author(
                                        name=f"กําลังเล่น {time} {track}",
                                        icon_url=self.bot.user.avatar.url,
                                        url=track.uri,
                                    )
                                    embed.add_field(
                                        name="``📞`` ช่องเสียง",
                                        value=ctx.author.voice.channel.mention,
                                    )
                                    embed.add_field(
                                        name="``🔊`` ระดับเสียงเพลง", value=player.volume
                                    )
                                    embed.add_field(name="``🔁`` โหมด", value="Default")
                                    embed.add_field(
                                        name="``🍬`` ผู้ขอเพลง", value=ctx.author.mention
                                    )
                                    if not track.thumbnail is None:
                                        embed.set_image(url=track.thumbnail)
                                    else:
                                        embed.set_image(
                                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                                        )
                                    embed.set_footer(
                                        text=f"server : {ctx.guild.name} | เพลงในคิว : 1"
                                    )
                                    data = {
                                        "guild_id": ctx.guild.id,
                                        "Mode": "Default",
                                        "Request_channel": ctx.channel.id,
                                        "Queue": [],
                                    }
                                    data["Queue"].append(
                                        {
                                            "source": s_source,
                                            "song_title": s_title,
                                            "song_id": s_id,
                                            "requester": ctx.author.id,
                                        }
                                    )

                                    await player.play(track)
                                    message = await self.bot.get_channel(
                                        music_channel
                                    ).fetch_message(music_embed)
                                    await message.edit(
                                        content=f"__รายการเพลง:__🎵\n **1.** {track} -{ctx.author.mention}",
                                        embed=embed,
                                    )
                                    await settings.collectionmusic.insert_one(data)
                                except Exception as e:
                                    print(e)

                            else:
                                queue = len(Queue["Queue"])
                                if not queue > 50:
                                    nu = (
                                        track
                                        if queue < 2
                                        else Queue["Queue"][1]["song_title"]
                                    )
                                    time = await time_format(
                                        player.current.length / 1000
                                    )
                                    left = queue + 1
                                    list_song = []
                                    num = 1
                                    embed = nextcord.Embed(
                                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                        colour=0xFFFF00,
                                    )
                                    member: nextcord.Member = (
                                        await ctx.guild.fetch_member(
                                            Queue["Queue"][0]["requester"]
                                        )
                                    )
                                    embed.set_author(
                                        name=f"กําลังเล่น {time}"
                                        + player.current.title,
                                        icon_url=self.bot.user.avatar.url,
                                        url=player.current.uri,
                                    )
                                    embed.add_field(
                                        name="``📞`` ช่องเสียง",
                                        value=ctx.guild.me.voice.channel.mention,
                                    )
                                    embed.add_field(
                                        name="``🔊`` ระดับเสียงเพลง", value=player.volume
                                    )
                                    embed.add_field(
                                        name="``🔁`` โหมด", value=Queue["Mode"]
                                    )
                                    embed.add_field(
                                        name="``🍬`` ผู้ขอเพลง", value=member.mention
                                    )
                                    if not track.thumbnail is None:
                                        embed.set_image(url=player.current.thumbnail)
                                    else:
                                        embed.set_image(
                                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                                        )
                                    embed.set_footer(
                                        text=f"next up : {nu} | เพลงในคิว : {left}"
                                    )
                                    data = {
                                        "source": s_source,
                                        "song_title": s_title,
                                        "song_id": s_id,
                                        "requester": ctx.author.id,
                                    }
                                    await settings.collectionmusic.update_one(
                                        {"guild_id": ctx.guild.id},
                                        {"$push": {"Queue": data}},
                                    )

                                    Queue["Queue"].append(data)
                                    for song in Queue["Queue"]:
                                        list_song.append(
                                            f"**{num}.** "
                                            + song["song_title"]
                                            + " -"
                                            + ctx.guild.get_member(
                                                song["requester"]
                                            ).mention
                                            + "\n"
                                        )
                                        num = num + 1
                                        if num > 20:
                                            list_song.append(f"เเละอีก {queue-20}เพลง")
                                            break

                                    list_song = "".join(list_song)

                                    message = await self.bot.get_channel(
                                        music_channel
                                    ).fetch_message(music_embed)
                                    await message.edit(
                                        content=f"__รายการเพลง:__🎵\n {list_song} ",
                                        embed=embed,
                                    )

                                else:
                                    return
                    else:
                        return

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def musicsetup(self, ctx):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            server_language = languageserver["Language"]
            data = await settings.collection.find_one({"guild_id": ctx.guild.id})
            if data is None:
                newserver = await Music.setnewserver(self, ctx)
                await settings.collection.insert_one(newserver)
                channel = await ctx.guild.create_text_channel(
                    name="😁│Smilewin Music",
                    topic=":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง :sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง",
                )

                embed = nextcord.Embed(
                    description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                    colour=0xFFFF00,
                )
                embed.set_author(
                    name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                    icon_url=self.bot.user.avatar.url,
                )
                embed.set_image(
                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                )
                embed.set_footer(text=f"server : {ctx.guild.name}")
                try:
                    embed_message = await channel.send(
                        content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                        embed=embed,
                        view=MusicButton(self),
                    )
                except Exception as e:
                    print(e)
                music_message = await channel.send(
                    "กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง"
                )
                await settings.collection.update_one(
                    {"guild_id": ctx.guild.id},
                    {
                        "$set": {
                            "Music_channel_id": channel.id,
                            "Embed_message_id": embed_message.id,
                            "Music_message_id": music_message.id,
                        }
                    },
                )

                await ctx.reply(f"สร้างห้องสําเร็จ {channel.mention}")
            else:
                if data["Music_channel_id"] == "None":
                    channel: nextcord.TextChannel = await ctx.guild.create_text_channel(
                        name="😁│Smilewin Music",
                        topic=":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง :sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง",
                    )

                    embed = nextcord.Embed(
                        description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                        colour=0xFFFF00,
                    )
                    embed.set_author(
                        name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                        icon_url=self.bot.user.avatar.url,
                    )
                    embed.set_image(
                        url="https://smilewinbot.web.app/assets/image/host/music.png"
                    )
                    embed.set_footer(text=f"server : {ctx.guild.name}")
                    embed_message: nextcord.Message = await channel.send(
                        embed=embed, view=MusicButton(self.bot)
                    )
                    music_message: nextcord.Message = await channel.send(
                        "กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง"
                    )
                    await settings.collection.update_one(
                        {"guild_id": ctx.guild.id},
                        {
                            "$set": {
                                "Music_channel_id": channel.id,
                                "Embed_message_id": embed_message.id,
                                "Music_message_id": music_message.id,
                            }
                        },
                    )
                    await ctx.reply(f"สร้างห้องสําเร็จ {channel.mention}")
                else:
                    channel = self.bot.get_channel(data["Music_channel_id"])
                    if channel is None:
                        channel = await ctx.guild.create_text_channel(
                            name="😁│Smilewin Music",
                            topic=":play_pause: หยุด/เล่นเพลง:track_next: ข้ามเพลง:stop_button: หยุดและลบคิวในเพลง :sound: ลดเสียงขึ้นทีล่ะ 10%:loud_sound: เพิ่มเสียงทีล่ะ 10%:mute: ปิดเสียงเพลง",
                        )

                        embed = nextcord.Embed(
                            description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                            colour=0xFFFF00,
                        )
                        embed.set_author(
                            name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                            icon_url=self.bot.user.avatar.url,
                        )
                        embed.set_image(
                            url="https://smilewinbot.web.app/assets/image/host/music.png"
                        )
                        embed.set_footer(text=f"server : {ctx.guild.name}")
                        embed_message = await channel.send(
                            content="__รายการเพลง:__\n🎵 ไม่มีเพลงที่กำลังเล่นในขณะนี้ ",
                            embed=embed,
                            view=MusicButton(self.bot),
                        )
                        music_message = await channel.send(
                            "กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง"
                        )
                        await settings.collection.update_one(
                            {"guild_id": ctx.guild.id},
                            {
                                "$set": {
                                    "Music_channel_id": channel.id,
                                    "Embed_message_id": embed_message.id,
                                    "Music_message_id": music_message.id,
                                }
                            },
                        )
                        await ctx.reply(f"สร้างห้องสําเร็จ {channel.mention}")
                    else:
                        channel = self.bot.get_channel(data["Music_channel_id"])
                        try:
                            embed_message = await channel.fetch_message(
                                data["Embed_message_id"]
                            )
                            music_message = await channel.fetch_message(
                                data["Music_message_id"]
                            )
                            embed = nextcord.Embed(
                                title="มีห้องเล่นเพลงเเล้ว",
                                colour=0xFFFF00,
                                description=channel.mention,
                            )
                            await ctx.send(embed=embed)
                        except nextcord.NotFound:
                            try:
                                embed_message = await channel.fetch_message(
                                    data["Embed_message_id"]
                                )

                            except nextcord.NotFound:
                                embed = nextcord.Embed(
                                    description="[❯ Invite](https://smilewinbot.web.app/page/invite) | [❯ Website](https://smilewinbot.web.app) | [❯ Support](https://discord.com/invite/R8RYXyB4Cg)",
                                    colour=0xFFFF00,
                                )
                                embed.set_author(
                                    name="❌ ไม่มีเพลงที่เล่นอยู่ ณ ตอนนี้",
                                    icon_url=self.bot.user.avatar.url,
                                )
                                embed.set_image(
                                    url="https://smilewinbot.web.app/assets/image/host/music.png"
                                )
                                embed.set_footer(text=f"server : {ctx.guild.name}")
                                embed_message = await channel.send(
                                    embed=embed, view=MusicButton(self.bot)
                                )
                                await settings.collection.update_one(
                                    {"guild_id": ctx.guild.id},
                                    {"$set": {"Embed_message_id": embed_message.id}},
                                )

                            try:
                                music_message = await channel.fetch_message(
                                    data["Music_message_id"]
                                )
                            except nextcord.NotFound:
                                music_message = await channel.send(
                                    "กรุณาเข้า Voice Channel เเละเพิ่มเพลงโดยพิมพ์ชื่อเพลงหรือลิ้งเพลง"
                                )
                                await settings.collection.update_one(
                                    {"guild_id": ctx.guild.id},
                                    {"$set": {"Music_message_id": music_message.id}},
                                )


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))
    bot.add_view(MusicButton(bot))
