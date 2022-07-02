from sqlalchemy import BigInteger, Column, Integer
from dragonbot import base
from dragonbot.core.model import CoreACL


class CoreUser(base):

    __tablename__ = "core_user"

    id: int = Column(BigInteger, primary_key=True)
    acl: int = Column(Integer)