import discord
import os
import ctypes
import ctypes.util

# gets secret key
bot_token = ''
with open('./secret.txt', 'r') as secret:
    for line in secret:
        bot_token = line

# sets up bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)
a = ctypes.util.find_library('opus')
b = discord.opus.load_opus(a)
print(discord.opus.is_loaded())



def getFileList():
    """
    Gets list of names of sound files
    
    Returns:
        [str]: names of sound files
    """
    return os.listdir('./clips/')

def getErrorEmbed(desc):
    """
    Generates a error embedded message

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
    Generates a help embedded message

    Returns:
        Embed: Help embed
    """
    embed = discord.Embed(
        title = 'Soundboard Help',
        colour = discord.Colour.orange()
    )
    embed.add_field(name='!play <clip name>', value='Play a clip from the soundboard.', inline=False)
    embed.add_field(name='!add', value='Type !add and upload a .mp3 file in the same message to add a new sound clip.', inline=False)
    embed.add_field(name='!list', value='List all available sound clips.', inline=False)
    return embed

def getListEmbed(file_list):
    """
    Generates an embedded message containing a list of sound files

    Args:
        file_list ([str]): list of sound file names

    Returns:
        Embed: embedded message
    """
    embed = discord.Embed(
        title = 'Sound Clips',
        colour = discord.Colour.blue()
    )
    for f in file_list:
        embed.add_field(name=f[:-4], value=f'!play {f[:-4]}', inline=False)
    return embed

def getAddSuccessEmbed(filename):
    """
    Generates a !add success embedded message

    Args:
        filename (str): name of file added
        
    Returns:
        Embed: success embed
    """
    embed = discord.Embed(
        title = 'Add Success',
        description = f'Added sound clip: {filename}',
        colour = discord.Colour.green()
    )
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
            
            if not user.voice or not user.voice.channel:
                await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('You must be in a voice channel to use this command.'))
                return
                
            channel = user.voice.channel

            try:
                if soundclip_file in getFileList():
                    # https://discordpy.readthedocs.io/en/stable/api.html#voice-related
                    
                    voice = await channel.connect()
                    voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg/ffmpeg-4.4-amd64-static/ffmpeg", source=f'./clips/{soundclip_file}'), after=lambda e: print(f'Played {soundclip_file} in channel {channel.name}', e))
                   
                    while voice.is_playing(): # while the sound clip is still playing, dont leave the voice channel
                        pass
                    await voice.disconnect()
                    voice.cleanup()
                else:
                    await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed(f'The clip "{soundclip_name}" does not exist.\nUse !list to see available sound clips.'))
                    return
            except discord.errors.ClientException:
                print("Bot is already in a voice channel.")
            return         
        else:
            await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('Wrong usage of !play.\nCorrect usage: !play <clip name>.'))
            return
    elif msg.startswith('!add'): # feature to add new clips
        # https://discordpy.readthedocs.io/en/stable/api.html#attachment
        
        msg = msg[4:]
        
        if len(msg) == 0 and len(message.attachments) == 1: # make sure there is an attachment with the message
            if message.attachments[0].filename[-4:] == '.mp3': # only .mp3 files
                if message.attachments[0].filename in getFileList():
                    await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('File name already in use. Change the file name and try again.'))
                    return
                
                file = message.attachments[0]
                
                try:
                    await file.save(fp=f'./clips/{message.attachments[0].filename}')
                except:
                    await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('File upload failed, please try again.'))
                    return
                
                await message.channel.send(f'{user.mention}\n', embed=getAddSuccessEmbed(message.attachments[0].filename[:-4]))
                return
            else:
                await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('Unsupported file format. Please only upload .mp3 files.'))
                return
        else:
            await message.channel.send(f'{user.mention}\n', embed=getErrorEmbed('Wrong usage of !add.\nType !add and upload a .mp3 file in the same message.'))
            return
    elif msg.startswith('!list'): # print a list of sound files
        await message.channel.send(f'{user.mention}\n', embed=getListEmbed(getFileList()))
        return
    elif msg.startswith('!help'): # help menu
        await message.channel.send(f'{user.mention}\n', embed=getHelpEmbed())
        return
        

client.run(bot_token)
        
