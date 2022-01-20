import nextcord
from nextcord.ext import commands
import settings
from utils.languageembed import languageEmbed
import random


class TicTacToe(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(aliases=["ttt","xo","ox"], invoke_without_command=True)
    async def tictactoe(self, ctx):
        serverlanguage = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
            return
        else:
            serverlanguage = serverlanguage["Language"]


        # Display information about this game
        if serverlanguage == "Thai":
            embed = nextcord.Embed(title="Tic Tac Toe", color=0xFED000)
            embed.add_field(name="Start", value=f"เริ่มเกม | `{settings.COMMAND_PREFIX} tictactoe start` [@ผู้เล่นคนที่ 1] [@ผู้เล่นคนที่2]", inline=False)
            embed.add_field(name="📢หมายเหตุ",value="""```
[] คือ ค่าที่จำเป็นต้องใส่
/ คือ หรือ
<> คือ ค่าที่จะใส่หรือไม่ใส่ก็ได้``````
• เพื่อให้บอทสามารถใช้งานได้ทุกฟังชั่นควรให้บอทมีบทบาท Administrator (ผู้ดูเเล)
• ฟังชั่นไม่สามารถทํางานในเเชทส่วนตัวได้
```
""", inline=False)
        elif serverlanguage == "English":
            embed = nextcord.Embed(title="Tic Tac Toe", color=0xFED000)
            embed.add_field(name="Start", value=f"Start the game | `{settings.COMMAND_PREFIX} fortictactoe start [@player1] [@player2]`", inline=False)
            embed.add_field(name="📢Note",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""", inline=False)
        await ctx.send(embed=embed)

    #Start the game
    @tictactoe.command(aliases=["s","play"])
    async def start(self, ctx, player1:nextcord.Member, player2:nextcord.Member):
        serverlanguage = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')

        # Check if the game is already running
        server_data = await settings.collectiontictactoe.find_one({"guild_id":ctx.guild.id})
        if server_data is not None:
            await ctx.send("The game is already starting.")
            return
        
        # Prepare data for the game
        p1 = [str(player1),player1.id]
        p2 = [str(player2),player2.id]
        board = [[0,0,0],
                [0,0,0],
                [0,0,0]]
        turn = random.randint(1,2)

        embed = await draw_board(board,turn,p1,p2)
        message = await ctx.send(embed=embed)
        # Insert data into database
        data = {"guild_id":ctx.guild.id,
                "p1":p1,
                "p2":p2,
                "board":board,
                "turn":turn,
                "channel_id":ctx.channel.id,
                "message_id":message.id}
        
        await settings.collectiontictactoe.insert_one(data)
        
        # Add reactions for recieving input
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        await message.add_reaction("5️⃣")
        await message.add_reaction("6️⃣")
        await message.add_reaction("7️⃣")
        await message.add_reaction("8️⃣")
        await message.add_reaction("9️⃣")
    
    @tictactoe.command(aliases=["end","cancel","leave","exit","quit","stopgame","endgame","cancelgame","leavegame","exitgame","quitgame"])
    async def stop(self,ctx):
        # Fetches server language
        serverlanguage = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')
        else:
            serverlanguage = serverlanguage["Language"]
        
        # Try to fetch game data from database
        server_data = await settings.collectiontictactoe.find_one({"guild_id":ctx.guild.id})
        # If isn't found = game has not started
        if server_data is None:
            # Respond to user
            if serverlanguage == "Thai":
                await ctx.send("เกมยังไม่ถูกเริ่มต้น")
            elif serverlanguage == "English":
                await ctx.send("The game is not running.")
            return

        # If game has started
        else:
            # fetch message object 
            data = await settings.collectiontictactoe.find_one({"guild_id":ctx.guild.id})
            channel = await self.bot.fetch_channel(data["channel_id"])
            message = await channel.fetch_message(data["message_id"])

            # Clear message reactions
            await message.clear_reactions()
            # Delete message
            await settings.collectiontictactoe.delete_one({"guild_id":ctx.guild.id})
            
            # Respond a message to user
            if serverlanguage == "Thai":
                await ctx.send("เกมถูกยกเลิกแล้ว")
            elif serverlanguage == "English":
                await ctx.send("The game has been stopped.")
    

    
async def draw_board(board,turn,p1,p2,is_win=False,is_draw=False):
    # Create embed
    embed = nextcord.Embed(
        title="Tic Tac Toe",
        color=0xFED000

    )

    # Create a board text for the value of the embed
    display = ""
    for i in board:
        for j in i:
            if j == 0:
                display += "⬜ | "
            elif j == 1:
                display += "❎ | "
            elif j == 2:
                display += "⭕ | "
        display += "\n"
        display += "━━━━━━━\n"

    #Display Turn
    if turn == 1:
        Turn = p1[0]
    else:
        Turn = p2[0]
    
    #Display the board
    if is_win:
        embed.add_field(name=f"{Turn} Win!", value=display, inline=False)
    elif is_draw:
        embed.add_field(name="Draw!", value=display, inline=False)
    else:
        embed.add_field(name=f"{Turn} Turn!", value=display, inline=False)
    
    # Return embed object
    return embed
        
async def recieve_input(bot,payload):
    # if It is a bot return
    if payload.user_id == bot.user.id:
        return
    # Get data from database
    data = await settings.collectiontictactoe.find_one({"guild_id":payload.guild_id})
    # If the game is not running reutrn
    if data is None:
        return
    # Get the message object
    channel = await bot.fetch_message(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    # Check Is the message is the same as the one in the database if not return
    if message.id != data["message_id"]:
        return
    # Get the player's id
    if payload.user_id == data["p1"][1]:
        player = 1
    elif payload.user_id == data["p2"][1]:
        player = 2
    else:
        # Clear the reactions
        await message.remove_reaction(payload.emoji.name,payload.member)
        return

    # Check turn is the same as the player's id
    if player != data["turn"]:
        # Clear the reactions
        await message.remove_reaction(payload.emoji.name,payload.member)
        return

    # Get the position of the player
    if payload.emoji.name == "1️⃣":
        position = 1
    elif payload.emoji.name == "2️⃣":
        position = 2
    elif payload.emoji.name == "3️⃣":
        position = 3
    elif payload.emoji.name == "4️⃣":
        position = 4
    elif payload.emoji.name == "5️⃣":
        position = 5
    elif payload.emoji.name == "6️⃣":
        position = 6
    elif payload.emoji.name == "7️⃣":
        position = 7
    elif payload.emoji.name == "8️⃣":
        position = 8
    elif payload.emoji.name == "9️⃣":
        position = 9
    else:
        # Clear the reactions
        await message.remove_reaction(payload.emoji.name,payload.member)
        return

    #                                                     row,col                row,col
    # Turn position to array | for example position = 4 => [1,0], position = 7 => [2,0]
    if position <= 3:
        position = [0,position-1]
    elif position >= 4 and position <= 6:
        position = [1,position-4]
    elif position >= 7 and position <= 9:
        position = [2,position-7]

    # Check if the position is already taken
    if data["board"][position[0]][position[1]] != 0:
        # Clear the reactions
        await message.remove_reaction(payload.emoji.name,payload.member)
        return
    # Change the board
    data["board"][position[0]][position[1]] = player
    # Check if the player won
    win = await check_win(data["board"],player)
    draw = await check_draw(data["board"])
    if win or draw:
        if win:
            await message.edit(embed=await draw_board(data["board"],data["turn"],data["p1"],data["p2"],True,False))
        elif draw:
            await message.edit(embed=await draw_board(data["board"],data["turn"],data["p1"],data["p2"],False,True))
        await message.clear_reactions()
        #Clear the database
        await settings.collectiontictactoe.delete_one({"guild_id":data["guild_id"]})
        return
    # Change the turn
    if data["turn"] == 1:
        data["turn"] = 2
    else:
        data["turn"] = 1
    
    # Edit the message
    await message.edit(embed=await draw_board(data["board"],data["turn"],data["p1"],data["p2"]))
    # Update the database
    await settings.collectiontictactoe.update_one({"guild_id":payload.guild_id}, {"$set":data})
    # Clear the reactions
    await message.remove_reaction(payload.emoji.name,payload.member)

async def check_draw(board):
    for i in board:
        for j in i:
            if j == 0:
                return False
    return True
    
async def check_win(board,turn):
    # Check horizontal
    for i in range(3):
        if board[i][0] == turn and board[i][1] == turn and board[i][2] == turn:
            return True

    # Check vertical
    for i in range(3):
        if board[0][i] == turn and board[1][i] == turn and board[2][i] == turn:
            return True
    
    # Check diagonal \
    if board[0][0] == turn and board[1][1] == turn and board[2][2] == turn:
        return True
    
    # Check diagonal (reversed) /
    if board[0][2] == turn and board[1][1] == turn and board[2][0] == turn:
        return True
    
    return False

def setup(bot):
    bot.add_cog(TicTacToe(bot))