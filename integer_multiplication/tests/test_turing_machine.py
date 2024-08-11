"""Tests behavior of Turing machine class."""

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.transition import Transition
from integer_multiplication.turing_machine.turing_machine import TuringMachine


def test_turing_machine_set_input_tape_values() -> None:
    """Check that setting input is on tape 0 and has expected symbols."""
    tm: TuringMachine = TuringMachine(
        num_states=2,
        num_tapes=1,
        starting_state=0,
        halting_states={1},
        transitions=[
            [
                Transition(
                    new_state=1,
                    accept_condition={},
                    symbols_to_write={0: Symbol.ONE},
                    tape_shifts={0: Shift.RIGHT},
                )
            ]
        ],
    )

    tm.set_input_tape_values(
        [Symbol.ONE, Symbol.ZERO, Symbol.BLANK, Symbol.ONE], reset_tape_head=True
    )

    assert len(tm.tapes) == 1
    assert tm.tapes[0].head == 0
    assert tm.tapes[0].cells == {
        0: Symbol.ONE,
        1: Symbol.ZERO,
        2: Symbol.BLANK,
        3: Symbol.ONE,
    }
