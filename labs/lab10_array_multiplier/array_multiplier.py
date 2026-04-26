#!/usr/bin/env python3
"""Lab 10 – Array Multiplier simulation.

An N×N array multiplier computes A × B using:
  - An AND gate array to generate partial products
  - A triangle array of Full Adders to accumulate them

Run:
  python3 array_multiplier.py              # demo
  python3 array_multiplier.py <A> <B> [bits]
  Example: python3 array_multiplier.py 6 5 4
"""

import sys


# ---------------------------------------------------------------------------
# Gate primitives
# ---------------------------------------------------------------------------

def AND(a: int, b: int) -> int: return a & b

def full_adder(a: int, b: int, cin: int) -> tuple[int, int]:
    s    = a ^ b ^ cin
    cout = (a & b) | (b & cin) | (a & cin)
    return s, cout


# ---------------------------------------------------------------------------
# Array Multiplier
# ---------------------------------------------------------------------------

def array_multiplier(a: int, b: int, n: int):
    """Multiply two n-bit numbers using an array of AND gates and FAs.

    Returns (product, partial_products).
    partial_products[i][j] = bit j of partial product i (= A[j] AND B[i]).
    """
    a_bits = [(a >> i) & 1 for i in range(n)]
    b_bits = [(b >> i) & 1 for i in range(n)]

    # Step 1 – AND gate array: PP[i][j] = a_bits[j] AND b_bits[i]
    PP = [[AND(a_bits[j], b_bits[i]) for j in range(n)] for i in range(n)]

    # Step 2 – accumulate partial products row by row
    # Start with the first partial product row
    # acc[k] holds the current accumulated sum bit at position k (0 = LSB)
    # We work with 2n bits of precision.

    acc = [0] * (2 * n)

    # Initialise with PP[0] (no shifting needed, it represents A * b_bits[0])
    for j in range(n):
        acc[j] = PP[0][j]

    # Add PP[i] (shifted left by i) to accumulator
    for i in range(1, n):
        carry = 0
        for j in range(n):
            pos = i + j
            s, carry = full_adder(acc[pos], PP[i][j], carry)
            acc[pos] = s
        # propagate remaining carry
        pos = i + n
        while carry and pos < 2 * n:
            s, carry = full_adder(acc[pos], 0, carry)
            acc[pos] = s
            pos += 1

    product = sum(acc[k] << k for k in range(2 * n))
    return product, PP


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def fmt_bits(bits: list[int]) -> str:
    return "".join(str(b) for b in reversed(bits))


def print_multiplication(a: int, b: int, n: int):
    product, PP = array_multiplier(a, b, n)

    a_bits = [(a >> i) & 1 for i in range(n)]
    b_bits = [(b >> i) & 1 for i in range(n)]

    print(f"\n{n}-bit × {n}-bit Array Multiplier")
    print(f"  A = {fmt_bits(a_bits)}  ({a})")
    print(f"  B = {fmt_bits(b_bits)}  ({b})")
    print(f"  A × B = {a} × {b} = {product}")
    print()

    # Partial products table (long multiplication style)
    print(f"  Partial Products (PP[i] = A × B[i], shifted left by i):")
    width = 2 * n + 2
    for i in range(n):
        pp_bits = [0] * (2 * n)
        for j in range(n):
            pp_bits[i + j] = PP[i][j]
        label = f"PP[{i}] (×B[{i}]={b_bits[i]})"
        print(f"  {label:<18} = {''.join(str(pp_bits[k]) for k in range(2*n-1, -1, -1))}")

    # Result
    res_bits = [(product >> k) & 1 for k in range(2 * n)]
    print(f"  {'─' * (width + 20)}")
    print(f"  {'Product':<18} = {''.join(str(res_bits[k]) for k in range(2*n-1, -1, -1))}  ({product})")


def demo():
    print("=" * 50)
    print("Array Multiplier Demo")
    print("=" * 50)
    print_multiplication(6, 5, 4)   # 6×5=30
    print_multiplication(13, 11, 4) # 13×11=143
    print_multiplication(15, 15, 4) # 15×15=225
    print_multiplication(12, 10, 8) # 8-bit example


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) >= 3:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else max(a, b).bit_length()
        print_multiplication(a, b, n)
    else:
        demo()


if __name__ == "__main__":
    main()
