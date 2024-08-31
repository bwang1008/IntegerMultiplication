"""Implementation of Karatsuba's multiplication algorithm on a Turing machine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integer_multiplication.algorithm.utils import (
    TapeDirection,
    copy_word,
    erase_word,
    move_across_word,
)
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
            1. Let x be arg1 value, and y be arg2 value. Pop x and y from arg1,
                arg2 tapes. If x or y are length 1, copy answer (0, y, or x)
                into results tape. Write a blank on the recursion_counter tape
                and move left. Move back to step 3.
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

    start_node: int = builder.create_state()
    builder.set_starting_state(start_node)

    main_loop_node: int = builder.create_state()
    _initialize(builder, start_node, main_loop_node)

    # step 3
    start_split_node: int = builder.create_state()
    recursion_counter_tape: int = builder.get_or_create_tape_index(
        name="recursion_counter"
    )

    builder.add_single_tape_transition(
        main_loop_node,
        start_split_node,
        recursion_counter_tape,
        SingleTapeTransition(Symbol.ONE, None, None),
    )
    _main_loop(builder, start_split_node, main_loop_node)

    return builder.create()


def _initialize(builder: TuringMachineBuilder, start_node: int, end_node: int) -> None:
    """Implement steps 1 and 2, to prepare for main loop."""
    input_tape: int = builder.get_or_create_tape_index(name="input")
    arg1_tape: int = builder.get_or_create_tape_index(name="arg1")
    arg2_tape: int = builder.get_or_create_tape_index(name="arg2")
    recursion_counter_tape: int = builder.get_or_create_tape_index(
        name="recursion_counter"
    )

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
        end_node,
        recursion_counter_tape,
        SingleTapeTransition(None, Symbol.ONE, None),
    )


def _main_loop(builder: TuringMachineBuilder, start_node: int, end_node: int) -> None:
    """Check both args on arg1, arg2, and split if needed.

    arg1, arg2 tape heads should be at least-significant bits (right-hand-side).
    """
    #  arguments_len1


def _handle_len_1(
    builder: TuringMachineBuilder,
    start_node: int,
    end_node: int,
    len_1_tape: int,
    arg_tape: int,
) -> None:
    """Write result of arg1 * arg2 into results tape, when one arg is 0 / 1.

    Assume len_1_tape is either a 0 or 1, while arg_tape is at least-significant
    bit.
    Assume results tape is at a blank, and to its left is a blank (clear from
    any previous results).

    Afterwards, len_1_tape and arg_tape should be popped, and pointing at
    the previous's least-significant bit.
    The results_tape should add the multiplication result, and move 2 right
    onto a new blank.
    """
    write_0_node: int = builder.create_state()
    write_1_node: int = builder.create_state()
    results_tape: int = builder.get_or_create_tape_index(name="results")

    # if multiply 0 x N, result is a 0
    builder.add_single_tape_transition(
        start_node,
        write_0_node,
        len_1_tape,
        SingleTapeTransition(Symbol.ZERO, None, None),
    )
    # write a 0 to results tape
    move_right_node: int = builder.create_state()
    builder.add_single_tape_transition(
        write_0_node,
        move_right_node,
        results_tape,
        SingleTapeTransition(None, Symbol.ZERO, Shift.RIGHT),
    )
    # need to shift results tape right again
    erase_node: int = builder.create_state()
    builder.add_single_tape_transition(
        move_right_node,
        erase_node,
        results_tape,
        SingleTapeTransition(None, None, Shift.RIGHT),
    )

    # else if multiply 1 x N, result is N
    builder.add_single_tape_transition(
        start_node,
        write_1_node,
        len_1_tape,
        SingleTapeTransition(Symbol.ONE, None, None),
    )
    # point arg_tape at most-significant bit
    move_across_word(builder, write_1_node, TapeDirection(arg_tape, Shift.LEFT))
    start_copy_node: int = builder.create_state()
    builder.add_single_tape_transition(
        write_1_node,
        start_copy_node,
        arg_tape,
        SingleTapeTransition(Symbol.BLANK, None, Shift.RIGHT),
    )
    copy_word(
        builder,
        start_copy_node,
        TapeDirection(arg_tape, Shift.RIGHT),
        [TapeDirection(results_tape, Shift.RIGHT)],
    )
    # move results tape one more right (so it can add a new entry)
    # and move arg tape left, on least-signficiant bit, so we can erase
    builder.add_transition(
        start_copy_node,
        erase_node,
        accept_condition={},
        symbols_to_write={},
        tape_shifts={results_tape: Shift.RIGHT, arg_tape: Shift.LEFT},
    )

    # pop both args
    erase_node_2: int = builder.create_state()
    erase_node_3: int = builder.create_state()
    erase_word(builder, erase_node, erase_node_2, len_1_tape)
    builder.add_single_tape_transition(
        erase_node_2,
        erase_node_3,
        len_1_tape,
        SingleTapeTransition(None, None, None),
    )
    erase_word(builder, erase_node_3, end_node, arg_tape)
