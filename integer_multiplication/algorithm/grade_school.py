"""Implementation of grade-school integer multiplication on Turing machine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.turing_machine_builder import (
    TuringMachineBuilder,
)

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.turing_machine import TuringMachine


@dataclass
class TapeDirection:
    """Class for keeping track of a specific tape and a direction/shift."""

    tape_index: int
    shift: Shift


def _create_half_adder_transitions(
    output_tape: TapeDirection,
    summand_tape: TapeDirection,
    carry_tape: int,
) -> list[tuple[dict[int, str], dict[int, Symbol], dict[int, Shift]]]:
    """Create transitions corresponding to half-adder inputs and outputs.

    :param output_tape: which tape the output is stored on, as well as which
        direction / shift to go from least to most significant bit.
    :param summand_tape: which tape that should be added to output.
    :param carry_tape: tape that holds the carry bit, initially assigned to 0
    :return: the state that the transitions end on
    """
    transitions: list[tuple[dict[int, str], dict[int, Symbol], dict[int, Shift]]] = []
    for output_value in [[Symbol.BLANK.value, Symbol.ZERO.value], Symbol.ONE.value]:
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
                    carry_tape.tape_index: Symbol[str(carry_bit)],
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
        2. For each bit in the second arg on input tape,
            go through each bit of first arg on arg1 tape, and add to
            accumulated sum on output tape. Maintain carry bit on carry tape.
    """
    builder = TuringMachineBuilder()

    input_tape: int = builder.get_or_create_tape_index(name="input")
    output_tape: int = builder.get_or_create_tape_index(name="output")
    arg1_tape: int = builder.get_or_create_tape_index(name="arg1")
    carry_tape: int = builder.get_or_create_tape_index(name="carry")

    start_node: int = builder.get_or_create_state(name="start")

    # copy first input into arg1 tape
    # copy 0s
    builder.add_transition(
        start_node,
        new_state=start_node,
        accept_condition={input_tape: Symbol.ZERO.value},
        symbols_to_write={arg1_tape: Symbol.ZERO.value},
        tape_shifts={input_tape: Shift.RIGHT, arg1_tape: Shift.RIGHT},
    )
    # copy 1s
    builder.add_transition(
        start_node,
        new_state=start_node,
        accept_condition={input_tape: Symbol.ONE.value},
        symbols_to_write={arg1_tape: Symbol.ONE.value},
        tape_shifts={input_tape: Shift.RIGHT, arg1_tape: Shift.RIGHT},
    )
    # When encounter a blank, you are in between the two inputs.
    # Use this time when the input head moves to the second input,
    # to write a 0 into the carry tape.
    process_arg2_node: int = builder.get_or_create_state(name="process_arg2")
    builder.add_transition(
        start_node,
        new_state=process_arg2_node,
        accept_condition={input_tape: Symbol.BLANK.value},
        symbols_to_write={
            carry_tape: Symbol.ZERO.value,
        },
        tape_shifts={
            input_tape: Shift.RIGHT,  # head now on most-significant bit of 2nd arg
            arg1_tape: Shift.LEFT,  # set head on least-significant bit
        },
    )

    # Multiply current bit of 2nd arg with all bits of 1st arg, going from
    # least-significant bit of 1st arg to most-significant. That is, when the
    # current bit of 2nd arg is a 1, then
    # output_tape += arg1.

    # when current bit of 2nd arg is 0, continue to next bit
    builder.add_transition(
        process_arg2_node,
        new_state=process_arg2_node,
        accept_condition={input_tape: Symbol.ZERO.value},
        symbols_to_write={},
        tape_shifts={
            input_tape: Shift.RIGHT,  # continue to next bit of arg2
            output_tape: Shift.RIGHT,  # shift partial sum since lower power of 2
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
        tuple[dict[int, str], dict[int, Symbol], dict[int, Shift]]
    ] = _create_half_adder_transitions(
        TapeDirection(output_tape, Shift.LEFT),
        TapeDirection(arg1_tape, Shift.LEFT),
        carry_tape,
    )

    for accept_condition, symbols_to_write, tape_shifts in half_adder_transitions:
        builder.add_transition(
            process_arg2_node,
            new_state=process_arg2_node,
            accept_condition={
                input_tape: Symbol.ONE.value,
                **accept_condition,
            },
            symbols_to_write=symbols_to_write,
            tape_shifts=tape_shifts,
        )

    # if arg1 tape sees a blank, then the head has already moved all the way
    # to the left of arg 1. Here, we need to move the head of the arg1 tape
    # back to the right, the least-significant bit, just like performing the
    # grade-school multiplication algorithm on paper where you write the next
    # summand on the next line starting from the least significant bit.
