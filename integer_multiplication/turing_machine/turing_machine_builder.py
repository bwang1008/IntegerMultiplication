"""Help create instances of TuringMachine."""

from __future__ import annotations

import itertools
from collections import defaultdict
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.symbol import Symbol
from integer_multiplication.turing_machine.transition import (
    SingleTapeTransition,
    Transition,
)
from integer_multiplication.turing_machine.turing_machine import TuringMachine

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.shift import Shift


class TuringMachineBuilder:
    """Iteratively build up a TuringMachine instance."""

    def __init__(self) -> None:
        """Initialize with no states, no tapes, no transitions."""
        self.num_states: int = 0
        self.num_tapes: int = 0
        self.transitions: defaultdict[int, list[Transition]] = defaultdict(list)
        self.named_states: dict[str, int] = {}
        self.named_tapes: dict[str, int] = {}
        self.starting_state: int | None = None
        self.halting_states: set[int] = set()

    def create_state(self, *, halting: bool = False) -> int:
        """Create a new state index.

        :param halting: if the new state should be a halting state or not
        :return: int representing new state
        """
        new_state_index: int = self.num_states
        if halting:
            self.halting_states.add(new_state_index)
        self.num_states += 1
        return new_state_index

    def get_or_create_tape_index(self, *, name: str) -> int:
        """Fetch an existing tape index or create a new tape.

        :param name: name associated with the tape. If used before, the existing
            tape index is returned. Otherwise a new tape is created with the
            associated name.
        :return: Index of existing / new tape
        """
        if name in self.named_tapes:
            return self.named_tapes[name]

        new_tape_index: int = self.num_tapes
        self.named_tapes[name] = new_tape_index
        self.num_tapes += 1
        return new_tape_index

    def set_starting_state(self, starting_state: int) -> None:
        """Designate a particular state as the starting state of the machine.

        The Turing machine cannot be created without setting a starting state.

        :param starting_state: which state to be used as the starting state.
        """
        self.starting_state = starting_state

    def add_transition(
        self,
        old_state: int,
        new_state: int,
        accept_condition: dict[int, Symbol | list[Symbol]],
        symbols_to_write: dict[int, Symbol],
        tape_shifts: dict[int, Shift],
    ) -> None:
        """Add transition from old to new state, using simpler syntax.

        :param old_state: which state the Turing machine is in to consider
            this transition
        :param new_state: which state to move to if accept_condition matches
            the tape input
        :param accept_condition: mapping from tape index to expected symbol
            or to a list of symbols. If a list of
            symbols is provided, then a transition is added for every possible
            value. Note that this means a Cartesian product of every list in
            accept_condition is used to create all transitions. For example,
            accept_condition := {0: "1", 3: "0"} means to take this transition
            if tape 0 has a "1" and tape 3 has a "0", while
            accept_condition := {0: ["1", "0"], 3: ["0"]} means create one
            transition for when tape 0 has a "1" and tape 3 has a "0", and
            create another transition for when tape 0 has a "0" and tape 3 has
            a "0". This is useful for a situation like detecting if tape 0 is
            current not a blank: set accept_condition := {0: ["0", "1"]} to mean
            "whenever tape 0 is a 0 or a 1".
        :param symbols_to_write: mapping from tape index to symbol to write.
        :param tape_shifts: mapping from tape index to which way the heads of the
            tapes should move.
        """
        accept_condition_lists: list[list[Symbol]] = []
        for val in accept_condition.values():
            if isinstance(val, Symbol):
                accept_condition_lists.append([val])
            elif isinstance(val, list):
                accept_condition_lists.append(val)

        tape_indices: list[int] = list(accept_condition)
        for cartesian_product in itertools.product(*accept_condition_lists):
            accept_condition_instance: dict[int, Symbol] = dict(
                zip(tape_indices, cartesian_product)
            )
            self.transitions[old_state].append(
                Transition(
                    new_state=new_state,
                    accept_condition=accept_condition_instance,
                    symbols_to_write=symbols_to_write,
                    tape_shifts=tape_shifts,
                )
            )

    def add_single_tape_transition(
        self,
        old_state: int,
        new_state: int,
        tape_index: int,
        single_transition: SingleTapeTransition,
    ) -> None:
        """Create a transition between old state to new state based on one tape.

        Often not all of the tapes are used when considering to take a transition
        at the current state. When only one tape is considered, this effectively
        reduces to a transition from a 1-tape Turing machine. Then the machinery
        for specifying which tape indices to read/write/shift do not need to be
        specified so many times, leading to a more simplified interface.

        :param old_state: which state the Turing machine is in to consider
            this transition
        :param new_state: the state the Turing machine should be in when taking
            this transition
        :param tape_index: which tape index to read/write/shift from
        :param single_transition: container object with what character to
            expect to accept this transition, what new symbol to write, and
            how to shif tape_index's tape head
        """
        self.add_transition(
            old_state,
            new_state=new_state,
            accept_condition=(
                {tape_index: single_transition.accept_condition}
                if single_transition.accept_condition is not None
                else {}
            ),
            symbols_to_write=(
                {tape_index: single_transition.symbol_to_write}
                if single_transition.symbol_to_write is not None
                else {}
            ),
            tape_shifts=(
                {tape_index: single_transition.shift}
                if single_transition.shift is not None
                else {}
            ),
        )

    def create(self) -> TuringMachine:
        """Create an instance of TuringMachine.

        A starting state should be set first with set_starting_state() before
        calling this method.

        :return: TuringMachine instance corresponding to states/tapes/transitions
            previously added
        """
        if self.starting_state is None:
            error_msg: str = "Must set starting_state before creating Turing machine."
            raise RuntimeError(error_msg)

        return TuringMachine(
            num_states=self.num_states,
            num_tapes=self.num_tapes,
            starting_state=self.starting_state,
            halting_states=self.halting_states,
            transitions=[self.transitions[i] for i in range(self.num_states)],
        )
