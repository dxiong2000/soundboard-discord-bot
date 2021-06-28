import discord
import os

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

def getHelpEmbed():
    """
    Generates a Discord help embedded message

    Returns:
        Embed: Help embed
    """
    embed = discord.Embed(
        title = 'Soundboard Help',
        colour = discord.Colour.orange()
    )
    embed.add_field(name='!play <clip name>', value='Play a clip from the soundboard.', inline=False)
    embed.add_field(name='!list', value='List all available sound clips.', inline=False)
    return embed

def getListEmbed(file_list):
    embed = discord.Embed(
        title = 'Sound Clips',
        colour = discord.Colour.green()
    )
    for f in file_list:
        embed.add_field(name=f[:-4], value=f'!play {f[:-4]}', inline=False)
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
    https://discordpy.readthedocs.io/en/stable/api.html#discord.VoiceClient.play
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
            
            if not user.voice or not user.voice.channel:
                await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('You must be in a voice channel to use this command.'))
                return
                
            channel = user.voice.channel

            try:
                voice = await channel.connect()
                voice.play(discord.FFmpegPCMAudio(executable="C:/FFmpeg/ffmpeg/ffmpeg.exe", source=f'./clips/{soundclip_file}'), after=lambda e: print(f'Played {soundclip_file}', e))
                while voice.is_playing():
                    pass
                await voice.disconnect()
                voice.cleanup()
            except discord.errors.ClientException:
                print("Bot is already in a voice channel.")
            
        else:
            await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('Wrong usage of !play.\nCorrect usage: !play <clip name>.'))
            return
    elif msg.startswith('!list'):
        file_list = os.listdir('./clips/')
        await message.channel.send(f'{user.mention}\n', embed=getListEmbed(file_list))
        return
    elif msg.startswith('!help'):
        await message.channel.send(f'{user.mention}\n', embed=getHelpEmbed())
        return
        

client.run(bot_token)
        