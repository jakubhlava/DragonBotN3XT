import os
from dragonbot import installdir, bot, guild_ids
from dragonbot.loader import Plugin

import nextcord.ext.commands

plugindir = os.path.join(installdir, "plugins")
discovered_plugins: dict[str, Plugin] = {}


def discover():
    global discovered_plugins
    try:
        with open(os.path.join(plugindir, "plugins.ignore")) as f:
            ignored_plugins = f.readlines()
    except EnvironmentError:
        ignored_plugins = []
    dirs = [d for d in os.listdir(plugindir) if os.path.isdir(os.path.join(plugindir, d)) and d not in ignored_plugins]
    dirs = [d for d in dirs if any(f.endswith(".py") for f in os.listdir(os.path.join(plugindir, d)))]
    for d in dirs:
        discovered_plugins[d] = Plugin(os.path.basename(d))


async def load_all():
    discover()
    for pl in discovered_plugins.keys():
        await load(pl)


async def loaded_autocomplete(state, integration, option_data) -> list[str]:
    if not option_data:
        option_data = ""
    return [pl for pl in discovered_plugins.keys() if discovered_plugins[pl].loaded and pl.startswith(option_data)]


async def unloaded_autocomplete(state, integration, option_data) -> list[str]:
    if not option_data:
        option_data = ""
    return [pl for pl in discovered_plugins.keys() if not discovered_plugins[pl].loaded and pl.startswith(option_data)]


def get_plugins() -> dict[str: list[Plugin]]:
    """Returns two lists of plugins keyed 'loaded' and 'unloaded'"""
    return {
        "loaded": [pl for pl in discovered_plugins.values() if pl.loaded],
        "unloaded": [pl for pl in discovered_plugins.values() if not pl.loaded]
    }


def get_plugin(plugin_name: str) -> Plugin:
    try:
        plugin = discovered_plugins[plugin_name]
    except KeyError:
        print(f"Plugin {plugin_name} does not exist")
        return None
    return plugin


async def load(plugin_name: str):
    plugin = get_plugin(plugin_name)
    if not plugin.loaded:
        try:
            bot.load_extension(plugin.load_str)
            for guild_id in guild_ids:
                guild = bot.get_guild(guild_id)
                await guild.sync_application_commands()
        except AttributeError:
            return False
    plugin.loaded = True
    return True


def unload(plugin_name: str):
    plugin = get_plugin(plugin_name)
    if plugin.loaded:
        try:
            bot.unload_extension(plugin.load_str)
        except AttributeError:
            return False
    plugin.loaded = False
    return True


async def reload(plugin_name: str):
    plugin = get_plugin(plugin_name)
    if plugin.loaded:
        try:
            bot.reload_extension(plugin.load_str)
            for guild_id in guild_ids:
                guild = bot.get_guild(guild_id)
                await guild.sync_application_commands()
        except AttributeError:
            return False
    plugin.loaded = True
    return True


