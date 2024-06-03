import discord
from discord.ext import commands, tasks
from googleapiclient.discovery import build
import json

class ytbnotif(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.load_config()
        self.streaming_status = {
            'live': False,
            'videoId': None
        }
        self.youtube = build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        self.check_streaming.start()

    def cog_unload(self):
        self.check_streaming.cancel()

    def load_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.YOUTUBE_API_KEY = config['YOUTUBE_API_KEY']
            self.CHANNEL_ID = config['CHANNEL_ID']
            self.NOTIFY_CHANNEL_ID = config['NOTIFY_CHANNEL_ID']

    @tasks.loop(minutes=15)  # Changed the interval for testing purposes
    async def check_streaming(self):
        await self.check_and_notify()

    async def check_and_notify(self):
        request = self.youtube.search().list(
            part='snippet',
            channelId=self.CHANNEL_ID,
            type='video',
            eventType='live'
        )
        response = request.execute()

        notify_channel = self.client.get_channel(self.NOTIFY_CHANNEL_ID)

        if notify_channel is None:
            print(f"Could not find channel with ID {self.NOTIFY_CHANNEL_ID}")
            return
    
        if response['items']:
            video = response['items'][0]
            video_id = video['id']['videoId']
            if not self.streaming_status['live'] or self.streaming_status['videoId'] != video_id:
                self.streaming_status['live'] = True
                self.streaming_status['videoId'] = video_id
                self.streaming_status['channelTitle'] = video["snippet"]["channelTitle"]
                # Notify channel
                message = f'{video["snippet"]["channelTitle"]} is live! Watch here: https://www.youtube.com/watch?v={video_id}'
                await notify_channel.send(message)
        else:
            self.streaming_status['live'] = False
            self.streaming_status['videoId'] = None

    @commands.command(name='stream')
    async def check_stream_command(self, ctx):
        """Manual command to check the streaming status."""
        await self.check_and_notify()
        if self.streaming_status['live']:
            await ctx.send(f'The channel is currently live! Watch here: https://www.youtube.com/watch?v={self.streaming_status["videoId"]}')
        else:
            await ctx.send('The channel is not currently live.')

async def setup(client:commands.Bot) -> None:
  await client.add_cog(ytbnotif(client))