"""Create Turing machines that implement integer multiplication algorithms.

Inputs are two positive integers written in the standard binary format.
For instance, 13 in decimal would be presented as "1101" because 13 = 8 + 4 + 1.
The bits are written with higher-order bits on the left and lower-order bits
on the right. The two arguments are to be written on the first tape of the
Turing machine, which will be designated the "input tape". This tape is read
only and should not have symbols written to it. There should be a single blank
between the two integers on the tape. At the start, the head of the input tape
should be at the left-most non-blank symbol, which is the highest-order bit
of the first argument.

The output should be the result of the integer multiplication of the two
positive integers in the input, written in the standard binary format.
This should be written to the second tape of the Turing machine, which will be
designated the output tape. Note that this implies these machines must have
at least 2 tapes. By the end of the computation, the head of the output tape
should be at the left-most non-blank symbol, which is the highest-order bit
of the multiplication result.
"""
