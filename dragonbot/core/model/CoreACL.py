from enum import Enum


class CoreACL(Enum):
    OWNER = 100
    ADMIN = 80
    MOD = 60
    DEFAULT = 0
