import discord
import requests
from discord.ext import commands

class prices(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


    API_KEY = '07f3b329-8019-44b8-bd63-a9c436b6a66f'

    # Fungsi untuk mendapatkan data harga kripto dalam Rupiah (IDR) dari API CoinMarketCap
    def get_crypto_price(self, symbol):
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        parameters = {
            'symbol': symbol.upper(),
            'convert': 'IDR'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.API_KEY,
        }

        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()

        if 'data' in data:
            crypto_data = data['data'][symbol.upper()]
            price = crypto_data['quote']['IDR']['price']
            return price
        else:
            return None

    @commands.hybrid_command(name='price',  description='Symbol mata uang cryto')
    async def price(self, ctx, symbol):
        try:
            price = self.get_crypto_price(symbol)
            if price:
                embed = discord.Embed(title="")
                embed.set_thumbnail(
                url="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmZiZDEyeDQxdWszNmlvcmZuOGg5cWFvbjF5cThndWMyNGJpejRrcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/veHIwhDRl780wT2XfC/giphy.gif")  # Ganti URL dengan URL logo kripto yang sesuai
                embed.set_author(name="✨ CryptoBot ✨")
                embed.add_field(name=f"```{symbol.upper()} price :```", value=f"```- Rp {price:,.2f}```", inline=True)
                embed.set_footer(text="Information requested by : ryco ")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'Gagal mendapatkan harga {symbol.upper()} atau {symbol.upper()} tidak valid.')
        except Exception as e:
            print(e)
            await ctx.send('Terjadi kesalahan saat memproses perintah.')


async def setup(client:commands.Bot) -> None:
  await client.add_cog(prices(client))