from urllib import response

from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands
import aiohttp

class youtube_notify(commands.Cog):
	def __init__(self, bot: commands.AutoShardedBot):
		self.bot = bot

						
	@commands.command()
	async def setyt(self, ctx , channel_url: str, textchannel : nextcord.TextChannel = None):
		channel_Id = channel_url.split("/")[2]
		language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
		if language is None:
			message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
			await message.add_reaction('👍')

		else:
			server_language = language["Language"]    

			youtube_data = await settings.collectionyoutube.find_one({"Youtube":channel_url})
			if server_language == "Thai":
				try:
					async with aiohttp.ClientSession() as session:
						async with session.get(f"https://www.googleapis.com/youtube/v3/search?key={settings.youtubeapi}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=1") as r:
							response = await r.json()
						
							l_videoId = response["items"][0]["id"]["videoId"]
							if youtube_data is None:

								data = {
									"Youtube":channel_url,
									"Lastest_video ":l_videoId,
									"Notify":[]
										}
								data["Notify"].append({
									"guild_id":ctx.guild.id,
									"text_channel_id": textchannel.id
								})

								await settings.collectionyoutube.insert_one(data)

							else:

								if any(ctx.guild.id in d.values() for d in youtube_data['Notify']):
									for element in youtube_data["Notify"]:
										if ctx.guild.id in element.values():
											index = youtube_data["Notify"].index(element)
											if element["text_channel_id"] == textchannel.id:
												return

											else:
												await settings.collectionyoutube.update_one({"Youtube":channel_url , f"Notify.guild_id":element["guild_id"]},{"$set":{"Notify.$.text_channel_id":textchannel.id}})		
								
								else:			
									await settings.collectionyoutube.update_one({"Youtube":channel_url}, {'$push': {'Notify': {"guild_id":ctx.guild.id,"text_channel_id": textchannel.id}}})
				except Exception as e:
					print(e)




				channelName = f"https://www.youtube.com/channel/"
				embed = nextcord.Embed(
						title=f"ตั้งค่า **{channelName}** แจ้งเตือนที่ **{textchannel.mention}** ",
						description=f"ตั้งค่าเสร็จสมบูรณ์",
						color=nextcord.Colour.green()
					)
				await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(youtube_notify(bot))

