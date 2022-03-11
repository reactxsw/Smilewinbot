import nextcord
import settings
from nextcord.ext import commands
from utils.languageembed import languageEmbed
from utils.language.translate import translate_help


class HelpButton(nextcord.ui.View):
    def __init__(self, Member: nextcord.Member):
        super().__init__(timeout=None)
        self.Member = Member
        self.add_item(
            nextcord.ui.Button(
                style=nextcord.ButtonStyle.link,
                url="https://smilewinbot.web.app/page/server",
                label="ติดต่อซัพพอร์ต",
                row=2,
            )
        )

    @nextcord.ui.button(
        label="🎵", style=nextcord.ButtonStyle.gray, custom_id="help_music", row=0
    )
    async def help_music(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="⚙️", style=nextcord.ButtonStyle.gray, custom_id="help_setup", row=0
    )
    async def help_setup(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="🤖", style=nextcord.ButtonStyle.gray, custom_id="help_bot", row=0
    )
    async def help_bot(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="🎮", style=nextcord.ButtonStyle.gray, custom_id="help_game", row=0
    )
    async def help_game(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="🛡️", style=nextcord.ButtonStyle.gray, custom_id="help_protect", row=0
    )
    async def help_protect(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="🔞", style=nextcord.ButtonStyle.gray, custom_id="help_nsfw", row=1
    )
    async def help_nsfw(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="🏠 หน้าหลัก",
        style=nextcord.ButtonStyle.primary,
        custom_id="home_menu",
        row=2,
    )
    async def home_menu(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label="❌ ปิดเมนู", style=nextcord.ButtonStyle.red, custom_id="close_menu", row=2
    )
    async def close_menu(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Help.handle_click(self, button, interaction)


class Help(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.language = translate_help.call()

    async def handle_click(
        self: HelpButton, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if interaction.user == self.Member:
            if button.custom_id == "help_music":
                embed = nextcord.Embed(
                    title="🎵 คำสั่งเล่นเพลง",
                    description=f"``{settings.COMMAND_PREFIX}musicsetup`` สร้างห้องเล่นเพลง",
                    color=0xFED000,
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)

            elif button.custom_id == "help_setup":
                embed = nextcord.Embed(
                    title="⚙️ คำสั่งตั้งค่าบอท",
                    description=f"""
``{settings.COMMAND_PREFIX}setup`` สร้างห้องเล่นเพลง
``{settings.COMMAND_PREFIX}setwelcome`` ตั้งค่าห้องเเจ้งเตือนคนเข้า
``{settings.COMMAND_PREFIX}setleave`` ตั้งค่าห้องเเจ้งเตือนคนออก
``{settings.COMMAND_PREFIX}setleave`` ตั้งค่าห้องเเจ้งเตือนคนออก
``{settings.COMMAND_PREFIX}setintroduce [#text-channel]`` ตั้งค่าห้องเเนะนําตัว ``!r ind``
``{settings.COMMAND_PREFIX}setintroduce-role give/role [@role]`` ตั้งค่ายศที่จะให้หรือลบหลังจากเเนะนําตัว
``{settings.COMMAND_PREFIX}introduce on/off`` เปิดปิดระบบเเนะนําตัว
``{settings.COMMAND_PREFIX}setframe [frame]`` ตั้งค่ากรอบเเนะนําตัว
``{settings.COMMAND_PREFIX}setverify [#text-channel]`` ตั้งค่าห้องยืนยันตัวตน ``!r vfy``
``{settings.COMMAND_PREFIX}verification on/off`` ตั้งค่าเปิด/ปิดระบบยืนยันตัวตน
``{settings.COMMAND_PREFIX}verification on/off`` ตั้งค่าเปิด/ปิดระบบยืนยันตัวตน
""",
                    color=0xFED000,
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)

            elif button.custom_id == "help_bot":
                embed = nextcord.Embed(
                    title="🤖 คําสั่งเกี่ยวกับตัวบอท",
                    description=f"""
``{settings.COMMAND_PREFIX}test`` ดูว่าบอทonline ไหม
``{settings.COMMAND_PREFIX}ping`` เช็ค ping ของบอท
``{settings.COMMAND_PREFIX}uptime`` เช็คเวลาทำงานของบอท
``{settings.COMMAND_PREFIX}botinvite`` ส่งลิงค์เชิญบอท
``{settings.COMMAND_PREFIX}botvote`` โหวตให้บอท
``{settings.COMMAND_PREFIX}credit`` เครดิตคนทําบอท
``{settings.COMMAND_PREFIX}botinfo`` ข้อมูลเกี่ยวกับตัวบอท
``{settings.COMMAND_PREFIX}support [text]`` ส่งข้อความหา support หากพบปัญหา
""",
                    color=0xFED000,
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)

            elif button.custom_id == "help_nsfw":
                embed = nextcord.Embed(
                    title="🔞 คําสั่ง nsfw",
                    description=f"**18+**\n``porn``,``gsolo``,``classic``,``pussy``,``eroyuri``,``yuri``,``solo``,``anal``,\n``erofeet``,``feet``,``hentai``,``boobs``,``tits``,``blowjob``,``lewd``,``lesbian``\n``feed``,``tickle``, ``slap``,``hug``,``smug``,``pat``,``kiss``",
                    color=0xFED000,
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)

            elif button.custom_id == "help_user":
                embed = nextcord.Embed(
                    title="🤖 คําสั่งเกี่ยวกับตัวบอท",
                    description=f"""
``{settings.COMMAND_PREFIX}rank <@Member>`` เช็คเเรงค์ของคุณหรือสมาชิก
``{settings.COMMAND_PREFIX}leaderboard`` ดูอันดับเลเวลของในเซิฟเวอร์
``{settings.COMMAND_PREFIX}ind`` เช็คเวลาทำงานของบอท
``{settings.COMMAND_PREFIX}vfy`` ยืนยันตัวตนโดย captcha
""",
                    color=0xFED000,
                )

            elif button.custom_id == "home_menu":
                embed = nextcord.Embed(
                    title="📋 เมนูช่วยเหลือ",
                    description=f"{interaction.user.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``\nกดปุ่มด้านล่างเพื่อดูคําส่งทั้งหมดของบอทได้เลยนะครับ",
                    color=0xFED000,
                )
                embed.set_image(
                    url="https://smilewinbot.web.app/assets/image/host/smilewin.gif"
                )

                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)
                
            elif button.custom_id == "help_game":
                messages = [f"`{settings.COMMAND_PREFIX}tictactoe start [@ผู้เล่นคนที่สอง]` เล่นเกม tictactoe หรือ xo",
                           f"`{settings.COMMAND_PREFIX}roulette` เริ่มเล่นเกมรูเล็ต",
                           f"`{settings.COMMAND_PREFIX}horse [จำนวนตัว] [จำนวนเงิน]` เริ่มเล่นเกม horse",
                           f"`{settings.COMMAND_PREFIX}blackjack [จำนวนเงิน]` เริ่มเกม Blackjack"]
                text = await convert_list_of_string_to_text(messages)
                    
                embed = nextcord.Embed(
                    title="🎮 คําสั่งเกี่ยวกับเกม",
                    description=text,
                    color= 0xFED000
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)
            
            elif button.custom_id == "help_protect":
                messages = [f"`{settings.COMMAND_PREFIX}scam` เพื่อดูรายระเอียดการระบบป้องกันลิ้งค์ที่ไม่ปลอดภัย"]
                text = await convert_list_of_string_to_text(messages)

                embed = nextcord.Embed(
                    title="🛡️ คําสั่งเกี่ยวระบบป้องกัน",
                    description=text,
                    color= 0xFED000
                )
                embed.set_footer(text=f"┗Requested by {interaction.user}")
                await interaction.message.edit(embed=embed)
            
            elif button.custom_id == "close_menu":
                await interaction.message.delete()
        else:
            print("ควยไรอะ")

    @commands.command()
    async def help(self, ctx: commands.Context):
        languageserver = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if languageserver is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")

        else:
            embed = nextcord.Embed(
                title="📋 เมนูช่วยเหลือ",
                description=f"{ctx.author.mention} เครื่องหมายหน้าคำสั่งคือ ``{settings.COMMAND_PREFIX}``\nกดปุ่มด้านล่างเพื่อดูคําส่งทั้งหมดของบอทได้เลยนะครับ",
                color=0xFED000,
            )
            embed.set_image(
                url="https://smilewinbot.web.app/assets/image/host/smilewin.gif"
            )
            embed.set_footer(text=f"┗Requested by {ctx.author}")
            await ctx.send(embed=embed, view=HelpButton(ctx.author))


async def convert_list_of_string_to_text(strings: list):
    text = ""
    for index,string in enumerate(strings):
        text += string
        if index != len(strings)-1:
            text += "\n"
    return text 

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))