import asyncio
import logging
import os

import discord
import yt_dlp as youtube_dl
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'outtmpl': 'temp_music/%(title)s.%(ext)s'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class _YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

class PlayMusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wbijaj')
    async def join(self, ctx):
        try:
            if not ctx.message.author.voice:
                await ctx.send(
                    f"{ctx.message.author.name} ej, niech ktoś dołączy najpierw, nie chce tam siedzieć sam 🤔")
                return
            else:
                channel = ctx.author.voice.channel
                await channel.connect()
                logging.info(f"Bot connected with voice channel: {channel}")
        except Exception as e:
            logging.error(f"Bot cannot connected with voice channel: {channel}")

    @commands.command(name='wyjdz')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            logging.info(f"Bot disconnected with voice channel.")
        else:
            await ctx.send(f"Przecież nie siedze na czacie z Wami, to po ci mnie pingasz {ctx.message.author.name}.")

    @commands.command(name='graj')
    async def play(self, ctx, url):
        voice_client = ctx.voice_client
        if not voice_client.is_playing():
            ydl_opts = {'format': 'bestaudio', 'verbose': True}
            with youtube_dl.YoutubeDL(ydl_opts):
                filename = await _YTDLSource.from_url(url)
                voice_client.play(discord.FFmpegPCMAudio(executable=r'E:\software\mpeg\bin\mpeg.exe', source=filename))
            logging.info(f"Bot is playing music from url: {url}")
        else:
            await ctx.send("Już przecież gram! Albo mnie zastopuj !stop, albo zmień utwór !graj url  😎")
            logging.info(f"Bot is already playing music.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            logging.info(f"Bot is stop playing music.")
        else:
            await ctx.send("Przecież nic nie gram...")
            logging.info(f"Bot is not playing any music so nothing to stop.")


async def setup(bot):
    await bot.add_cog(PlayMusicCog(bot))
