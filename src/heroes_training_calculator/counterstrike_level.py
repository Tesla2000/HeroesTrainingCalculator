from __future__ import annotations

from enum import Enum


class CounterstrikeLevel(str, Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    EXPERT = "expert"
    ULTIMATE = "ultimate"
