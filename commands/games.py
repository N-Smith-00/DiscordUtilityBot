import discord
import random

def rps(interaction: discord.Interaction, player_choice):
    com_choice = random.choice(['ROCK', 'PAPER', 'SCISSORS'])
    if com_choice == player_choice:
        return (0, com_choice)
    
    win = (1, com_choice)
    loss = (-1, com_choice)
    
    match player_choice:
        case 'ROCK':
            if com_choice == 'PAPER':
                return win
            return loss
        case 'PAPER':
            if com_choice == 'SCISSORS':
                return win
            return loss
        case 'SCISSORS':
            if com_choice == 'ROCK':
                return win
            return loss
        
def counter_setup(interaction: discord.Interaction, channel):
    pass
        
class Counter:
    def __init__(self, channel, guild, start=0) -> None:
        self.channel = channel
        self.guild = guild
        self.value = start
    
    async def counter(self, message: discord.Message):
        """main logic for the counter game

        Args:
            message (discord.Message): the message being evaluated
        """        
        if message.channel == self.channel:
            try:
                num = int(message.content.strip())
            except ValueError:
                await message.channel.send(f"{message.author.name} sent {message.content.strip()} which is not a valid number, resetting the counter to 0")
                self.value = 0
                exit()
            
            if num == self.value + 1:
                self.value += 1
                exit()
            else:
                await message.channel.send(f"that was the wrong number, resetting the counter to 0")
                self.value = 0
                exit()
    