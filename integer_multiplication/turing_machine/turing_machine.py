"""Definition of multi-tape Turing machine used to model multiplication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.shift import Shift
from integer_multiplication.turing_machine.tape import Tape

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.symbol import Symbol
    from integer_multiplication.turing_machine.transition import Transition


class TuringMachine:
    """Model multi-tape Turing machine.

    This Turing machine has the following traits:
        - fixed number of two-way infinite tapes
        - 3 symbols: BLANK, ZERO, and ONE
        - a tape head can shift left, right, or not shift
    """

    def __init__(
        self,
        *,
        num_states: int,
        num_tapes: int,
        starting_state: int,
        halting_states: set[int],
        transitions: list[list[Transition]],
    ) -> None:
        """Initialize beginning state of Turing machine with empty tapes.

        :param num_states: Number of states Turing machine has, including any
            halting states.
        :param num_tapes: Number of tapes
        :param starting_state: Number at least 0 and less than num_states that
            describes which state to start running from
        :param halting_states: set of states, each in range [0, num_states),
            that are declared to be halting. When running the Turing machine,
            if the current state is one of the halt states, then the Turing
            machine halts
        :param transitions: a mapping from a state to a list of possible
            transitions.
        """
        self.num_states: int = num_states
        self.tapes: list[Tape] = [Tape() for i in range(num_tapes)]
        self.starting_state: int = starting_state
        self.halting_states: set[int] = halting_states
        self.transitions: list[list[Transition]] = transitions

        # scratch variables when running the Turing Machine
        self.num_steps: int = 0
        self.current_state: int = starting_state
        self.one_halting_state: int = next(iter(halting_states))

    def is_halted(self) -> bool:
        """Return true if current state is a halting state.

        :return: True if current state of Turing machine is a halting state
        """
        return self.current_state in self.halting_states

    def read_tape_contents(self) -> str:
        """Return each tape head contents, concatenated together as a string.

        :return: the tape head symbols concatenated in order as a string
        """
        return "".join(tape.read().value for tape in self.tapes)

    def set_input_tape_values(self, symbols: list[Symbol]) -> None:
        """Set the initial tape contents of the 'input' tape.

        The 'input' tape will be the first tape, i.e. self.tapes[0].
        For Turing machines computing a function f: N^k -> N with k inputs,
        the k inputs should be in the standard binary format, separated
        by a single blank between inputs.

        This should not be called after the machine has started running.

        :param symbols: list of Symbols to be written on the first tape
        """
        if self.num_steps > 0:
            error_msg: str = (
                "Cannot set input tape values after it has started running."
            )
            raise RuntimeError(error_msg)

        for symbol in symbols:
            self.tapes[0].write(symbol)
            self.tapes[0].shift(Shift.RIGHT)

    def step(self) -> None:
        """Perform a single step of the Turing Machine.

        Given its current state and its tape contents, first find the list
        of all valid transitions from the current state.

        Then for each possible transition, check if the tape contents
        matches the transition's accept condition. If so, use the transition's
        information on next state, the new tape contents, and where to shift
        the tape heads.

        If no match is found, then the transition to a halting state is assumed.
        """
        possible_transitions: list[Transition] = self.transitions[self.current_state]
        for transition in possible_transitions:
            if transition.matches(self.read_tape_contents()):
                self.current_state = transition.new_state

                for tape_index, symbol in transition.symbols_to_write.items():
                    self.tapes[tape_index].write(symbol)
                for tape_index, shift in transition.tape_shifts.items():
                    self.tapes[tape_index].shift(shift)

                self.num_steps += 1
                return

        if not self.is_halted():
            # unspecified transition means default to a halted state
            self.current_state = self.one_halting_state
            self.num_steps += 1

    def run(self, *, max_steps: int | None = None) -> int:
        """Run the Turing machine until it halts.

        :param max_steps: the maximum number of steps the Turing
            machine should run for before returning. If None, the machine
            will run until it halts. Default None.
        :return: number of steps the Turing machine took
        """
        while not self.is_halted() and (
            max_steps is None or self.num_steps < max_steps
        ):
            self.step()

        return self.num_steps

    def reset(self) -> None:
        """Set all blank tapes, current_state to initial state, reset steps counter.

        Note that this erases any existing input tape cells.
        """
        num_tapes: int = len(self.tapes)
        self.tapes = [Tape() for i in range(num_tapes)]
        self.current_state = self.starting_state
        self.num_steps = 0
