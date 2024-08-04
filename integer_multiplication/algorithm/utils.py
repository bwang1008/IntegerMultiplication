"""Common functions when designing Turing machines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.symbol import Symbol

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.shift import Shift
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
        accept_condition={tape.tape_index: [Symbol.ZERO.value, Symbol.ONE.value]},
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
    tape_shifts: dict[int, Shift] = {
        input_tape.tape_index: input_tape.shift,
        **{output_tape.tape_index: output_tape.shift for output_tape in output_tapes},
    }

    # copy 0s
    builder.add_transition(
        start_node,
        new_state=start_node,
        accept_condition={input_tape.tape_index: Symbol.ZERO.value},
        symbols_to_write={
            output_tape.tape_index: Symbol.ZERO for output_tape in output_tapes
        },
        tape_shifts=tape_shifts,
    )
    # copy 1s
    builder.add_transition(
        start_node,
        new_state=start_node,
        accept_condition={input_tape.tape_index: Symbol.ONE.value},
        symbols_to_write={
            output_tape.tape_index: Symbol.ONE for output_tape in output_tapes
        },
        tape_shifts=tape_shifts,
    )
