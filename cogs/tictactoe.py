import nextcord
from nextcord.ext import commands
import settings
from utils.languageembed import languageEmbed
import random


class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(aliases=["ttt", "xo", "ox"], invoke_without_command=True)
    async def tictactoe(self, ctx: commands.Context):
        serverlanguage = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
            return
        else:
            serverlanguage = serverlanguage["Language"]

        # Display information about this game
        if serverlanguage == "Thai":
            embed = nextcord.Embed(title="Tic Tac Toe", color=0xFED000)
            embed.add_field(
                name="Start",
                value=f"เริ่มเกม | `{settings.COMMAND_PREFIX} tictactoe start [@ผู้เล่นคนที่2]`",
                inline=False,
            )
            embed.add_field(
                name="Stop",
                value=f"หยุดเกม | `{settings.COMMAND_PREFIX} tictactoe stop`",
                inline=False,
            )
            embed.add_field(
                name="Profile",
                value=f"ดูข้อมูลผู้เล่น | `{settings.COMMAND_PREFIX} tictactoe profile`",
                inline=False,
            )
            embed.add_field(
                name="📢หมายเหตุ",
                value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""",
                inline=False,
            )
        elif serverlanguage == "English":
            embed = nextcord.Embed(title="Tic Tac Toe", color=0xFED000)
            embed.add_field(
                name="Start",
                value=f"Start the game | `{settings.COMMAND_PREFIX} tictactoe start [@player2]`",
                inline=False,
            )
            embed.add_field(
                name="Stop",
                value=f"Stop the game | `{settings.COMMAND_PREFIX} tictactoe stop [@player2]`",
                inline=False,
            )
            embed.add_field(
                name="Profile",
                value=f"View player's profile | `{settings.COMMAND_PREFIX} tictactoe profile`",
                inline=False,
            )
            embed.add_field(
                name="📢Note",
                value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""",
                inline=False,
            )
        await ctx.send(embed=embed)

    # Start the game
    @tictactoe.command(aliases=["s", "play"])
    async def start(self, ctx: commands.Context, player2: nextcord.Member):
        serverlanguage = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
            return
        else:
            serverlanguage = serverlanguage["Language"]

        # You cannnot play with yourself
        if ctx.author.id == player2.id:
            if serverlanguage == "Thai":
                await ctx.send("คุณไม่สามารถเล่นกับตัวเองได้")
            elif serverlanguage == "English":
                await ctx.send("You cannot play with yourself")
            return

        # if player2 is bot then you cannot play with bot
        elif player2.bot:
            if serverlanguage == "Thai":
                await ctx.send("คุณไม่สามารถเล่นกับบอทได้")
            elif serverlanguage == "English":
                await ctx.send("You cannot play with bot")

        p1_game = await settings.collectiontictactoe.find_one(
            {
                "guild_id": ctx.guild.id,
                "$or": [{"p1": ctx.author.id}, {"p2": ctx.author.id}],
            }
        )
        if p1_game is not None:
            if serverlanguage == "Thai":
                await ctx.send(
                    f"คุณได้เริ่มเกมไปแล้ว กรุณาพิมพ์ `{settings.COMMAND_PREFIX} tictactoe stop` เพื่อหยุดเกม"
                )
            elif serverlanguage == "English":
                await ctx.send(
                    f"You have started the game already. Please type `{settings.COMMAND_PREFIX} tictactoe stop` to stop the game."
                )
            return

        p2_game = await settings.collectiontictactoe.find_one(
            {"guild_id": ctx.guild.id, "$or": [{"p1": player2.id}, {"p2": player2.id}]}
        )
        if p2_game is not None:
            if serverlanguage == "Thai":
                await ctx.send(f"{player2.mention} กำลังเล่นอยู่")
            elif serverlanguage == "English":
                await ctx.send(f"{player2.mention} is playing.")
            return

        # Prepare data for the game
        p1 = [str(ctx.author), ctx.author.id]
        p2 = [str(player2), player2.id]
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        turn = random.randint(1, 2)

        embed = await draw_board(board, turn, p1, p2)
        message = await ctx.send(embed=embed, view=TictactoeButton(self.bot))
        # Insert data into database
        data = {
            "guild_id": ctx.guild.id,
            "p1": p1,
            "p2": p2,
            "board": board,
            "turn": turn,
            "channel_id": ctx.channel.id,
            "message_id": message.id,
        }

        await settings.collectiontictactoe.insert_one(data)

    @tictactoe.command(
        aliases=[
            "end",
            "cancel",
            "leave",
            "exit",
            "quit",
            "stopgame",
            "endgame",
            "cancelgame",
            "leavegame",
            "exitgame",
            "quitgame",
        ]
    )
    async def stop(self, ctx: commands.Context):
        # Fetches server language
        serverlanguage = await settings.collectionlanguage.find_one(
            {"guild_id": ctx.guild.id}
        )
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self, ctx))
            await message.add_reaction("👍")
            return
        else:
            serverlanguage = serverlanguage["Language"]

        # Try to find the game in that guild that has the author as player 1 or 2
        game = await settings.collectiontictactoe.find_one(
            {
                "guild_id": ctx.guild.id,
                "$or": [{"p1.1": ctx.author.id}, {"p2.1": ctx.author.id}],
            }
        )
        if game is None:
            if serverlanguage == "Thai":
                await ctx.send(
                    f"ยังไม่มีเกมที่คุณเล่นอยู่ กรุณาพิมพ์ `{settings.COMMAND_PREFIX} tictactoe start [@ผู้เล่น2]` เพื่อเริ่มเกม"
                )
            elif serverlanguage == "English":
                await ctx.send(
                    f"You don't have any game. Please type `{settings.COMMAND_PREFIX} tictactoe start [@player2]` to start the game."
                )
            return
        else:
            # If the game is found, delete it from the database
            await settings.collectiontictactoe.delete_one(
                {
                    "guild_id": ctx.guild.id,
                    "$or": [{"p1.1": ctx.author.id}, {"p2.1": ctx.author.id}],
                }
            )
            if serverlanguage == "Thai":
                await ctx.send("ยกเลิกเกมเรียบร้อยแล้ว")
            elif serverlanguage == "English":
                await ctx.send("Canceled the game")
            message = await ctx.fetch_message(game["message_id"])
            await message.edit(
                embed=await draw_board(
                    game["board"], game["turn"], game["p1"], game["p2"], cancel=True
                ),
                view=None,
            )

    @tictactoe.command(
        aliases=[
            "level",
            "xp",
            "win",
            "wins",
            "loss",
            "losses",
            "draw",
            "draws",
            "winrate",
            "winrates",
            "win_rate",
        ]
    )
    async def profile(self, ctx: commands.Context):
        embed = nextcord.Embed(title=f"{ctx.author}", color=0xFED000)
        user_data = await settings.collectiontictactoe_user.find_one(
            {"user_id": ctx.author.id}
        )
        if user_data is None:
            embed.add_field(
                name="Please play at least one game before use this command.",
                value=f"{settings.COMMAND_PREFIX} tictactoe start [@player2]",
                inline=False,
            )
        else:
            embed.add_field(name="Wins", value=f"{user_data['wins']}", inline=True)
            embed.add_field(name="Losses", value=f"{user_data['losses']}", inline=True)
            embed.add_field(name="Draws", value=f"{user_data['draws']}", inline=True)
            embed.add_field(
                name="Total Games", value=f"{user_data['games']}", inline=False
            )
            embed.add_field(
                name="Win Rate", value=f"{user_data['win_rate']}%", inline=False
            )
            if ctx.author.avatar.url is not None:
                embed.set_thumbnail(url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


number_emoji = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


async def draw_board(board, turn, p1, p2, is_win=False, is_draw=False, cancel=False):
    # Create embed
    embed = nextcord.Embed(title="Tic Tac Toe", color=0xFED000)

    # Create a board text for the value of the embed
    display = ""
    for index, item in enumerate(board):
        if item == 0:
            display += f"{number_emoji[index]} | "

        elif item == 1:
            display += ":x: | "

        elif item == 2:
            display += ":o: | "

        if (index + 1) % 3 != 0:
            display += "|  "
            # display += ":white_large_square:  "

        if (index + 1) % 3 == 0:
            display += "\n"

        if ((index + 1) % 3 == 0) and ((index + 1) % 9 != 0):
            display += "━━━━━━━━━\n"

    # for i in board:
    #     for j in i:
    #         if j == 0:

    #             display += "⬜ | "
    #         elif j == 1:
    #             display += "❎ | "
    #         elif j == 2:
    #             display += "⭕ | "
    #     display += "\n"
    #     display += "━━━━━━━\n"

    # Display Turn
    if turn == 1:
        Turn = p1[0]
    else:
        Turn = p2[0]

    # Display the board
    if is_win:
        embed.add_field(name=f"{Turn} Win!", value=display, inline=False)
    elif is_draw:
        embed.add_field(name="Draw!", value=display, inline=False)
    elif cancel:
        embed = nextcord.Embed(
            title="Tictactoe", description="Game Ended", color=0xFED000
        )
    else:
        if turn == 1:
            embed.add_field(name=f"{Turn} Turn! | :x:", value=display, inline=False)
        else:
            embed.add_field(name=f"{Turn} Turn! | :o:", value=display, inline=False)

    # Return embed object
    return embed


class TictactoeButton(nextcord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label=" 1️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="1", row=0
    )
    async def pause_stop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 2️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="2", row=0
    )
    async def skip_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 3️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="3", row=0
    )
    async def stop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 4️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="4", row=1
    )
    async def repeat_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 5️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="5", row=1
    )
    async def loop_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 6️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="6", row=1
    )
    async def vol_up_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 7️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="7", row=2
    )
    async def vol_down_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 8️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="8", row=2
    )
    async def vol_mute_btn(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)

    @nextcord.ui.button(
        label=" 9️⃣ ", style=nextcord.ButtonStyle.secondary, custom_id="9", row=2
    )
    async def nine_button(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await recieve_input(self.bot, button, interaction)


async def recieve_input(bot, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    # if It is a bot return
    if bot.user.id == interaction.user.id:
        return
    # Get data from database
    data = await settings.collectiontictactoe.find_one(
        {
            "guild_id": interaction.guild_id,
            "$or": [{"p1": interaction.user.id}, {"p2": interaction.user.id}],
        }
    )

    # If the game is not found return
    if data is None:
        return

    # Check interaction message id and game message id
    if interaction.message.id != data["message_id"]:
        return

    # Get the player's id
    if interaction.user.id == data["p1"][1]:
        player = 1
    elif interaction.user.id == data["p2"][1]:
        player = 2

    else:
        return

    # Check turn is the same as the player's id
    if player != data["turn"]:
        return

    # Get the position of the player
    if button.custom_id == "1":
        position = 1
    elif button.custom_id == "2":
        position = 2
    elif button.custom_id == "3":
        position = 3
    elif button.custom_id == "4":
        position = 4
    elif button.custom_id == "5":
        position = 5
    elif button.custom_id == "6":
        position = 6
    elif button.custom_id == "7":
        position = 7
    elif button.custom_id == "8":
        position = 8
    elif button.custom_id == "9":
        position = 9
    else:
        return

    # Check if the position is already taken
    if data["board"][position - 1] != 0:
        return

    # Change the board
    data["board"][position - 1] = player

    # Check if the player won
    win = await check_win(data["board"], player)
    draw = await check_draw(data["board"])
    if win or draw:
        if win:
            await interaction.message.edit(
                embed=await draw_board(
                    data["board"], data["turn"], data["p1"], data["p2"], True, False
                ),
                view=None,
            )

            # Update user profile of this game
            await update_user_profile(data["turn"], data["p1"], data["p2"], True, False)

        elif draw:
            await interaction.message.edit(
                embed=await draw_board(
                    data["board"], data["turn"], data["p1"], data["p2"], False, True
                ),
                view=None,
            )

            # Update user profile of this game
            await update_user_profile(data["turn"], data["p1"], data["p2"], False, True)

        # Clear the database
        await settings.collectiontictactoe.delete_one(
            {
                "guild_id": interaction.guild_id,
                "$or": [{"p1": interaction.user.id}, {"p2": interaction.user.id}],
            }
        )
        return
    # Change the turn
    if data["turn"] == 1:
        data["turn"] = 2
    else:
        data["turn"] = 1

    # Edit the message
    await interaction.edit(
        embed=await draw_board(data["board"], data["turn"], data["p1"], data["p2"])
    )
    # Update the database
    await settings.collectiontictactoe.update_one(
        {"guild_id": interaction.guild_id}, {"$set": data}
    )


async def update_user_profile(turn, p1, p2, win, draw):

    # Get the user profiles
    p1_profile = await settings.collectiontictactoe_user.find_one({"user_id": p1[1]})
    p2_profile = await settings.collectiontictactoe_user.find_one({"user_id": p2[1]})

    # if the user is not in the database
    if p1_profile is None:
        p1_profile = {
            "user_id": p1[1],
            "username": p1[0],
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "games": 0,
            "win_rate": 0,
        }
        await settings.collectiontictactoe_user.insert_one(p1_profile)
    if p2_profile is None:
        p2_profile = {
            "user_id": p2[1],
            "username": p1[0],
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "games": 0,
            "win_rate": 0,
        }
        await settings.collectiontictactoe_user.insert_one(p2_profile)

    # Update username in case it changed
    p1_profile["username"] = p1[0]
    p2_profile["username"] = p2[0]

    # Update the user profiles
    if win:
        if turn == 1:
            p1_profile["wins"] += 1
            p2_profile["losses"] += 1
        else:
            p1_profile["losses"] += 1
            p2_profile["wins"] += 1
    elif draw:
        p1_profile["draws"] += 1
        p2_profile["draws"] += 1
    p1_profile["games"] += 1
    p2_profile["games"] += 1

    # Calculate the win rate
    p1_profile["win_rate"] = round((p1_profile["wins"] / p1_profile["games"]) * 100, 2)
    p2_profile["win_rate"] = round((p2_profile["wins"] / p2_profile["games"]) * 100, 2)

    # Update the database
    await settings.collectiontictactoe_user.update_one(
        {"user_id": p1[1]}, {"$set": p1_profile}
    )
    await settings.collectiontictactoe_user.update_one(
        {"user_id": p2[1]}, {"$set": p2_profile}
    )


async def check_draw(board):
    for i in board:
        if i == 0:
            return False
    return True


async def check_win(board, turn):

    # Check horizontal -
    for i in range(3):
        # 0 3 6    1 4 7    2 5 8
        if (
            board[i * 3] == turn
            and board[i * 3 + 1] == turn
            and board[i * 3 + 2] == turn
        ):
            return True

    # Check vertical |
    for i in range(3):
        # 0 1 2    3 4 5    6 7 8
        if board[i] == turn and board[i + 3] == turn and board[i + 6] == turn:
            return True

    # Check diagonal \
    if board[0] == turn and board[4] == turn and board[8] == turn:
        return True

    # Check diagonal /
    if board[2] == turn and board[4] == turn and board[6] == turn:
        return True

    return False


def setup(bot):
    bot.add_cog(TicTacToe(bot))
    bot.add_view(TictactoeButton(bot))
