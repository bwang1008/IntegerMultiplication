"""Implementation of Karatsuba's multiplication algorithm on a Turing machine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integer_multiplication.algorithm.utils import TapeDirection, copy_word
from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.transition import SingleTapeTransition
from integer_multiplication.turing_machine.turing_machine_builder import (
    TuringMachineBuilder,
)

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.turing_machine import TuringMachine


def create_karatsuba_turing_machine() -> TuringMachine:
    """Generate Turing machine that implements Karatsuba's algorithm.

    Method:
        1. Copy first input into arg1 tape, copy second input into arg2 tape.
        2. Write a 1 in recursion_counter tape.
        3. If recursion_counter tape is a 1:
            1. Let x be arg1 value, and y be arg2 value. If x or y are length 1,
                copy answer (y or x) into results tape. Write a blank on the
                recursion_counter tape and move left. Move back to step 3.
            2. Otherwise x, y are both length > 1. Split x into 2 roughly equal
                parts: x1, x0.
            3. Write 1s onto base tape, same length as x0.
            4. Split y into y1 and y0, where len(y0) is the same as len(x0).
            5. On the recursion_counter tape,
                1. Move right
                2. Write a 0, move right.
                3. Write a 1, move right.
                4. Write a 1, move right.
                5. Write a 1, don't move.
            6. Push x1 into arg1 tape, y1 into arg2 tape.
            7. Push x0 into arg1 tape, y0 into arg2 tape.
            8. Push (x0 + x1) into arg1 tape, (y0 + y1) into arg2 tape.
            9. Go back to step 3 (outer).
        4. If recursion_counter tape is a 0:
            1. Pop 3 values from the results tape, as z3, z0, and z2.
            2. Pop value B from the base tape.
            3. Compute z1 = z3 - z0 - z2
            4. Pad z2 with added trailing 0s, twice as many as 1s in B
            5. Pad z1 with trailing 0s, with as many 0s 1s as B.
            6. Compute result = z2 + z1 + z0
            7. Push result into results tape.
            8. Write a blank on recursion_counter tape, move left.
        5. If recursion_counter tape is a blank:
            1. Copy word on results tape into output and halt.
    """
    builder: TuringMachineBuilder = TuringMachineBuilder()

    input_tape: int = builder.get_or_create_tape_index(name="input")
    output_tape: int = builder.get_or_create_tape_index(name="output")
    arg1_tape: int = builder.get_or_create_tape_index(name="arg1")
    arg2_tape: int = builder.get_or_create_tape_index(name="arg2")
    recursion_counter_tape: int = builder.get_or_create_tape_index(
        name="recursion_counter"
    )

    start_node: int = builder.create_state()
    builder.set_starting_state(start_node)
    recursion_start_node: int = builder.create_state()
    end_node: int = builder.create_state(halting=True)

    # step 1
    copy_word(
        builder,
        start_node,
        TapeDirection(input_tape, Shift.RIGHT),
        [TapeDirection(arg1_tape, Shift.RIGHT)],
    )
    # move head of arg1 tape back to least-significant bit; continue input tape
    read_arg2_node: int = builder.create_state()
    builder.add_transition(
        start_node,
        read_arg2_node,
        accept_condition={input_tape: Symbol.BLANK},
        symbols_to_write={},
        tape_shifts={input_tape: Shift.RIGHT, arg1_tape: Shift.LEFT},
    )
    copy_word(
        builder,
        read_arg2_node,
        input_tape=TapeDirection(input_tape, Shift.RIGHT),
        output_tapes=[TapeDirection(arg2_tape, Shift.RIGHT)],
    )
    # move head of arg2 tape back to least-significant bit
    prior_node: int = builder.create_state()
    builder.add_transition(
        read_arg2_node,
        prior_node,
        accept_condition={input_tape: Symbol.BLANK},
        symbols_to_write={},
        tape_shifts={arg2_tape: Shift.LEFT},
    )

    # step 2
    builder.add_single_tape_transition(
        prior_node,
        recursion_start_node,
        recursion_counter_tape,
        SingleTapeTransition(None, Symbol.ONE, None),
    )

    return builder.create()
