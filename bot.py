import os, discord
from discord import app_commands
from dotenv import load_dotenv

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

@tree.command(
    name="hello",
    description="replies with hello",
    guild=discord.Object(id=1048911119584084018)
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.display_name}")

client.run(TOKEN)
