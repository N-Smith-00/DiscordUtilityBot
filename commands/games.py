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