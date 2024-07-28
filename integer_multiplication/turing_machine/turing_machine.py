"""Definition of multi-tape Turing machine used to model multiplication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from integer_multiplication.turing_machine.tape import Tape

if TYPE_CHECKING:
    from integer_multiplication.turing_machine.symbol import Symbol


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
        transitions,
    ) -> None:
        """Initialize beginning state of Turing machine with empty tapes."""
        self.num_states: int = num_states
        self.tapes: list[Tape] = [Tape() for i in range(num_tapes)]
        self.starting_state: int = starting_state
        self.halting_states: set[int] = halting_states
        self.transitions = transitions

        # scratch variables when running the Turing Machine
        self.num_steps: int = 0
        self.current_state: int = starting_state

    def is_halted(self) -> bool:
        """Return true if current state is a halting state."""
        return self.current_state in self.halting_states

    def set_input_tape_values(self, symbols: list[Symbol]) -> None:
        """Set the initial tape contents of the 'input' tape.

        The 'input' tape will be the first tape, i.e. self.tapes[0].
        For Turing machines computing a function f: N^k -> N with k inputs,
        the k inputs should be in the standard binary format, separated
        by a single blank between inputs.

        This should not be called after the machine has started running.
        """
        if self.num_steps > 0:
            ...

        for symbol in symbols:
            self.tapes[0].write(symbol)

    def step(self) -> None:
        """Perform a single step of the Turing Machine.

        Given its current state and its tape contents, use its transition
        function to find the next state, the new tape contents, and where
        to shift the tape heads.
        """
        if self.is_halted():
            return

        self.num_steps += 1

    def run(self) -> int:
        """Run the Turing machine until it halts."""
        while not self.is_halted():
            self.step()

        return self.num_steps
