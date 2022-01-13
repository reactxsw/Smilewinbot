import nextcord
from nextcord.ext import commands
import settings
from utils.languageembed import languageEmbed
import random


class TicTacToe(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(name="tictactoe", aliases=["ttt","xo","ox"])
    async def tictactoe(self, ctx):
        serverlanguage = await settings.collectionlanguage.find_one({"guild_id":ctx.guild.id})
        if serverlanguage is None:
            message = await ctx.send(embed=languageEmbed.languageembed(self,ctx))
            await message.add_reaction('👍')


        # Display information about this game
        if serverlanguage == "Thai":
            pass
        elif serverlanguage == "English":
            embed = nextcord.Embed(title="Tic Tac Toe",color=0xFED000)
            embed.add_field(name="Start", value="Start the game | `tictactoe start [@player1] [@player2]`")
            embed.add_field(name="📢Note",value="""```
[] = required
/ = or
<> = optional``````
• In order for bots to use all functions, bots should have Administrator permission.
• The function cannot work in private chat.
```
""", inline=False)

    #Start command
    @tictactoe.command(name="start", aliases=["s"])
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
        
        p1 = player1.id
        p2 = player2.id
        board = [[0,0,0],
                [0,0,0],
                [0,0,0]]
        turn = random.randint(1,2)

        # Insert data into database
        data = {"guild_id":ctx.guild.id,
                "p1":p1,
                "p2":p2,
                "board":board,
                "turn":turn}
        
        await settings.collectiontictactoe.insert_one(data)
        message_id = await self.draw_board(ctx,board)
    
    async def draw_board(self,ctx,board):
        embed = nextcord.Embed(
            title="Tic Tac Toe",
            color=0xFED000

        )
        display = ""
        for i in board:
            for j in i:
                if j == 0:
                    display += "⬜ "
                elif j == 1:
                    display += "⬛ "
                elif j == 2:
                    display += "🔴 "
            display += "\n"

        

    

def setup(bot):
    bot.add_cog(TicTacToe(bot))