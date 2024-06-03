import discord, config
from discord.ext import commands
from discord.ui import View, Select


class HelpSelect(Select):
    def __init__(self, client: commands.Bot):
        options = [
            discord.SelectOption(
                label=cog_name,
                description=cog.__doc__ if cog.__doc__ else "No description"
            ) for cog_name, cog in client.cogs.items() if cog_name != 'Jishaku'
        ]
        
        super().__init__(placeholder="Choose a category", options=options)
        self.client = client

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.client.get_cog(self.values[0])
        if not cog:
            return

        commands_mixer = []
        for command in cog.walk_commands():
            commands_mixer.append(command)

        for command in cog.walk_app_commands():
            commands_mixer.append(command)

        embed = discord.Embed(
            title=f"{cog.__cog_name__} Commands",
            description='\n'.join(
                f"**{command.name}**: `{command.description}`" if command.description else f"**{command.name}**"
                for command in commands_mixer
            )
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='help', description='Show list of commands')
    async def help_util(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Help command",
            description="This is a help command."
        )
        view = View()
        view.add_item(HelpSelect(self.client))
        await ctx.send(embed=embed, view=view)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(utils(client))
