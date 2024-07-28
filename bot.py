import os, discord, json
from discord import app_commands
from dotenv import load_dotenv
import commands.games as games
import commands.moderation as mod

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
connected = False
log_channel:discord.TextChannel = None

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1048911119584084018))
    print(f"We have logged in as {client.user}")

    # load counter data
    counter_file = open("saves/counter.json", "r")
    count = json.loads(counter_file.read())
    counter_file.close()
    global counter_manager
    counter_manager = games.Counter(count["channel"], count["value"], count["max"])

    # load mod log data
    log_file = open("saves/moderation.json", "r")
    file_cont = log_file.read()
    log_file.close()
    if (len(file_cont) > 0):
        global log_channel
        log_channel = client.get_channel(json.loads(file_cont)["log_channel"])

    global connected
    connected = True

@client.event
async def on_disconnect():
    print("disconnecting")
    if connected and counter_manager:
        await counter_manager.save()
        

@client.event
async def on_message(message: discord.Message): 
    if message.author != client.user:
        # check for the counter game
        await counter_manager.counter(message)

@client.event
async def on_audit_log_entry_create(entry:discord.AuditLogEntry):
    if log_channel != None:
        await mod.log(client, entry, log_channel)

@tree.command(
        name="quit",
        guild=discord.Object(id=1048911119584084018)
)
async def exit(interaction: discord.Interaction):
    """disconnects the bot
    """    
    await interaction.response.send_message("Bot now shutting down")
    await client.close()


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
    result = games.rps(choice.upper());
    if result[0] == 0:
        await interaction.response.send_message(f'I chose {result[1].lower()}, we tied')
    elif result[0] > 0:
        await interaction.response.send_message(f"I chose {result[1].lower()}, I win")
    else:
        await interaction.response.send_message(f'I chose {result[1].lower()}, you win')

@tree.command(
    name="counter_setup",
    guild=discord.Object(id=1048911119584084018)
)
async def counter_setup(interaction: discord.Interaction, channel: str):
    """setup for the counter game, resets current game if there is one

    Args:
        interaction (discord.Interaction): _description_
        channel (str): the ID of the channel the game will be played in (must turn on developer mode to see ID)
    """
    global counter_manager
    counter_manager = games.Counter(channel)
    if counter_manager != None:
        await interaction.response.send_message(f"Counter has been set up in #{client.get_channel(counter_manager.channel).name}")
        
@tree.command(
    name="counter_info",
    guild=discord.Object(id=1048911119584084018)
)
async def counter_info(interaction:discord.Interaction):
    """displays info about the current counter game
    """    
    if "counter_manager" in globals():
        await interaction.response.send_message(f"Current streak: {counter_manager.value} \nMax streak: {counter_manager.max}")
    else:
        await interaction.response.send_message('Counter not initialized, use "/counter_setup" to start it')

@tree.command(
    name="log_setup",
    guild=discord.Object(id=1048911119584084018)
)
async def log_setup(interaction:discord.Interaction, channel_id:str):
    """setup moderation logging

    Args:
        channel_id (str): the channel to send logs to
    """
    try:
        channel_id = int(channel_id)
    except ValueError:
        interaction.response.send_message("Channel ID is not valid, please try again")
        return
    # check if channel is a valid text channel
    if client.get_channel(channel_id) != None and client.get_channel(channel_id).type == discord.ChannelType.text:
        global log_channel
        log_channel = client.get_channel(channel_id)
        # store channel in file
        m = open("saves/moderation.json", "w")
        m.write(json.dumps({"log_channel": str(channel_id)}))
        m.close()
        await interaction.response.send_message(f"log has been set up in #{log_channel.name}")
    else:
        await interaction.response.send_message("Channel could not be found, log has not been set up")


client.run(TOKEN)
