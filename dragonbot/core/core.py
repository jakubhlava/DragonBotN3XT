import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption
from dragonbot import guild_ids, __version__
from dragonbot.loader import Loader
import subprocess

class Core(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.version = "1.0"
        print(f"N3XT Core v{self.version} Loaded")

    @slash_command(guild_ids=guild_ids, description="Loads plugin")
    async def load(self, interaction: Interaction,
                   plugin_name: str = SlashOption(description="Name of plugin", required=True, autocomplete=True,
                                                  autocomplete_callback=Loader.unloaded_autocomplete)):
        status = await Loader.load(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` loaded!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` cannot be loaded!")

    @slash_command(guild_ids=guild_ids, description="Unloads plugin")
    async def unload(self, interaction: Interaction,
                     plugin_name: str = SlashOption(description="Name of plugin", required=True, autocomplete=True,
                                                    autocomplete_callback=Loader.loaded_autocomplete)):
        status = Loader.unload(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` unloaded!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` cannot be unloaded!")

    @slash_command(guild_ids=guild_ids, description="Reloads plugin")
    async def reload(self, interaction: Interaction,
                     plugin_name: str = SlashOption(description="Name of plugin", required=True, autocomplete=True,
                                                    autocomplete_callback=Loader.loaded_autocomplete)):
        status = Loader.reload(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` reloaded!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` cannot be reloaded!")

    @slash_command(guild_ids=guild_ids, description="Rediscovers installed plugins")
    async def rediscover(self, interaction: Interaction):
        Loader.discover()
        await interaction.send("Plugins were rediscovered!")

    @slash_command(guild_ids=guild_ids, description="Shows bot info")
    async def info(self, interaction: Interaction):
        embed = nextcord.Embed(color=0xab00ff,
                               title="BOT Info").add_field(
            name="Bot", value=f"**Version** {__version__}\n"
                              f"**Core module:** N3XT Core v{self.version}\n"
                              f"**Git revision:** {self.get_git_revision()}").add_field(
            name="Plugins", value="\n".join(f"{pl.name}" for pl in Loader.get_plugins()["loaded"])+"\n"+"\n".join(f"{pl.name} *(unloaded)*" for pl in Loader.get_plugins()["unloaded"])
        )
        await interaction.send(embed=embed)

    def get_git_revision(self):
        try:
            rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            rev = "unknown"


def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
