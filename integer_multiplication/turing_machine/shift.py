"""Enumerations of valid shifts of a tape head."""

from enum import Enum


class Shift(Enum):
    """Valid shifts of tape head."""

    LEFT = -1
    NONE = 0
    RIGHT = 1
