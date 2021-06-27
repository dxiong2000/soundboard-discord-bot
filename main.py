import discord

# gets secret key
bot_token = ''
with open('./secret.txt', 'r') as secret:
    for line in secret:
        bot_token = line

# sets up bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)



def getErrorEmbed(desc):
    """
    Generates a Discord error embedded message

    Args:
        desc (str): String for error message

    Returns:
        Embed: Error embed
    """
    embed = discord.Embed(
        title = 'Soundboard Error',
        description = desc,
        colour = discord.Colour.red()
    )
    embed.set_footer(text='Type !help for a list of commands.')
    return embed


@client.event
async def on_ready():
    """
    Prints "Logged on as <bot name>!" on startup.
    """
    print(f'Logged on as {client.user}!')

@client.event
async def on_message(message):
    """
    Parses commands sent to bot
    Args:
        message (Message): Discord API Message object (https://discordpy.readthedocs.io/en/stable/api.html#message)
    """
    
    # ignore messages from the bot and messages with no content
    if message.author == client.user or len(message.content) == 0 or message.channel.name != 'soundboard':
        return
    
    user = message.author
    msg = message.content
    
    if msg.startswith('!play'): # play a sound clip
        msg = msg[5:]
        
        # selects soundclip and plays it
        if len(msg) > 0 and msg[0] == ' ': # input validation
            soundclip_name = msg[1:]
            soundclip_file = soundclip_name + '.mp3'
            print(soundclip_file)
            
            
        else:
            await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('Wrong usage of !play.\nCorrect usage: !play <clip name>.'))
            return
        
    
    

client.run(bot_token)
        