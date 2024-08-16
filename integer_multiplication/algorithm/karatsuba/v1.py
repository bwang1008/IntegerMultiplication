"""Implementation of Karatsuba's multiplication algorithm on a Turing machine."""

from __future__ import annotations


def create_karatsuba_turing_machine() -> None:
    """Generate Turing machine that implements Karatsuba's algorithm.

    Method:
        1. Copy first input into arg1 tape, copy second input into arg2 tape.
        2. Write a 1 in recursion_counter tape.
        3. If recursion_counter tape is a 1:
            1. Let x be arg1 value, and y be arg2 value. If x or y are length 1,
                copy answer (y or x) into results tape. Write a blank on the
                recursion_counter tape and move left.
            2. Otherwise x, y are both length > 1. Split x into 2 roughly equal
                parts: x1, x0.
            3. Write 1s onto base tape, same length as x0.
            4. Split y into y1 and y0, where len(y0) is the same as len(x0).
            4. On the recursion_counter tape,
                1. Move right
                2. Write a 0, move right.
                3. Write a 1, move right.
                4. Write a 1, move right.
                5. Write a 1, don't move.
            5. Push x1 into arg1 tape, y1 into arg2 tape.
            6. Push x0 into arg1 tape, y0 into arg2 tape.
            7. Push (x0 + x1) into arg1 tape, (y0 + y1) into arg2 tape.
            8. Go back to step 3 (outer).
        4. If recursion_counter tape is a 0:
            1. Pop 3 values from the results tape, as z3, z0, and z2.
            2. Pop value B from the base tape.
            3. Compute z1 = z3 - z0 - z2
            4. Pad z2 with added trailing 0s, twice as many as 1s in B
            5. Pad z1 with trailing 0s, with as many 0s 1s as B.
            6. Compute result = z2 + z1 + z0
            7. Push result into results tape.
        5. If recursion_counter tape is a blank:
            1. Copy word on results tape into output and halt.
    """
