## Grade-School Multiplication Algorithm

The `v1.py` Turing machine has 4 tapes and 6 states. When measured on inputs of the form `(2^n-1) * (2^n - 1)`, the number of steps taken are shown in the following table:

| n | Steps taken |
| -- | -- |
| 1 | 11 |
| 2 | 24 |
| 3 | 40 |
| 4 | 60 |
| 5 | 84 |
| 6 | 112 |
| 7 | 144 |
| 8 | 180 |
| 9 | 220 |
| 10 | 264 |

indicating that for `n >= 2`, the numbers of steps the Turing machine takes to multiply `(2^n - 1) * (2^n - 1)` is `2n^2 + 6n + 4`. The reason why one less step is taken for `n = 1` is because the product only takes one bit, while for `n >= 2`, the number of bits taken is `2n`.
