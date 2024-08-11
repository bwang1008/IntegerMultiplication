"""Tests behavior of TuringMachineBuilder methods."""

from typing import TYPE_CHECKING

import pytest

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.transition import (
    SingleTapeTransition,
    Transition,
)
from integer_multiplication.turing_machine.turing_machine_builder import (
    TuringMachineBuilder,
)

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.turing_machine import TuringMachine


def test_get_or_create_tape_index() -> None:
    """Check that naming a tape will not be created later."""
    builder: TuringMachineBuilder = TuringMachineBuilder()
    current_num_tapes: int = 0
    assert builder.num_tapes == current_num_tapes

    tape_index_1: int = builder.get_or_create_tape_index(name="test_tape_1")
    current_num_tapes += 1
    assert builder.num_tapes == current_num_tapes

    tape_index_2: int = builder.get_or_create_tape_index(name="test_tape_2")
    current_num_tapes += 1
    assert builder.num_tapes == current_num_tapes
    assert tape_index_1 != tape_index_2

    tape_index_1_again: int = builder.get_or_create_tape_index(name="test_tape_1")
    assert builder.num_tapes == current_num_tapes
    assert tape_index_1 == tape_index_1_again


def test_create() -> None:
    """Check that create returns TuringMachine with specified transition."""
    builder: TuringMachineBuilder = TuringMachineBuilder()
    tape_index: int = builder.get_or_create_tape_index(name="one")
    start_node: int = builder.create_state()
    end_node: int = builder.create_state(halting=True)
    current_num_states: int = 2

    builder.add_single_tape_transition(
        start_node,
        end_node,
        tape_index,
        SingleTapeTransition(Symbol.ZERO, Symbol.ONE, Shift.RIGHT),
    )

    with pytest.raises(
        RuntimeError, match="Must set starting_state before creating Turing machine."
    ):
        builder.create()

    builder.set_starting_state(start_node)

    tm: TuringMachine = builder.create()

    assert len(tm.tapes) == 1
    assert tm.num_states == current_num_states
    assert len(tm.transitions) == current_num_states
    assert len(tm.transitions[0]) == 1

    transition: Transition = tm.transitions[0][0]

    assert transition.new_state == end_node
    assert transition.accept_condition == {tape_index: Symbol.ZERO}
    assert transition.symbols_to_write == {tape_index: Symbol.ONE}
    assert transition.tape_shifts == {tape_index: Shift.RIGHT}
