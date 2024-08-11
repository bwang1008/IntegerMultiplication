"""Tests behavior of TuringMachineBuilder methods."""

from integer_multiplication.turing_machine.turing_machine_builder import (
    TuringMachineBuilder,
)


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
