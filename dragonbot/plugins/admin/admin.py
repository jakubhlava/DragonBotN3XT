from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption

from dragonbot.loader import Plugin

__version__ = "1.0"


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    def plugin_info(self) -> Plugin:
        return Plugin(
            name="admin",
            description="Administrative tools",
            version=__version__,
            maintainer="HerrKopf",
            dependencies=[]
        )


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
