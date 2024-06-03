import discord
import yt_dlp
from discord.ext import commands

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voice_clients = {}
        self.yt_dl_options = {"format": "bestaudio/best"}
        self.ytdl = yt_dlp.YoutubeDL(self.yt_dl_options)
        self.volume = 1.0  # Default volume

    @commands.command()
    async def play(self, ctx, url: str):
        try:
            if ctx.author.voice and ctx.author.voice.channel:
                voice_client = await ctx.author.voice.channel.connect()
                self.voice_clients[ctx.guild.id] = voice_client
            else:
                await ctx.send("You must join a voice channel first.")
                return
        except Exception as e:
            print(f"An error occurred while joining voice channel: {e}")

        try:
            data = await self.client.loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
            song = data['url']
            player = discord.FFmpegOpusAudio(song)
            self.voice_clients[ctx.guild.id].play(player)
        except Exception as e:
            print(f"An error occurred while playing song: {e}")

    @commands.command()
    async def pause(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(f"An error occurred while pausing song: {e}")

    @commands.command()
    async def resume(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(f"An error occurred while resuming song: {e}")

    @commands.command()
    async def stop(self, ctx):
        try:
            self.voice_clients[ctx.guild.id].stop()
            await self.voice_clients[ctx.guild.id].disconnect()
        except Exception as e:
            print(f"An error occurred while stopping song: {e}")

async def setup(client:commands.Bot) -> None:
  await client.add_cog(music(client))