import os
import pickle
import socket
import struct
from pathlib import Path
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv

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


def get_song_list():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))
    msg = s.recv(1024)
    print(msg)
    s.send(bytes("List", "utf-8"))
    res = s.recv(1024)


def search_song(arg: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    msg = s.recv(1024)
    print(msg)
    s.send(bytes("Search", "utf-8"))
    s.send(bytes(arg, "utf-8"))
    res = s.recv(1024).decode("utf-8")
    if res == '404':
        return False
    return True


def audio_stream(arg: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    msg = s.recv(1024)
    print(msg)
    s.send(bytes("Play", "utf-8"))
    s.send(bytes(arg, "utf-8"))
    data = b""
    data2 = Path('./stream/' + 'streaming_file' + '.mp3')
    payload_size = struct.calcsize("Q")
    # stream = open("stream/test2.mp3", 'wb')
    while True:
        try:
            while len(data) < payload_size:
                packet = s.recv(4 * 1024)  # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += s.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            # stream.write(frame)
            data2.write_bytes(frame)
            s.send(b"close")
        except:

            break

    s.close()
    print('Audio Created')
    return True


song_list = []


@bot.event
async def on_ready():
    print('Bot is ready')


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


# play command
@bot.command(pass_context=True)
async def play(ctx, arg1: str):
    print(f'You passed {arg1}')
    voice_client = ctx.guild.voice_client
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        # voice_client = await channel.connect()
        if voice_client.is_playing():
            voice_client.stop()
        if search_song(arg1):
            audio_stream(arg1)
            voice_client.play(discord.FFmpegPCMAudio("./stream/streaming_file.mp3"))
        else:
            await ctx.send(f"Không tìm thấy bài hát: {arg1}")
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
    await ctx.send("Đã ngắt kết nối")
    if os.path.exists("./stream/streaming_file.mp3"):
        os.remove("./stream/streaming_file.mp3")


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
