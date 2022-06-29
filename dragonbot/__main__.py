import nextcord

from dragonbot import bot, cfg, guild_ids, __version__
from dragonbot.loader import Loader


@bot.event
async def on_ready():
    print(f"DragonBot N3XT v{__version__} connected")
    bot.load_extension("core.core")
    for guild_id in guild_ids:
        guild = bot.get_guild(guild_id)
        await guild.sync_application_commands()
    await Loader.load_all()


@bot.slash_command(description="Core reload", guild_ids=guild_ids)
async def reloadcore(interaction: nextcord.Interaction):
    bot.reload_extension("core.core")
    for guild_id in guild_ids:
        guild = bot.get_guild(guild_id)
        await guild.sync_application_commands()
    await interaction.send("Core reloaded.")

if __name__ == "__main__":
    bot.run(cfg["bot"]["token"])