"""Common functions when designing Turing machines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.turing_machine_builder import (
    SingleTapeTransition,
)

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.turing_machine_builder import (
        TuringMachineBuilder,
    )


@dataclass
class TapeDirection:
    """Class for keeping track of a specific tape and a direction/shift."""

    tape_index: int
    shift: Shift


def move_across_word(
    builder: TuringMachineBuilder,
    start_node: int,
    tape: TapeDirection,
) -> None:
    """Define transitions for moving tape head until a blank occurs.

    :param builder: instance of TuringMachineBuilder that is being used to
        construct the Turing machine these transitions will be a part of
    :param start_node: node that the transitions to move across the tape start
        from
    :param tape: tape index + direction to move across the tape until a
        blank occurs
    """
    builder.add_transition(
        start_node,
        new_state=start_node,
        accept_condition={tape.tape_index: [Symbol.ZERO, Symbol.ONE]},
        symbols_to_write={},
        tape_shifts={tape.tape_index: tape.shift},
    )


def copy_word(
    builder: TuringMachineBuilder,
    start_node: int,
    input_tape: TapeDirection,
    output_tapes: list[TapeDirection],
) -> None:
    """Copy contents of input_tape into output_tapes, until blank is read.

    :param builder: instance of TuringMachineBuilder that is being used to
        construct the Turing machine these transitions will be a part of
    :param start_node: node that the transitions start from
    :param input_tape: tape where input to copy resides
    :param output_tapes: tapes where input should be copied to
    """
    # copy 0s and 1s
    for symbol in [Symbol.ZERO, Symbol.ONE]:
        builder.add_transition(
            start_node,
            new_state=start_node,
            accept_condition={input_tape.tape_index: symbol},
            symbols_to_write={
                output_tape.tape_index: symbol for output_tape in output_tapes
            },
            tape_shifts={
                input_tape.tape_index: input_tape.shift,
                **{
                    output_tape.tape_index: output_tape.shift
                    for output_tape in output_tapes
                },
            },
        )


def erase_word(
    builder: TuringMachineBuilder,
    start_node: int,
    end_node: int,
    tape_index: int,
) -> None:
    """Erase a word from a tape."""
    builder.add_transition(
        start_node,
        start_node,
        accept_condition={tape_index: [Symbol.ZERO, Symbol.ONE]},
        symbols_to_write={tape_index: Symbol.BLANK},
        tape_shifts={tape_index: Shift.LEFT},
    )

    builder.add_single_tape_transition(
        start_node,
        end_node,
        tape_index,
        SingleTapeTransition(Symbol.BLANK, Symbol.BLANK, Shift.LEFT),
    )
