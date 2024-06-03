import discord
import requests
from aiohttp import ClientSession
from discord.ext import commands

class waifu(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


## hentai -------------------------------------------------
    async def getHentai(self, tag):
        async with ClientSession() as resp:
            async with resp.get(f'https://api.waifu.im/search?included_tags=hentai') as response:
               data = await response.json()
        if data['images']:
            anime_data = data['images'][0]
            url = anime_data['url']
            source = anime_data.get('source', 'Unknown')
            description = anime_data.get('description', 'A female anime/manga character.')
            return url, source, description
        else:
            return None, None, None
    

    @commands.command(name='hentai')
    async def hentai(self, ctx):
        anime_url, source, description = await self.getHentai('hentai')
        if anime_url:
            embed = discord.Embed()
            embed.set_image(url=anime_url)
            embed.add_field(name="Source", value=source, inline=False)
            embed.add_field(name="Description", value=description, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't find any anime with the specified tag.")


## anime ---------------------------------------------------------------

    async def getWaifu(self, tag):
        async with ClientSession() as resp:
            async with resp.get(f'https://api.waifu.im/search?included_tags=waifu') as response:
               data = await response.json()
        if data['images']:
            anime_data = data['images'][0]
            url = anime_data['url']
            source = anime_data.get('source', 'Unknown')
            description = anime_data.get('description', 'A female anime/manga character.')
            return url, source, description
        else:
            return None, None, None
    
    @commands.command(name='anime')
    async def anime(self, ctx):
        anime_url, source, description = await self.getWaifu('anime')
        if anime_url:
            embed = discord.Embed()
            embed.set_image(url=anime_url)
            embed.add_field(name="Source", value=source, inline=False)
            embed.add_field(name="Description", value=description, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't find any anime with the specified tag.")

## milf--------------------------------------------------------------------------------------------------------
    async def getMilf(self, tag):
        async with ClientSession() as resp:
            async with resp.get(f'https://api.waifu.im/search?included_tags=milf') as response:
               data = await response.json()
        if data['images']:
            anime_data = data['images'][0]
            url = anime_data['url']
            source = anime_data.get('source', 'Unknown')
            description = anime_data.get('description', 'A female anime/manga character.')
            return url, source, description
        else:
            return None, None, None

    @commands.command(name='milf')
    async def milf(self, ctx):
        anime_url, source, description = await self.getMilf('milf')
        if anime_url:
            embed = discord.Embed()
            embed.set_image(url=anime_url)
            embed.add_field(name="Source", value=source, inline=False)
            embed.add_field(name="Description", value=description, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Couldn't find any anime with the specified tag.")

##---------------------------------------------------------------------------------------------------------


async def setup(client:commands.Bot) -> None:
  await client.add_cog(waifu(client))