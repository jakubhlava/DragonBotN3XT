import nextcord
from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption
from dragonbot import guild_ids, __version__, base, engine, session
from dragonbot.core.model import *
from dragonbot.loader import Loader
from dragonbot.core import access_control
import subprocess


class Core(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.version = "1.0"
        base.metadata.create_all(engine)
        print(f"N3XT Core v{self.version} Loaded")

    @slash_command(guild_ids=guild_ids, description="Načte plugin")
    @access_control.check(CoreACL.ADMIN)
    async def load(self, interaction: Interaction,
                   plugin_name: str = SlashOption(description="Název pluginu", required=True, autocomplete=True,
                                                  autocomplete_callback=Loader.unloaded_autocomplete)):
        status = await Loader.load(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` načten!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` nelze načíst!")

    @slash_command(guild_ids=guild_ids, description="Vypne plugin")
    @access_control.check(CoreACL.ADMIN)
    async def unload(self, interaction: Interaction,
                     plugin_name: str = SlashOption(description="Název pluginu", required=True, autocomplete=True,
                                                    autocomplete_callback=Loader.loaded_autocomplete)):
        status = Loader.unload(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` vypnut!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` nelze vypnout!")

    @slash_command(guild_ids=guild_ids, description="Přenačte plugin")
    @access_control.check(CoreACL.ADMIN)
    async def reload(self, interaction: Interaction,
                     plugin_name: str = SlashOption(description="Název pluginu", required=True, autocomplete=True,
                                                    autocomplete_callback=Loader.loaded_autocomplete)):
        status = Loader.reload(plugin_name)
        if status:
            await interaction.send(f":white_check_mark: Plugin `{plugin_name}` přenačten!")
        else:
            await interaction.send(f":x: Plugin `{plugin_name}` nelze přenačíst!")

    @slash_command(guild_ids=guild_ids, description="Vyhledá dostupné pluginy")
    @access_control.check(CoreACL.ADMIN)
    async def rediscover(self, interaction: Interaction):
        Loader.discover()
        await interaction.send("Pluginy byly znovu nalezeny!")

    @slash_command(guild_ids=guild_ids, description="Zobrazí informace o botovi")
    @access_control.check(CoreACL.ADMIN)
    async def info(self, interaction: Interaction):
        embed = nextcord.Embed(color=0xab00ff,
                               title="BOT Info").add_field(
            name="Bot", value=f"**Verze** {__version__}\n"
                              f"**Core modul:** N3XT Core v{self.version}\n"
                              f"**Git revize:** {self.get_git_revision()}").add_field(
            name="Pluginy", value="\n".join(f"{pl.name}" for pl in Loader.get_plugins()["loaded"])+"\n"+"\n".join(f"{pl.name} *(vypnutý)*" for pl in Loader.get_plugins()["unloaded"])
        )
        await interaction.send(embed=embed)

    @slash_command(guild_ids=guild_ids, description="Nastaví ACL")
    @access_control.check(CoreACL.OWNER)
    async def setacl(self, interaction: Interaction,
                     user: nextcord.Member = SlashOption(description="Uživatel pro změnu ACL"),
                     acl: int = SlashOption(description="Access Control Level, 60 = MOD, 80 = ADMIN, 100 = OWNER")):
        db_user = session.get(CoreUser, user.id)
        if not db_user:
            db_user = CoreUser(id=user.id, acl=acl)
            session.add(db_user)
        else:
            db_user.acl = acl
        session.commit()
        await interaction.send(f":white_check_mark: Uživatel {user.name} má nyní ACL **{acl}**")

    @staticmethod
    def get_git_revision():
        try:
            rev = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            rev = "unknown"
        return rev


def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
