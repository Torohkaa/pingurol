import discord
from typing import Union, Optional
from discord.ext import commands
from discord import app_commands

class misc(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Bot Ping", 
            description=f"My ping is {round(self.client.latency * 1000)}ms", 
            color=0xff0000
        )
        await ctx.send(embed=embed)

    @app_commands.command(name='ping', description='Bot latency')
    async def _ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Ping", 
            description=f"Ping is {round(self.client.latency * 1000)}ms", 
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed)

    @commands.hybrid_command(name='avatar', description='Show avatar')
    async def avatar(self, ctx, user: Optional[Union[discord.Member, discord.User]] = None):
        if not user:
            user = ctx.author

        embed = discord.Embed(colour=0x303236)
        embed.set_image(url=user.display_avatar.url)

        av_button = discord.ui.Button(label='Download', url=user.display_avatar.url, emoji='📥')
        view = discord.ui.View()
        view.add_item(av_button)

        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(810072359703937047)  # Ganti dengan ID saluran kamu
        if channel:
            embed = discord.Embed(
                title="Selamat Datang!",
                description=f"Selamat datang di server kami, {member.mention}! Kami senang kamu bergabung. Silakan baca peraturan dan nikmati waktumu di sini!",
                color=0x00ff00
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            if member.guild.icon:
                embed.set_image(url=member.guild.icon.url)
            embed.set_footer(text="Jangan lupa untuk memperkenalkan diri!")
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(810072359703937047)  # Ganti dengan ID saluran kamu
        if channel:
            embed = discord.Embed(
                title="Selamat Tinggal!",
                description=f"Kami sedih kamu pergi, {member.mention}. Kamu akan dirindukan!",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            if member.guild.icon:
                embed.set_image(url=member.guild.icon.url)
            embed.set_footer(text="Semoga kita bertemu lagi!")
            await channel.send(embed=embed)

##---------------------------------------------------------------- embed creator -----------------

async def setup(client: commands.Bot):
    await client.add_cog(misc(client))
