import asyncio
from typing import Final

import discord
from discord.ext import commands
from discord.ext.music import MusicClient, WAVAudio, Track

from dotenv import load_dotenv
import socket, os
import threading, wave, pyaudio, pickle, struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

# Load Token from dot env

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


# play command
@bot.command()
async def play(ctx, arg1: str):
    print(f'You passed {arg1}')
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send("Đã kết nối")
        # call socket
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #  s.connect((socket.gethostname(), port))
        #  res = s.recv(1024)
        #  print(res)
        #  s.send(bytes("Play", "utf-8"))
        #  wave_file = s.recv(1024)
        # test play
        voice_client.play(discord.FFmpegPCMAudio('more than words.wav'))

    else:
        await ctx.send("Bạn không trong kênh giọng nói nào cả")


@bot.command(pass_context=True)
async def connect(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send("Đã kết nối")
    else:
        await ctx.send("Bạn không trong kênh giọng nói nào cả")


# disconnect command
@bot.command(pass_context=True)
async def disconnect(ctx):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Disconnected")


# pause command
@bot.command()
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("Không có bài hát nào đang được phát")


@bot.command()
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("Không có bài hát nào đang bị tạm dừng")


@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("Không có bài hát nào đang được phát")


bot.run(token=TOKEN)
