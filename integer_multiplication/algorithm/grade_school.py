"""Implementation of grade-school integer multiplication on Turing machine."""

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.turing_machine import TuringMachine
from integer_multiplication.turing_machine.turing_machine_builder import (
    TuringMachineBuilder,
)


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
    # starting as 0.
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

                builder.add_transition(
                    process_arg2_node,
                    new_state=process_arg2_node,
                    accept_condition={
                        input_tape: Symbol.ONE.value,
                        output_tape: output_value,
                        arg1_tape: arg1_value,
                        carry_tape: carry_value,
                    },
                    symbols_to_write={
                        output_tape: Symbol[str(write_bit)],
                        carry_tape: Symbol[str(carry_bit)],
                    },
                    tape_shifts={
                        output_tape: Shift.LEFT,
                        arg1_tape: Shift.LEFT,
                    },
                )

    # if arg1 tape sees a blank, moved all the way to the left of arg 1.
    # need to start
