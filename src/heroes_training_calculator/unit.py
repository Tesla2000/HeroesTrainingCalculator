from __future__ import annotations

from enum import Enum


class Unit(str, Enum):
    PEASANT = "peasant"
    ARCHER = "archer"
    FOOTMAN = "footman"
    GRIFFIN = "griffin"
    PRIEST = "priest"
    CAVALIER = "cavalier"
    ANGEL = "angel"
