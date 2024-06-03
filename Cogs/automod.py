import discord, config
from discord.ext import commands
import random

class automod(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.kata_kasar = ["mmek", "anjeng", "ajg","asu", "kntol", "anjing","ngentod", "ngntd", "asw"]
        self.subscribe = ["youtube"]
        self.nsfw = ["hentai","bkep","xnxx", "sange", "bokep", "bkp"]
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if any(word in message.content.lower() for word in self.kata_kasar):
            await message.channel.send("Tolong hindari penggunaan bahasa yang tidak pantas.")
        elif any(word in message.content.lower() for word in self.subscribe):
            await message.channel.send(random.choice(["```Jangan lupa subrek & like```"]))
        elif any(word in message.content.lower() for word in self.nsfw):
            await message.channel.send(random.choice(["!ihhh sangean"]))
            

async def setup(client:commands.Bot) -> None:
  await client.add_cog(automod(client))
