# Lab 12 – Program to Implement Booth's Algorithm

## Objective
Implement Booth's algorithm as a clean, tested program and verify it against a set of signed multiplication cases.

## Implementation

### File: `booth.py`
The program implements the standard N-bit Booth multiplier with:
- Automatic bit-width selection based on the operand magnitudes
- A built-in test suite covering positive × positive, negative × positive, positive × negative, and negative × negative
- An interactive mode for manual testing

### Core Function
```python
def booth_multiply(M: int, Q: int, n: int) -> int:
    """Multiply signed integers M and Q using Booth's algorithm.
    Returns the signed product."""
```

### Algorithm (clean pseudocode)
```
A = 0,  Q_reg = Q,  Q_m1 = 0

repeat n times:
    q0 = Q_reg[0]   # LSB
    if (q0, Q_m1) == (1, 0):  A = A - M
    if (q0, Q_m1) == (0, 1):  A = A + M

    Q_m1  = Q_reg[0]
    Q_reg = (Q_reg >> 1) | (A[0] << n-1)   # ARS of Q using A's LSB
    A     = arithmetic_right_shift(A, 1)

return signed_value({A, Q_reg})
```

## Running

```bash
cd labs/
python3 lab12_booth_program/booth.py                  # run test suite
python3 lab12_booth_program/booth.py -3 7             # -3 × 7 = -21
python3 lab12_booth_program/booth.py 100 -50 8        # 8-bit: 100 × -50
python3 lab12_booth_program/booth.py --interactive    # interactive prompt
```

### Test Suite Output (expected)
```
     M       Q   bits      Result    Expected    OK
  ──────────────────────────────────────────────────
     -3       7      4         -21         -21     ✓
      7      -3      4         -21         -21     ✓
      3       5      4          15          15     ✓
     -4      -3      4          12          12     ✓
      6       7      4          42          42     ✓
  ...
  All tests passed.
```

## Lab Tasks
1. Run the test suite and record the output.
2. Add a test case for `M = −8, Q = −8` using 5-bit width; explain why 4 bits is insufficient.
3. Modify `booth_multiply` to return both the product and the total number of add/subtract operations performed.
4. Compare the operation count with a standard unsigned multiplier for the same inputs.

## Questions
1. Why is the result stored in `{A, Q}` (2N bits) rather than a single N-bit register?
   - Multiplying two N-bit signed numbers can produce a result up to 2N bits wide (e.g., −8 × −8 = 64 in 4-bit = 0b1000000, needs 7 bits). Using {A, Q} as a 2N-bit register ensures the product is never truncated for any valid signed input pair. Intermediate partial products also need 2N bits of working space.
2. What happens if you use too few bits (n) for the given operands?
   - The operands are treated as if they fit in n-bit two's complement. If a value is outside the representable range for n bits, the upper bits are silently discarded — the algorithm runs on the truncated value and produces a wrong answer. E.g., using 4 bits for M=−8, Q=−8: −8 is the most-negative 4-bit value (1000); M×Q should be 64, but {A,Q} after 4 iterations stores the 8-bit result correctly only if n=5 or more.
3. Implement the check: for which input pair is the operation count maximised?
   - The maximum occurs when Q has alternating bits (01010101… or 10101010…). To find it programmatically:
   ```python
   max_ops, worst_Q = 0, 0
   for q in range(-(2**(n-1)), 2**(n-1)):
       _, ops = booth_multiply(1, q, n)  # count ops with trivial M=1
       if ops > max_ops:
           max_ops, worst_Q = ops, q
   print(f"Worst Q = {worst_Q} ({bin(worst_Q)}), ops = {max_ops}")
   ```
