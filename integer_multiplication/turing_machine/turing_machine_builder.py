"""Help create instances of TuringMachine."""

from __future__ import annotations

from collections import defaultdict

from integer_multiplication.turing_machine.transition import (
    SingleTapeTransition,
    Transition,
)
from integer_multiplication.turing_machine.turing_machine import TuringMachine


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
        """Fetch an existing state or create a new state.

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

    def add_transition_general(self, old_state: int, transition: Transition) -> None:
        """Add a Transition instance associated with old_state.

        :param old_state: which state the Turing machine is in to consider
            this transition
        :param transition: Transition instance detailing which new state to
            move to, which tape indices need to be read to check acceptance,
            which new symbols to write on the tapes, and which way to shift
            the tape heads
        """
        self.transitions[old_state].append(transition)

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
        self.add_transition_general(
            old_state,
            Transition(
                new_state=new_state,
                accept_condition={tape_index: single_transition.accept_condition},
                symbols_to_write={tape_index: single_transition.symbol_to_write},
                tape_shifts={tape_index: single_transition.shift},
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
            transitions=[self.transitions[i] for i in range(self.num_tapes)],
        )
