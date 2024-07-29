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
        """Initialize head pointer and tape cells to default BLANK."""
        self.head: int = 0
        self.cells: defaultdict = defaultdict(lambda: Symbol.BLANK)

    def read(self) -> Symbol:
        """Get symbol at head of tape.

        :return: Symbol at the tape head
        """
        return self.cells[self.head]

    def write(self, symbol: Symbol) -> None:
        """Set symbol at head of tape.

        :param symbol: Symbol to be written at the head of the tape
        """
        self.cells[self.head] = symbol

    def shift(self, shift_type: Shift) -> None:
        """Shift the head by the amount specified.

        :param shift_type: which way the tape head should shift after a transition
        """
        self.head += shift_type.value
