"""Tape class."""

from collections import defaultdict

from integer_multiplication.turing_machine.symbol import Symbol


class Tape:
    """Class defining tape of a Turing machine."""

    def __init__(self) -> None:
        """Initialize head pointer and tape cells."""
        self.head: int = 0
        self.cells: defaultdict = defaultdict(lambda: Symbol.BLANK)

    def __getitem__(self, index: int) -> Symbol:
        """Retrieve contents of tape at index."""
        return self.cells[index]

    def __setitem__(self, index: int, symbol: Symbol) -> None:
        """Set content of tape at index."""
        self.cells[index] = symbol
