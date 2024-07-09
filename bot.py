import os, discord
from discord import app_commands
from dotenv import load_dotenv
import commands.games as games

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
# needed for message event (not nessecary yet)
# intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1048911119584084018))
    print(f"We have logged in as {client.user}")

# regular message event (not nessecary yet)
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

# basic hello command
@tree.command(
    name="hello",
    description="replies with hello",
    guild=discord.Object(id=1048911119584084018)
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.display_name}")

# game commands
@tree.command(
    name="rock_paper_scissors",
    guild=discord.Object(id=1048911119584084018)
)
async def rps(interaction: discord.Interaction, choice: str):
    """PLays a game of rock paper scissors

    Args:
        choice : your move (rock, paper, or scissors)
    """    
    if not (choice.upper() in ['ROCK', 'PAPER', 'SCISSORS']):
        await interaction.response.send_message(f'"{choice}" is not an option, try playing again')
    result = games.rps(interaction, choice.upper());
    if result[0] == 0:
        await interaction.response.send_message(f'I chose {result[1].lower()}, we tied')
    elif result[0] > 0:
        await interaction.response.send_message(f"I chose {result[1].lower()}, I win")
    else:
        await interaction.response.send_message(f'I chose {result[1].lower()}, you win')


client.run(TOKEN)
