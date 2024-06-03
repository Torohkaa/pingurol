import discord
from discord.ext import commands
import json
import time
import platform
from typing import Literal
from colorama import Back, Fore, Style

class Client(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='.', intents=discord.Intents().all())
    self.cogslist = ["utils", "crypto", "misc","ytbnotif","music","waifu","automod"]

  async def on_ready(self):
    print(" Logged in as " + self.user.name)
    activity = discord.Activity(type=discord.ActivityType.listening, name='spotify', state='Relaxing @/playing Sopotipy')
    await client.change_presence(activity=activity)
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))   
    synced = await self.tree.sync()
    print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

  async def setup_hook(self):
    for ext in self.cogslist:
      await self.load_extension("Cogs."+ext)

with open('config.json', 'r') as f: 
  TOKEN = json.load(f)['TOKEN']

client = Client()
client.remove_command('help')

@commands.is_owner()
@client.tree.command(name="reload", description="Reloads a Cog Class")
async def reload(interaction: discord.Interaction, cog:Literal["Utils", "Crypto", "Misc","Ytbnotif","Music","Waifu","automod"]):
  try:
    await client.reload_extension(name="Cogs."+cog.lower())
    await interaction.response.send_message(f"Successfully reloaded **{cog}.py**")
  except Exception as e:
    await interaction.response.send_message(f"Failed! Could not reload this cog class. See error below\n```{e}```")


@client.event
async def on_message(message):
    # Skip jika pesan dikirim oleh bot sendiri
    if message.author == client.user:
        return

    # Periksa setiap attachment dalam pesan
    for attachment in message.attachments:
        # Periksa apakah attachment adalah gambar
        if attachment.height is not None:
            # Reaction yang ingin ditambahkan, misalnya '👍'
            reaction = '🗿'

            # Tambahkan reaction ke pesan
            await message.add_reaction(reaction)

    # Teruskan pesan ke command handler jika diperlukan
    await client.process_commands(message)



client.run(TOKEN)   