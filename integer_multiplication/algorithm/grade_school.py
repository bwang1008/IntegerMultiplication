"""Implementation of grade-school integer multiplication on Turing machine."""

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.transition import Transition
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
    builder.add_transition_general(
        start_node,
        Transition(
            new_state=start_node,
            accept_condition={input_tape: Symbol.ZERO.value},
            symbols_to_write={arg1_tape: Symbol.ZERO.value},
            tape_shifts={input_tape: Shift.RIGHT, arg1_tape: Shift.RIGHT},
        ),
    )
    # copy 1s
    builder.add_transition_general(
        start_node,
        Transition(
            new_state=start_node,
            accept_condition={input_tape: Symbol.ONE.value},
            symbols_to_write={arg1_tape: Symbol.ONE.value},
            tape_shifts={input_tape: Shift.RIGHT, arg1_tape: Shift.RIGHT},
        ),
    )
    # When encounter a blank, you are in between the two inputs.
    # Use this time when the input head moves to the second input,
    # to write a 0 into the output tape and into the carry tape.
    between_inputs_node: int = builder.get_or_create_state(name="between")
    builder.add_transition_general(
        start_node,
        Transition(
            new_state=between_inputs_node,
            accept_condition={input_tape: Symbol.BLANK.value},
            symbols_to_write={
                output_tape: Symbol.ZERO.value,
                carry_tape: Symbol.ZERO.value,
            },
            tape_shifts={
                input_tape: Shift.RIGHT,  # head now on most-significant bit of 2nd arg
                arg1_tape: Shift.LEFT,  # set head on least-significant bit
            },
        ),
    )
