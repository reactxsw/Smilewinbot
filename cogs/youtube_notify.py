from utils.languageembed import languageEmbed
import settings
import nextcord
from nextcord.ext import commands
import aiohttp

class youtube_notify(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

						
	@commands.command()
	async def setyt(self, channel_Id : int, textChannelId : int):
		YoutubeCollection = await settings.db.create_collection("youtube")
		language = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if language is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        else:
            server_language = language["Language"]    
            if server_language == "Thai":
            	with aiohttp.ClientSession() as session:
	            	youtube_api_key = "AIzaSyC61rafTZL2NeAaJEHqd0lmkDHG_18aPEA"
					res = session.get(f"https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=1")
					l = res.json()
					l_videoId = l["items"][0]["id"]["videoId"]
					if channel_Id not in YoutubeCollection:
						await YoutubeCollection.insert_one(
								{
									$set: 
									{
										channel: f"https://www.youtube.com/channel/%7B{channel_Id}%7D",
										lastestVidId: f"{res}",
										notify: [
											{ctx.guild.id, int(textChannelId)}
										]
									}
								}
							)
					elif channel_Id in YoutubeCollection:
						await YoutubeCollection.update_one(
							{
								$push : {
									notify: {ctx.guild.id, textChannelId}
								}
							})

	            	channelName = f"https://www.youtube.com/channel/{channel_Id}"
	            	embed = nextcord.Embed(
	            			title=f"ตั้งค่า **{channelName}** แจ้งเตือนที่ **{fetchChannel}** ",
	            			description=f"ตั้งค่าเสร็จสมบูรณ์",
	            			color=nextcord.Colour.green()
	            		)
	            	await ctx.send(embed=embed)
			elif server_language == "English":
				with aiohttp.ClientSession() as session:
					fetchChannel = commands.fetch_channel(textChannelId)
					youtube_api_key = "AIzaSyC61rafTZL2NeAaJEHqd0lmkDHG_18aPEA"
					res = session.get(f"https://www.googleapis.com/youtube/v3/search?key={youtube_api_key}&channelId={channel_Id}&part=snippet,id&order=date&maxResults=1")
					l = res.json()
					l_videoId = l["items"][0]["id"]["videoId"]
					
	            	data = await settings.collection.find_one( {"guild_id":ctx.guild.id})
	            	embed = nextcord.Embed(
	            			title=f"Set **{channelName}** notify at **{fetchChannel}** ",
	            			description=f"Setting successfully",
	            			color=nextcord.Colour.green()
	            	)
	            	await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(youtube_notify(bot))

