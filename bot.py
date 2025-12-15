import json
import random
import discord
from discord.ext import commands
from discord import ui

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["DISCORD_TOKEN"]
BOT_ID = config["DISCORD_BOT_ID"]

bot = commands.Bot(
    command_prefix=None,
    help_command=None,
    is_case_insensitive=True,
    intents=discord.Intents.all(),
)

class VerifiedView(ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("This isn't your game! Run /guess to start your own.", ephemeral=True)
            return False
        return True

class CategoryButton(ui.Button):
    def __init__(self, label):
        styles = [
            discord.ButtonStyle.primary,
            discord.ButtonStyle.success,
            discord.ButtonStyle.danger,
            discord.ButtonStyle.secondary
        ]
        random_style = random.choice(styles)
        super().__init__(label=label, style=random_style)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected {self.label}", ephemeral=True)

@bot.event
async def on_ready():
    print("Ready!")
    await bot.tree.sync()

@bot.tree.command(
    name="guess",
    description="Guess the song from the lyrics. Requires spotify oauth connection.",
)
async def guess(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎵 Guess the Song",
        description="Select a Mode below:",
        color=discord.Color.green()
    )
    
    view = VerifiedView(author=interaction.user)

    categories = ["Artist", "Album", "Liked Songs", "Playlist", "Trending Songs"]

    for category in categories:
        view.add_item(CategoryButton(label=category))
    
    await interaction.response.send_message(embed=embed, view=view)

bot.run(TOKEN)