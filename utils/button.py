import nextcord
from cogs.music import Music
class MusicButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label=' :play_pause:', 
        style=nextcord.ButtonStyle.green,
        custom_id="pause_stop")
    async def pause_stop_button(self, button: nextcord.ui.button, interaction : nextcord.Interaction):
        print("yellow")
        await self.handle_click(button, interaction)
    
    @nextcord.ui.button(
        label =" :track_next: ",
        style=nextcord.ButtonStyle.secondary,
        custom_id="skip_song")
    async def skip_button(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :stop_button: ",
        style=nextcord.ButtonStyle.danger ,
        custom_id="stop")
    async def stop_button(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :repeat_one: ",
        style=nextcord.ButtonStyle.secondary ,
        custom_id="repeat_song")
    async def stop_button(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :repeat: ",
        style=nextcord.ButtonStyle.secondary ,
        custom_id="loop_playlist")
    async def loop_button(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :sound: เพิ่มเสียง ",
        style=nextcord.ButtonStyle.primary ,
        custom_id="increase_volume")
    async def vol_up_btn(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :loud_sound: ลดเสียง ",
        style=nextcord.ButtonStyle.primary ,
        custom_id="decrease_volume")
    async def vol_down_btn(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label=" :mute: เพิ่มเสียง ",
        style=nextcord.ButtonStyle.primary ,
        custom_id="mute_volume")
    async def vol_mute_btn(self , button : nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)