import nextcord# pip install nextcord.py
import aiohttp
import urllib

class InteractiveView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.problem = ""

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "1"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "2"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "3"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="+", row=0)
    async def plus(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "+"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "4"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "5"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "6"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="/", row=1)
    async def divide(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
            self.problem += "/"
            await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "7"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "8"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "9"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, label="*", row=2)
    async def multiply(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "*"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "."
        await interaction.message.edit(content=f"```\n{self.problem}\n```")

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.problem += "0"
        await interaction.message.edit(content=f"```\n{self.problem}\n```")
