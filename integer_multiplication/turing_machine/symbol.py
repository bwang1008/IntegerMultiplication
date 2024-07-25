"""Enumeration of valid symbols on a tape."""

from enum import Enum


class Symbol(str, Enum):
    """Contents of a cell on a tape."""

    BLANK = "_"
    ZERO = "0"
    ONE = "1"
