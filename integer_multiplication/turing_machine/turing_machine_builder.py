"""Help create instances of TuringMachine."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.turing_machine import TuringMachine

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.transition import Transition


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

    def get_or_create_state(
        self, *, name: str | None = None, halting: bool = False
    ) -> int:
        """Fetch an existing state of create a new state.

        If a name is provided and was used before, that node is returned.
        Otherwise, a new state is created with that name.

        :param name: name of the state. If this name was used before, then
            the state associated with the name is returned. Otherwise, a new
            node is created with the name associated with it.
        :param halting: if the new state should be a halting state or not.
            Has no effect if fetching an existing state.
        :return: int representing existing / new state
        """
        if name is not None:
            if name in self.named_states:
                return self.named_states[name]
            self.named_states[name] = self.num_states
            return self.create_state(halting=halting)

        return self.create_state(halting=halting)

    def set_starting_state(self, starting_state: int) -> None:
        """Designate a particular state as the starting state of the machine.

        The Turing machine cannot be created without setting a starting state.

        :param starting_state: which state to be used as the starting state.
        """
        self.starting_state = starting_state

    def create(self) -> TuringMachine:
        """Create an instance of TuringMachine.

        A starting state should be set first with set_starting_state() before
        calling this method.
        """
        if self.starting_state is None:
            error_msg: str = "Must set starting_state before creating Turing machine."
            raise RuntimeError(error_msg)

        return TuringMachine(
            num_states=self.num_states,
            num_tapes=self.num_tapes,
            starting_state=self.starting_state,
            halting_states=self.halting_states,
            transitions=[self.transitions[i] for i in range(self.num_tapes)],
        )
