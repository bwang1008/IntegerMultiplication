"""Tape class."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.symbol import Symbol

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.shift import Shift


class Tape:
    """Class defining tape of a Turing machine."""

    def __init__(self) -> None:
        """Initialize head pointer and tape cells."""
        self.head: int = 0
        self.cells: defaultdict = defaultdict(lambda: Symbol.BLANK)

    def read(self) -> Symbol:
        """Get symbol at head of tape."""
        return self.cells[self.head]

    def write(self, symbol: Symbol) -> None:
        """Set symbol at head of tape."""
        self.cells[self.head] = symbol

    def shift(self, shift_type: Shift) -> None:
        """Shift the head by the amount specified."""
        self.head += shift_type.value

    def set_input(self, starting_symbols: list[Symbol]) -> None:
        """Set the initial tape contents, moving head right."""
        for symbol in starting_symbols:
            self.cells[self.head] = symbol
            self.head += 1
