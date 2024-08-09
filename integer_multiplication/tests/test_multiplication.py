"""Tests that generated Turing machines correctly multiply integers together."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from integer_multiplication.algorithm.grade_school import (
    create_grade_school_turing_machine,
)
from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.tape import Tape
    from integer_multiplication.turing_machine.turing_machine import TuringMachine


@pytest.mark.parametrize(
    ("arg1", "arg2"), [(arg1, arg2) for arg1 in range(1, 11) for arg2 in range(1, 11)]
)
def test_multiplication(arg1: int, arg2: int) -> None:
    """Test that generated Turing machines correctly multiply small integers."""
    tm: TuringMachine = create_grade_school_turing_machine()
    tm.set_input_tape_values(
        [*convert_int_to_symbols(arg1), Symbol.BLANK, *convert_int_to_symbols(arg2)]
    )
    tm.run()

    output_value: int = read_integer(tm)
    assert output_value == arg1 * arg2


def read_integer(tm: TuringMachine) -> int:
    """Read a sequence of symbols on a tape as a binary integer."""
    tape: Tape = tm.tapes[1]
    value_read: int = 0
    while (symbol := tape.read()) != Symbol.BLANK:
        bit: int = int(symbol.value)
        value_read = 2 * value_read + bit
        tape.shift(Shift.RIGHT)

    return value_read


def convert_int_to_symbols(val: int) -> list[Symbol]:
    """Turn an int into list of Symbols representing binary integer."""
    bits: list[Symbol] = []
    while val > 0:
        bits.append(Symbol(str(val % 2)))
        val //= 2

    return list(reversed(bits))
