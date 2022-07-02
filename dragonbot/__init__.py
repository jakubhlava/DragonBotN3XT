import os.path

import logging

import nextcord
from nextcord.ext import commands
import configparser
from sqlalchemy import create_engine

__version__ = "3.0"

from sqlalchemy.orm import sessionmaker, Session, declarative_base

from sqlalchemy.orm.scoping import ScopedSession

installdir = os.path.dirname(__file__)

logger = logging.getLogger('nextcord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

cfg = configparser.ConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__), "settings.ini"))

guild_ids = [int(cfg["guild"]["id"])]

engine = create_engine(f"mysql+pymysql://"
                       f"{cfg['db']['username']}:"
                       f"{cfg['db']['password']}@"
                       f"{cfg['db']['host']}:"
                       f"{cfg['db']['port']}/"
                       f"{cfg['db']['database']}", future=True)

session: Session = sessionmaker(engine, future=True)()
base = declarative_base()

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True




bot = commands.Bot(intents=intents)