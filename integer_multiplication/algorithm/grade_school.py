"""Implementation of grade-school integer multiplication on Turing machine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integer_multiplication.algorithm.utils import (
    TapeDirection,
    copy_word,
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


def _create_half_adder_transitions(
    output_tape: TapeDirection,
    summand_tape: TapeDirection,
    carry_tape: int,
) -> list[tuple[dict[int, str | list[str]], dict[int, Symbol], dict[int, Shift]]]:
    """Create transitions corresponding to half-adder inputs and outputs.

    :param output_tape: which tape the output is stored on, as well as which
        direction / shift to go from least to most significant bit.
    :param summand_tape: which tape that should be added to output.
    :param carry_tape: tape that holds the carry bit, initially assigned to 0
    :return: the transitions corresponding to half-adder logic
    """
    transitions: list[
        tuple[dict[int, str | list[str]], dict[int, Symbol], dict[int, Shift]]
    ] = []

    output_value: str | list[str]
    for output_value in ([Symbol.BLANK.value, Symbol.ZERO.value], Symbol.ONE.value):
        for arg1_value in [Symbol.ZERO.value, Symbol.ONE.value]:
            for carry_value in [Symbol.ZERO.value, Symbol.ONE.value]:
                # add the 3 bits in the 3 tapes
                triple_sum: int = [output_value, arg1_value, carry_value].count(
                    Symbol.ONE.value
                )

                # split into 2 bits: the one you write, and the one to be carried over
                write_bit: int = triple_sum & 1
                carry_bit: int = (triple_sum // 2) & 1

                accept_condition = {
                    output_tape.tape_index: output_value,
                    summand_tape.tape_index: arg1_value,
                    carry_tape: carry_value,
                }
                symbols_to_write = {
                    output_tape.tape_index: Symbol[str(write_bit)],
                    carry_tape: Symbol[str(carry_bit)],
                }
                tape_shifts = {
                    output_tape.tape_index: output_tape.shift,
                    summand_tape.tape_index: summand_tape.shift,
                }

                transitions.append((accept_condition, symbols_to_write, tape_shifts))

    return transitions


def create_grade_school_turing_machine() -> TuringMachine:
    """Generate Turing machine that implements grade school multiplication.

    Method:
        1. Copy first input into arg1 tape
        2. For each bit in arg1, from least to most significant bit,
            make a forward pass across all bits of the second argument on the
            input tape, and add all bits to an accumulated sum on the output
            tape. Maintain carry bit on a separate tape.
    """
    builder = TuringMachineBuilder()

    input_tape: int = builder.get_or_create_tape_index(name="input")
    output_tape: int = builder.get_or_create_tape_index(name="output")
    arg1_tape: int = builder.get_or_create_tape_index(name="arg1")
    carry_tape: int = builder.get_or_create_tape_index(name="carry")

    start_node: int = builder.get_or_create_state(name="start")

    # copy first input into arg1 tape
    copy_word(
        builder,
        start_node,
        TapeDirection(input_tape, Shift.RIGHT),
        [TapeDirection(arg1_tape, Shift.RIGHT)],
    )

    # When encounter a blank, you are in between the two inputs.
    # Use this time when the input head moves to the second input
    # to write a 0 into the carry tape.
    read_arg2_node: int = builder.get_or_create_state(name="read_arg2")
    builder.add_transition(
        start_node,
        new_state=read_arg2_node,
        accept_condition={input_tape: Symbol.BLANK.value},
        symbols_to_write={
            carry_tape: Symbol.ZERO,
        },
        tape_shifts={
            input_tape: Shift.RIGHT,  # head now on most-significant bit of 2nd arg
            arg1_tape: Shift.LEFT,  # set head on least-significant bit
        },
    )

    # move input tape head so that it is at the least-significant bit of 2nd arg
    move_across_word(
        builder,
        read_arg2_node,
        TapeDirection(input_tape, Shift.RIGHT),
    )
    # at blank at the end of the 2nd arg, move back one
    process_arg2_node: int = builder.get_or_create_state()
    builder.add_single_tape_transition(
        read_arg2_node,
        process_arg2_node,
        input_tape,
        single_transition=SingleTapeTransition(
            Symbol.BLANK.value, Symbol.BLANK, Shift.LEFT
        ),
    )

    # Now have 2 tapes with heads at least-significant bit of each argument.
    # Multiply current bit of 2nd arg with all bits of 1st arg, going from
    # least to most-significant bit of 1st arg. That is, add a copy of arg1 to
    # the output tape.

    # when current bit of 2nd arg is 0, continue to next bit.
    builder.add_transition(
        process_arg2_node,
        new_state=process_arg2_node,
        accept_condition={
            input_tape: Symbol.ZERO.value,
            # write a 0 to output tape if currently BLANK
            output_tape: Symbol.BLANK.value,
        },
        symbols_to_write={
            output_tape: Symbol.ZERO,
        },
        tape_shifts={
            arg1_tape: Shift.LEFT,  # continue to more significant bit of arg2
            output_tape: Shift.LEFT,  # shift partial sum since now higher power of 2
        },
    )
    builder.add_transition(
        process_arg2_node,
        new_state=process_arg2_node,
        accept_condition={
            arg1_tape: Symbol.ZERO.value,
            output_tape: [Symbol.ZERO.value, Symbol.ONE.value],
        },
        # if output tape bit not blank, no need to write
        symbols_to_write={},
        tape_shifts={
            arg1_tape: Shift.LEFT,
            output_tape: Shift.LEFT,
        },
    )

    # when current bit of 2nd arg is a 1, add a copy of arg1 to the sum in output.
    # Use the carry_tape to implement a half-adder: given 3 bits on output_tape,
    # arg1_tape, and carry_tape, each 0 or 1, add the 3 bits together. Write the
    # least signficant bit of the sum to output_tape, while the 2nd-least
    # significant bit is written to the carry_tape.
    # Note that output_tape starting as BLANK should be treated the same as
    # starting as 1.

    half_adder_transitions: list[
        tuple[dict[int, str | list[str]], dict[int, Symbol], dict[int, Shift]]
    ] = _create_half_adder_transitions(
        TapeDirection(output_tape, Shift.LEFT),
        TapeDirection(arg1_tape, Shift.LEFT),
        carry_tape,
    )

    # (output += arg1) loop from least-significant to most-significant bit
    for accept_condition, symbols_to_write, tape_shifts in half_adder_transitions:
        builder.add_transition(
            process_arg2_node,
            new_state=process_arg2_node,
            accept_condition={
                # only add to output tape if current arg2 bit is a 1
                input_tape: Symbol.ONE.value,
                **accept_condition,
            },
            symbols_to_write=symbols_to_write,
            tape_shifts=tape_shifts,
        )

    # end of (output += arg1) is when arg1 tape hits blank beyond most-significant bit.
    # Then worry about any leftover carry. Since traversed from least to
    # most-significant bit, then output bit should be BLANK
    move_back_across_arg1_node: int = builder.get_or_create_state()
    builder.add_transition(
        process_arg2_node,
        move_back_across_arg1_node,
        accept_condition={
            input_tape: Symbol.ONE.value,
            arg1_tape: Symbol.BLANK.value,
            carry_tape: Symbol.ZERO.value,
        },
        symbols_to_write={},
        tape_shifts={
            output_tape: Shift.RIGHT,
            arg1_tape: Shift.RIGHT,
        },
    )
    # if carry bit was set, write a 1
    builder.add_transition(
        process_arg2_node,
        move_back_across_arg1_node,
        accept_condition={
            input_tape: Symbol.ONE.value,
            arg1_tape: Symbol.BLANK.value,
            carry_tape: Symbol.ONE.value,
        },
        symbols_to_write={
            output_tape: Symbol.ONE,
            carry_tape: Symbol.ZERO,
        },
        tape_shifts={
            output_tape: Shift.RIGHT,
            arg1_tape: Shift.RIGHT,
        },
    )

    # Head of arg1 tape has already moved all the way to the left of arg 1. Now move the
    # head of the arg1 tape back to the right, the least-significant bit, just like
    # performing the grade-school multiplication algorithm on paper where you write
    # the next summand on the next line starting from the least significant bit.
    builder.add_transition(
        move_back_across_arg1_node,
        new_state=move_back_across_arg1_node,
        accept_condition={arg1_tape: [Symbol.ZERO.value, Symbol.ONE.value]},
        symbols_to_write={},
        tape_shifts={arg1_tape: Shift.RIGHT, output_tape: Shift.RIGHT},
    )
    # once arg1 tape has hit blank on right of arg1, shift back one to go back
    # to where it started from, on the least-significant bit
    shift_arg2_head_left_node: int = builder.get_or_create_state()
    builder.add_transition(
        move_back_across_arg1_node,
        new_state=shift_arg2_head_left_node,
        accept_condition={arg1_tape: Symbol.BLANK.value},
        symbols_to_write={},
        tape_shifts={arg1_tape: Shift.LEFT, output_tape: Shift.LEFT},
    )

    # now move on to the next significant bit of arg2
    builder.add_transition(
        shift_arg2_head_left_node,
        new_state=process_arg2_node,
        accept_condition={},
        symbols_to_write={
            carry_tape: Symbol.ZERO,
        },
        tape_shifts={input_tape: Shift.LEFT, output_tape: Shift.LEFT},
    )

    # main loop done: check when input tape finishes going through all arg2 bits
    move_output_tape_head_left: int = builder.get_or_create_state()
    builder.add_transition(
        process_arg2_node,
        new_state=move_output_tape_head_left,
        accept_condition={input_tape: Symbol.BLANK.value},
        symbols_to_write={},
        tape_shifts={},
    )

    # move head of output_tape to left-most bit
    move_across_word(
        builder, move_output_tape_head_left, TapeDirection(output_tape, Shift.LEFT)
    )
    # once reaches blank on left, move one right to non-blank bit
    end_node: int = builder.get_or_create_state(halting=True)
    builder.add_single_tape_transition(
        move_output_tape_head_left,
        end_node,
        output_tape,
        SingleTapeTransition(
            accept_condition=None, symbol_to_write=None, shift=Shift.RIGHT
        ),
    )

    return builder.create()
