#!/usr/bin/env python3
"""Lab 11 – Booth's Algorithm: step-by-step trace.

Booth's algorithm multiplies two signed (2's complement) integers
by examining pairs of bits in the multiplier to decide whether to
add, subtract, or do nothing.

Run:
  python3 booth_trace.py              # demo with multiple examples
  python3 booth_trace.py <M> <Q> [bits]
  Example: python3 booth_trace.py -3 7 4
"""

import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_twos_complement(val: int, n: int) -> int:
    """Return the n-bit 2's complement representation of val as an integer."""
    if val < 0:
        return val + (1 << n)
    return val & ((1 << n) - 1)


def to_signed(bits: int, n: int) -> int:
    """Interpret an n-bit integer as a signed value."""
    if bits >= (1 << (n - 1)):
        return bits - (1 << n)
    return bits


def fmt_bits(val: int, n: int) -> str:
    return format(val & ((1 << n) - 1), f"0{n}b")


# ---------------------------------------------------------------------------
# Booth's Algorithm
# ---------------------------------------------------------------------------

def booth_trace(M: int, Q: int, n: int):
    """Perform Booth's algorithm with full step-by-step trace.

    M  = multiplicand (signed)
    Q  = multiplier   (signed)
    n  = bit width (including sign bit)
    """
    # Represent in n-bit 2's complement
    M_bits = to_twos_complement(M, n)
    neg_M  = to_twos_complement(-M, n)

    # Registers: A (accumulator), Q_reg, Q_{-1} (one extra bit)
    A  = 0                               # n-bit accumulator, starts 0
    Q_reg = to_twos_complement(Q, n)     # n-bit multiplier register
    Q_m1  = 0                            # Q_{-1} bit, starts 0

    mask = (1 << n) - 1

    print(f"\nBooth's Algorithm Trace")
    print(f"  M  = {M:+d}  =  {fmt_bits(M_bits, n)}  ({n}-bit 2's complement)")
    print(f"  Q  = {Q:+d}  =  {fmt_bits(Q_reg, n)}")
    print(f"  -M =  {-M:+d}  =  {fmt_bits(neg_M, n)}")
    print(f"  n  = {n} bits  →  {n} iterations")
    print()

    header = (f"  {'Step':>5}  {'A':>{n}}  {'Q':>{n}}  {'Q-1':>3}  "
              f"{'Q0':>3}  {'Action':<20}  Note")
    sep = "  " + "─" * (len(header) - 2)
    print(header)
    print(sep)

    def print_state(step, action, note=""):
        print(f"  {step:>5}  {fmt_bits(A,n)}  {fmt_bits(Q_reg,n)}  "
              f"  {Q_m1:1d}  "
              f"  {(Q_reg&1):1d}  {action:<20}  {note}")

    print_state("Init", "initialise", f"A={fmt_bits(A,n)} Q={fmt_bits(Q_reg,n)}")

    for step in range(1, n + 1):
        q0  = Q_reg & 1          # LSB of Q
        q_1 = Q_m1               # previous Q_{-1}
        pair = (q0, q_1)

        if pair == (1, 0):
            action = f"A = A - M"
            A = (A - M_bits) & mask
            note = f"→ A={fmt_bits(A,n)}"
        elif pair == (0, 1):
            action = f"A = A + M"
            A = (A + M_bits) & mask
            note = f"→ A={fmt_bits(A,n)}"
        else:
            action = "no operation"
            note = ""

        # Arithmetic right shift of {A, Q, Q_{-1}} by 1
        new_Q_m1  = Q_reg & 1
        new_Q_reg = ((Q_reg >> 1) | ((A & 1) << (n - 1))) & mask
        sign_bit  = (A >> (n - 1)) & 1   # preserve sign
        new_A     = ((A >> 1) | (sign_bit << (n - 1))) & mask

        Q_m1  = new_Q_m1
        Q_reg = new_Q_reg
        A     = new_A

        print_state(f"{step}", action, note + f" | after ARS: A={fmt_bits(A,n)}")

    print(sep)
    # Result is in {A, Q_reg} (2n bits)
    result_bits = (A << n) | Q_reg
    result_signed = to_signed(result_bits, 2 * n)

    print(f"\n  Result  = A:Q = {fmt_bits(A,n)} {fmt_bits(Q_reg,n)}  ({result_signed})")
    print(f"  Expected: {M} × {Q} = {M * Q}")
    match = "✓" if result_signed == M * Q else "✗ MISMATCH"
    print(f"  Check   : {match}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) >= 3:
        M = int(sys.argv[1])
        Q = int(sys.argv[2])
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else 4
        booth_trace(M, Q, n)
    else:
        # Demo: multiple examples
        examples = [
            (-3,  7, 4),   # common textbook example
            ( 7, -3, 4),
            ( 3,  5, 4),
            (-4, -3, 4),
            ( 6,  7, 4),
        ]
        for M, Q, n in examples:
            booth_trace(M, Q, n)
            print()


if __name__ == "__main__":
    main()
