#!/usr/bin/env python3
"""Lab 13 – Carry Save Adder (CSA) and Carry Save Multiplication.

A Carry Save Adder reduces three N-bit numbers to two N-bit numbers
(sum vector + carry vector) in O(1) time, deferring carry propagation.
This is used in array multipliers and other hardware to speed up
multi-operand addition.

Run:
  python3 carry_save.py                     # demo
  python3 carry_save.py <A> <B> <C>         # add three numbers
  python3 carry_save.py --multiply <M> <Q>  # CSA-based multiplication
"""

import sys


# ---------------------------------------------------------------------------
# Gate primitives
# ---------------------------------------------------------------------------

def full_adder_bits(a: int, b: int, cin: int) -> tuple[int, int]:
    return a ^ b ^ cin, (a & b) | (b & cin) | (a & cin)


# ---------------------------------------------------------------------------
# Carry Save Adder (single stage)
# ---------------------------------------------------------------------------

def carry_save_add(A: int, B: int, C: int, n: int) -> tuple[int, int]:
    """Add three n-bit integers using a Carry Save Adder.

    Returns (sum_vector, carry_vector) such that:
        A + B + C  =  sum_vector + (carry_vector << 1)

    The carry vector must be shifted left 1 bit before the final add.
    """
    S = 0  # sum bits
    K = 0  # carry bits

    for i in range(n):
        ai = (A >> i) & 1
        bi = (B >> i) & 1
        ci = (C >> i) & 1
        s, k = full_adder_bits(ai, bi, ci)
        S |= s << i
        K |= k << i

    return S, K


def csa_final_add(S: int, K: int) -> int:
    """Combine sum and carry vectors using a final ripple-carry add."""
    return S + (K << 1)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def fmt(val: int, n: int) -> str:
    return format(val & ((1 << n) - 1), f"0{n}b")


def print_csa(A: int, B: int, C: int, n: int):
    S, K = carry_save_add(A, B, C, n)
    result = csa_final_add(S, K)

    print(f"\nCarry Save Addition  ({n}-bit)")
    print(f"  A = {fmt(A, n)}  ({A})")
    print(f"  B = {fmt(B, n)}  ({B})")
    print(f"  C = {fmt(C, n)}  ({C})")
    print()
    print(f"  CSA Stage:")
    print(f"  S (sum vector)   = {fmt(S, n)}  ({S})")
    print(f"  K (carry vector) = {fmt(K, n)}  ({K})")
    print(f"  K << 1           = {fmt(K<<1, n+1)}  ({K<<1})")
    print()
    print(f"  Final add: S + (K<<1) = {result}")
    print(f"  Expected : A+B+C      = {A+B+C}")
    print(f"  Match    : {'✓' if result == A+B+C else '✗'}")


# ---------------------------------------------------------------------------
# CSA-based Multiplication (Carry Save Array Multiplier)
# ---------------------------------------------------------------------------

def csa_multiply(M: int, Q: int, n: int):
    """Multiply two unsigned n-bit numbers using a CSA tree.

    Generates partial products and reduces them with CSA stages,
    finishing with a final ripple-carry add.

    Returns (product, trace) where trace lists each CSA reduction step.
    """
    M_bits = [(M >> i) & 1 for i in range(n)]
    Q_bits = [(Q >> i) & 1 for i in range(n)]

    # Generate partial products: PP[i] = M * Q_bits[i] (shifted left by i)
    partial_products = []
    for i in range(n):
        pp = 0
        for j in range(n):
            pp |= (M_bits[j] & Q_bits[i]) << j
        partial_products.append(pp << i)

    trace = [list(partial_products)]

    # Reduce using CSA tree until 2 operands remain
    operands = list(partial_products)
    while len(operands) > 2:
        new_operands = []
        i = 0
        while i + 2 < len(operands):
            S, K = carry_save_add(operands[i], operands[i+1], operands[i+2], 2*n)
            new_operands.append(S)
            new_operands.append(K << 1)
            i += 3
        while i < len(operands):
            new_operands.append(operands[i])
            i += 1
        operands = new_operands
        trace.append(list(operands))

    product = sum(operands)
    return product, trace


def print_csa_multiply(M: int, Q: int, n: int):
    product, trace = csa_multiply(M, Q, n)
    expected = M * Q

    print(f"\nCSA-based Multiplication  ({n}-bit)")
    print(f"  M = {fmt(M, n)}  ({M})")
    print(f"  Q = {fmt(Q, n)}  ({Q})")
    print()
    print(f"  Partial Products:")
    for i, pp in enumerate(trace[0]):
        print(f"    PP[{i}] = {fmt(pp, 2*n)}  ({pp})")

    if len(trace) > 1:
        print(f"\n  CSA Reduction Stages:")
        for s, stage in enumerate(trace[1:], 1):
            print(f"  Stage {s}:")
            for j, v in enumerate(stage):
                print(f"    [{j}] = {fmt(v, 2*n)}  ({v})")

    print(f"\n  Product  = {product}")
    print(f"  Expected = {expected}")
    print(f"  Match    : {'✓' if product == expected else '✗'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if "--multiply" in sys.argv:
        idx = sys.argv.index("--multiply")
        if idx + 2 < len(sys.argv):
            M = int(sys.argv[idx + 1])
            Q = int(sys.argv[idx + 2])
            n = int(sys.argv[idx + 3]) if idx + 3 < len(sys.argv) else max(M, Q).bit_length()
            print_csa_multiply(M, Q, n)
        else:
            print("Usage: carry_save.py --multiply <M> <Q> [bits]")
        return

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) >= 3:
        A, B, C = int(args[0]), int(args[1]), int(args[2])
        n = max(A, B, C).bit_length() + 1
        print_csa(A, B, C, n)
        return

    # Demo
    print("=" * 50)
    print("Carry Save Adder Demo")
    print("=" * 50)
    print_csa(13, 11, 7, 5)
    print_csa(15, 15, 15, 5)

    print("\n" + "=" * 50)
    print("CSA-based Multiplication Demo")
    print("=" * 50)
    print_csa_multiply(6, 5, 4)
    print_csa_multiply(13, 11, 4)
    print_csa_multiply(7, 7, 4)


if __name__ == "__main__":
    main()
