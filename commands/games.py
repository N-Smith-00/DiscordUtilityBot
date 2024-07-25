import discord, random, json


def rps(player_choice):
    """main logic for rock paper scissors

    Args:
        player_choice (str): the player's move

    Returns:
        tuple(int, str): a tuple with the game result and the computer's move
    """    
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
        
class Counter:
    def __init__(self, channel, start=0, max=0) -> None:
        self.channel = int(channel)
        self.value = start
        self.max = max
    
    async def counter(self, message: discord.Message):
        """main logic for the counter game

        Args:
            message (discord.Message): the message being evaluated
        """        
        if message.channel.id == self.channel:
            try:
                num = int(message.content)
            except ValueError:
                await message.channel.send(f"{message.author.name} sent {message.content.strip()} which is not a valid number, resetting the counter to 0")
                self.value = 0
                return
            
            if num == self.value + 1:
                self.value += 1
                if self.value > self.max:
                    self.max = self.value
                return
            else:
                await message.channel.send(f"that was the wrong number, resetting the counter to 0")
                self.value = 0
                return
    
    async def save(self):
        """saves the current counter game to a json file (to be used on disconnect)
        """        
        rep = {
            "channel": self.channel,
            "value": self.value,
            "max": self.max
        }
        file = open("saves/counter.json", "w")
        file.write(json.dumps(rep))
        file.close()
        
    