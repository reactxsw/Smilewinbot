import discord

class languageEmbed():
    def languageembed(self , ctx):
        embed = discord.Embed(
            title = "Language setting / ตั้งค่าภาษา",
            description = "```คุณต้องตั้งค่าภาษาก่อน / You need to set the language first```" + "\n" + "/r setlanguage thai : เพื่อตั้งภาษาไทย" + "\n" + "/r setlanguage english : To set English language"

        )
        embed.set_footer(text=f"┗Requested by {ctx.author}")
        return embed 