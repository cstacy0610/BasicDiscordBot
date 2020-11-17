
import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os


#Creates bot and initializes the prefix used to input commands
intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
bot = commands.Bot(command_prefix = '!', intents = intents)

#Declares when the bot is ready to accept commands
@bot.event
async def on_ready():
    print('Bot ready, no errors.')

#Prints to console when someone joins the server
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

#Prints to console when someone leaves the server
@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

#Returns the bot's current latency to the server. Mostly used for debugging
@bot.command()
async def ping(context):
    await context.send(f'The current latency for this bot is {round(bot.latency*1000)}ms')

#Deletes a passed number of messages, including the command call, with the default deleting 1 previous message
@bot.command()
async def clear(context, amount = 2):
    await context.channel.purge(limit = amount)
    await context.send(f'{amount-1} previous messages were deleted.')

#Kicks a member of the server
@bot.command()
async def kick(context, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await context.send(f'{member} was kicked from the server. Reason: {reason}')

#Bans a member of the server
@bot.command()
async def ban(context, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await context.send(f'{member} was banned from the server. Reason: {reason}')

#Unbans a member from the server
@bot.command()
async def unban(context, *, member):
    banned_members = await context.guild.bans()
    member_name, member_nums = member.split('#')
    for ban_record in banned_members:
        user = ban_record.user
        if(user.name, user.discriminator) == (member_name, member_nums):
            await context.guild.unban(user)
            await context.send(f'{user} was unbanned from the server.')
            return

#Summons the bot into the channel the user is in
@bot.command()
async def join(context):
    channel = context.author.voice.channel
    voice = await channel.connect()
    await context.send('Bot has joined the voice channel.')


#Function for the bot to leave the voice channel
@bot.command()
async def leave(context):
    channel = context.message.author.voice.channel
    voice = get(bot.voice_clients, guild = context.guild)
    await voice.disconnect()

#Makes the bot play a song from a YouTube URL; bot must be in a channel already
@bot.command()
async def play(context, url):
    channel = context.message.author.voice.channel
    voice = get(bot.voice_clients, guild = context.guild)

    ydl_options = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'256'
        }]
    }

    with YoutubeDL(ydl_options) as ydl:
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            os.rename(file, 'song.mp3')

    voice.play(FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.05




#Links actual bot to this file using the bot token value and brings it online
bot.run('Nzc4MTM4Nzg0MTk3NjQwMjAy.X7NoNw.3iulMnnaiJ3m1jGaz1uxyCMoD80')