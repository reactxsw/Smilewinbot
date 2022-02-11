import nextcord
from nextcord.ext import commands
import random
import settings

class Blackjack(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=["bj"])
    async def blackjack(self,ctx):
        #Initialize variables
        card_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        player_hand = random.sample(card_list,2)
        dealer_hand = random.sample(card_list,2)

        #Create embed
        embed = nextcord.Embed(title="Blackjack")
        embed.add_field(name="Your hand",value=f"{player_hand[0]} {player_hand[1]}\n\n Value: {await get_score(player_hand)}")
        embed.add_field(name="Dealer's hand",value=f"{dealer_hand[0]} #\n\n Value: {await get_score([dealer_hand[0]])}")

        #Send embed
        await ctx.send(embed=embed)

        # #Create data for the game
        # data = {
        #     "player_hand": player_hand,
        #     "dealer_hand": dealer_hand,
        #     "player_score": await get_score(player_hand),
        #     "dealer_score": await get_score(dealer_hand),
        # }

        # #Insert data into database
        # await settings.collectionblackjack.insert_one(data)


async def get_score(cards: list):
    sum = 0
    for _ in range(cards.count("A")):
        if "A" in cards:
            if "J" in cards or "Q" in cards or "K" in cards:
                sum += 11
            else:
                sum += 1

    for _ in range(cards.count("J") + cards.count("Q") + cards.count("K")):
        if "J" in cards or "Q" in cards or "K" in cards:
            sum += 10

    for card in cards:
        if card not in ["A","J","Q","K"]:
            sum += int(card)
    return sum

class Blackjack_Button(nextcord.ui.View):

    def __init__(self,bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label = " Double down ",
        style=nextcord.ButtonStyle.secondary,
        custom_id= "double_down",
        row = 0
    )
    async def double_down(self,ctx):
        pass




def setup(bot):
    bot.add_cog(Blackjack(bot))