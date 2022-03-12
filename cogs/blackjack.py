import nextcord
from nextcord.ext import commands
import random
import settings

card_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["bj"])
    async def blackjack(self, ctx: commands.Context, amount=None):

        if amount is None:
            embed = nextcord.Embed(
                title="Error",
                description=f"โปรดใส่จำนวนเงินที่จะเดิมพัน | `{settings.COMMAND_PREFIX}blackjack <amount>`",
                color=0xFED000,
            )
            return await ctx.send(embed=embed, delete_after=5)

        try:
            amount = int(amount)
        except ValueError:
            embed = nextcord.Embed(
                title="Error",
                description="จำนวนเงินต้องเป็นจำนวนเต็มเท่านั้น",
                color=0xFED000,
            )
            return await ctx.send(embed=embed, delete_after=5)

        # Check status of economy system
        guild = await settings.collection.find_one({"guild_id": ctx.guild.id})
        if guild is not None:
            status = guild["economy_system"]
            if status == "YES":
                user = await settings.collectionmoney.find_one(
                    {"guild_id": ctx.guild.id, "user_id": ctx.author.id}
                )
                if user is None:
                    embed = nextcord.Embed(
                        title=f"{ctx.author.name} ยังไม่มีบัญชี",
                        description=f"ใช้คําสั่ง {settings.COMMAND_PREFIX}openbal เพื่อเปิดใช้",
                        colour=0x983925,
                    )
                    embed.set_footer(text=f"┗Requested by {ctx.author}")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("💸")
                else:
                    current = user["wallet"]
                    currency = guild["currency"]

                    if current <= amount:
                        embed = nextcord.Embed(
                            title="Error",
                            description="จำนวนเงินของคุณไม่พอ",
                            color=0xFED000,
                        )
                        return await ctx.send(embed=embed, delete_after=5)

        # Check if the user already has a game
        game = await settings.collectionblackjack.find_one(
            {"player_id": ctx.author.id, "game": "blackjack"}
        )

        if game is not None:
            embed = nextcord.Embed(
                title="Error",
                description=f"คุณได้เริ่มเกมไปแล้ว | หากต้องการหยุดเกมที่เล่นอยู่โปรดใช้ {settings.COMMAND_PREFIX}blackjack stop",
                color=0xFED000,
            )
            return await ctx.send(embed=embed, delete_after=5)

        # Initialize variables
        while True:
            player_hand = random.sample(card_list, 2)
            dealer_hand = random.sample(card_list, 2)

            player_score = await get_score(player_hand)
            dealer_score = await get_score(dealer_hand)

            if player_score < 21 and dealer_score < 21:
                break

        # Create the embed
        embed = await Blackjack.embed_generator(
            self, player_hand, dealer_hand, first_turn=True
        )
        # Send embed
        msg = await ctx.send(embed=embed, view=Blackjack_Button(self.bot))

        # Create data for the game
        data = {
            "game": "blackjack",
            "player_id": ctx.author.id,
            "player_hand": player_hand,
            "dealer_hand": dealer_hand,
            "channel_id": ctx.channel.id,
            "amount": amount,
            "msg_id": msg.id,
        }

        # Insert data into database
        await settings.collectionblackjack.insert_one(data)

    async def embed_generator(
        self, player_hand, dealer_hand, first_turn=False, state=None, infotext=""
    ):  # state = 1 for win, 2 for lose, 3 for draw
        player_hand_text = ""
        for i in player_hand:
            player_hand_text += f"{i} "

        dealer_hand_text = ""
        for i in dealer_hand:
            dealer_hand_text += f"{i} "

        embed = nextcord.Embed(title="Blackjack", color=0xFED000)
        if state is None:
            embed.add_field(
                name="Your hand",
                value=f"{player_hand_text}\n\n Value: {await get_score(player_hand)}",
            )

            if first_turn:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand[0]} #\n\n Value: {await get_score([dealer_hand[0]])}",
                )
            else:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand_text}\n\n Value: {await get_score(dealer_hand)}",
                )
            return embed
        elif state == 1:
            embed.add_field(
                name="Game end!", value=f"คุณชนะ! | {infotext}", inline=False
            )
            embed.add_field(
                name="Your hand",
                value=f"{player_hand_text}\n\n Value: {await get_score(player_hand)}",
            )

            if first_turn:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand[0]} #\n\n Value: {await get_score([dealer_hand[0]])}",
                )
            else:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand_text}\n\n Value: {await get_score(dealer_hand)}",
                )
            return embed
        elif state == 2:
            embed.add_field(
                name="Game end!", value=f"คุณแพ้! | {infotext}", inline=False
            )
            embed.add_field(
                name="Your hand",
                value=f"{player_hand_text}\n\n Value: {await get_score(player_hand)}",
            )

            if first_turn:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand[0]} #\n\n Value: {await get_score([dealer_hand[0]])}",
                )
            else:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand_text}\n\n Value: {await get_score(dealer_hand)}",
                )
            return embed
        elif state == 3:
            embed.add_field(name="Game end!", value=f"เสมอ! | {infotext}", inline=False)
            embed.add_field(
                name="Your hand",
                value=f"{player_hand_text}\n\n Value: {await get_score(player_hand)}",
            )

            if first_turn:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand[0]} #\n\n Value: {await get_score([dealer_hand[0]])}",
                )
            else:
                embed.add_field(
                    name="Dealer's hand",
                    value=f"{dealer_hand_text}\n\n Value: {await get_score(dealer_hand)}",
                )
            return embed

    @blackjack.command()
    async def stop(self, ctx: commands.Context):
        # Check if the user already has a game
        game = await settings.collectionblackjack.find_one(
            {"player_id": ctx.author.id, "game": "blackjack"}
        )

        if game is not None:
            await settings.collectionblackjack.delete_one(
                {"player_id": ctx.author.id, "game": "blackjack"}
            )
            await ctx.send(f"Game has stopped!")
        else:
            return await ctx.send(f"You don't have a game running!")

    @blackjack.command()
    async def help(self, ctx: commands.Context):
        embed = nextcord.Embed(title="Blackjack", color=0xFED000)
        embed.add_field(
            name="Blackjack",
            value=f"Play blackjack with the bot! | {settings.COMMAND_PREFIX}blackjack",
            inline=False,
        )
        embed.add_field(
            name="Stop",
            value=f"Stop the current game | {settings.COMMAND_PREFIX}blackjack stop",
            inline=False,
        )
        await ctx.send(embed=embed)

    # It will come from Blackjack_Button
    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if button.custom_id == "hit":
            game = await settings.collectionblackjack.find_one(
                {"player_id": interaction.user.id, "game": "blackjack"}
            )
            if game is not None:
                newcard = random.sample(card_list, 1)
                game["player_hand"].append(newcard[0])
                await settings.collectionblackjack.update_one(
                    {"player_id": game["player_id"]}, {"$set": game}
                )

                # Check player win lose this turn
                # update message
                player_score = await get_score(game["player_hand"])
                dealer_score = await get_score(game["dealer_hand"])
                status, state = await Blackjack.check_win_lose_draw(
                    player_score, dealer_score
                )
                if status == "End":
                    if state == "Win":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คุณได้รับ {game['amount']*2}{currency} คงเหลือ {current + game['amount']*2:,}{currency}"

                        # updata user wallet
                        await settings.collectionmoney.update_one(
                            {
                                "guild_id": interaction.guild.id,
                                "user_id": interaction.user.id,
                            },
                            {"$set": {"wallet": current + game["amount"] * 2}},
                        )

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=1,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )

                    elif state == "Lose":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คุณเสีย {game['amount']*2}{currency} คงเหลือ {current - game['amount']:,}{currency}"

                        # updata user wallet
                        await settings.collectionmoney.update_one(
                            {
                                "guild_id": interaction.guild.id,
                                "user_id": interaction.user.id,
                            },
                            {"$set": {"wallet": current - game["amount"]}},
                        )

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=2,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )

                    elif state == "Draw":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คงเหลือ {current:,}{currency} เท่าเดิม"

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=3,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )
                else:
                    embed = await Blackjack.embed_generator(
                        self, game["player_hand"], game["dealer_hand"]
                    )
                    await Blackjack.update_message(self, embed, interaction)

        elif button.custom_id == "stand":
            game = await settings.collectionblackjack.find_one(
                {"player_id": interaction.user.id, "game": "blackjack"}
            )
            if game is not None:

                # call computer dealer playing function
                await Blackjack.computer_dealer_playing(self, game)

                # update message
                player_score = await get_score(game["player_hand"])
                dealer_score = await get_score(game["dealer_hand"])
                status, state = await Blackjack.check_win_lose_draw(
                    self, player_score, dealer_score
                )

                if status == "End":
                    if state == "Win":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คุณได้รับ {game['amount']*2}{currency} คงเหลือ {current + game['amount']*2:,}{currency}"

                        # updata user wallet
                        await settings.collectionmoney.update_one(
                            {
                                "guild_id": interaction.guild.id,
                                "user_id": interaction.user.id,
                            },
                            {"$set": {"wallet": current + game["amount"] * 2}},
                        )

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=1,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )

                    elif state == "Lose":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คุณเสีย {game['amount']*2}{currency} คงเหลือ {current - game['amount']:,}{currency}"

                        # updata user wallet
                        await settings.collectionmoney.update_one(
                            {
                                "guild_id": interaction.guild.id,
                                "user_id": interaction.user.id,
                            },
                            {"$set": {"wallet": current - game["amount"]}},
                        )

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=2,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )

                    elif state == "Draw":
                        data = await settings.collection.find_one(
                            {"guild_id": interaction.guild.id}
                        )
                        user = await settings.collectionmoney.find_one(
                            {"user_id": interaction.user.id}
                        )
                        current = user["wallet"]
                        currency = data["currency"]
                        infotext = f"คงเหลือ {current:,}{currency} เท่าเดิม"

                        embed = await Blackjack.embed_generator(
                            self,
                            game["player_hand"],
                            game["dealer_hand"],
                            state=3,
                            infotext=infotext,
                        )
                        await Blackjack.update_message(
                            self, embed, interaction, remove_view=True
                        )
                        await settings.collectionblackjack.delete_one(
                            {"player_id": interaction.user.id, "game": "blackjack"}
                        )
                else:
                    embed = await Blackjack.embed_generator(
                        self, game["player_hand"], game["dealer_hand"]
                    )
                    await Blackjack.update_message(self, embed, interaction)

    # Check win lose in player turn
    async def check_win_lose_draw(self, player_score, dealer_score):
        # check win
        if (
            player_score == 21 or dealer_score < player_score or dealer_score > 21
        ) and not (player_score > 21):
            return "End", "Win"

        # check lose:
        if (
            dealer_score > player_score or player_score > 21 or dealer_score == 21
        ) and not (dealer_score > 21):
            return "End", "Lose"

        # check draw
        if dealer_score == player_score and dealer_score < 21 and player_score < 21:
            return "End", "Draw"

        return "Continue", False

    async def computer_dealer_playing(self, game):
        dealer_score = await get_score(game["dealer_hand"])
        if dealer_score < 17:
            newcard = random.sample(card_list, 1)
            game["dealer_hand"].append(newcard[0])

    async def update_message(self, embed, interaction, remove_view=False):
        if remove_view:
            await interaction.edit(embed=embed, view=None)
        else:
            await interaction.edit(embed=embed)


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
        if card not in ["A", "J", "Q", "K"]:
            sum += int(card)
    return sum


class Blackjack_Button(nextcord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label=" Hit ",
        style=nextcord.ButtonStyle.secondary,
        custom_id="hit",
        row=0,
    )
    async def double_down(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Blackjack.handle_click(self, button, interaction)

    @nextcord.ui.button(
        label=" Stand ", style=nextcord.ButtonStyle.secondary, custom_id="stand", row=0
    )
    async def stand(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await Blackjack.handle_click(self, button, interaction)


def setup(bot):
    bot.add_cog(Blackjack(bot))
    bot.add_view(Blackjack_Button(bot))
