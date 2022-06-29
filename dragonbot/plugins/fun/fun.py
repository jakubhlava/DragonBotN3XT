from nextcord.ext import commands
from nextcord import slash_command, Interaction, SlashOption


class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
