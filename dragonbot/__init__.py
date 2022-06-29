import os.path

import logging

import nextcord
from nextcord.ext import commands
import configparser

__version__ = "3.0"
installdir = os.path.dirname(__file__)

logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), "settings.ini"))

guild_ids = [int(cfg["guild"]["id"])]

print(guild_ids)

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(intents=intents)