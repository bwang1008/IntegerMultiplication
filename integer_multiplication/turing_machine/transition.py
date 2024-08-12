"""Defines how a transition of Turing machine matches inputs and gives outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.shift import Shift
    from integer_multiplication.turing_machine.symbol import Symbol


class Transition:
    """Transition describes how to match inputs and write output Symbols and shifts.

    This format is used to store only what is used. The format of specifying
    every direct transition possible is avoided, because otherwise a T-tape
    Turing machine would need 3^T transitions between every pair of states.
    """

    def __init__(
        self,
        *,
        new_state: int,
        accept_condition: dict[int, Symbol],
        symbols_to_write: dict[int, Symbol],
        tape_shifts: dict[int, Shift],
    ) -> None:
        """Contains data on what state to transition, output symbols, and shifts.

        :param new_state: what state the Turing machine should move to
        :param accept_condition: dictionary of tape indices to characters.
            If all characters of a given tape input at these specified indices
            match the mapped characters, then this transition is taken. For
            example, if accept_condition := {0: "1", 2: "0"}, then tape_input
            "100" on a 3-tape Turing machine would match, since the 0th char is
            "1" and the 2nd char is "0".
        :param symbols_to_write: dictionary of tape indices to symbols.
            When a given tape input matches accept_condition, the tapes at
            these indices should write their corresponding character symbols.
            Any tape index not specified is assumed to leave its existing
            cell content unchanged; i.e. no write is needed. For example,
            if symbols_to_write := {0: Symbol["1"], 2: Symbol["0"]}, then tape 0
            should write a "1", and tape 2 should write a "0".
        :param tape_shifts: dictionary of tape indices to shifts. When a given
            tape input matches accept_condition, the tapes at these indices
            should shift left, right, or not shift after writing a symbol.
        """
        self.new_state: int = new_state
        self.accept_condition: dict[int, Symbol] = accept_condition
        self.symbols_to_write: dict[int, Symbol] = symbols_to_write
        self.tape_shifts: dict[int, Shift] = tape_shifts

    def matches(self, tape_input: str) -> bool:
        """Determine if tape_input matches accept_condition.

        :param tape_input: the contents of the tapes of the Turing machine,
            concatenated together in order as a string
        :return: True when the tape_input matches the accept_condition
            on the accept_condition's specified tape indices
        """
        for index, desired_character in self.accept_condition.items():
            if tape_input[index] != desired_character.value:
                return False

        return True


@dataclass
class SingleTapeTransition:
    """Simplified transition that only reads and writes from one tape."""

    accept_condition: Symbol | None
    symbol_to_write: Symbol | None
    shift: Shift | None
