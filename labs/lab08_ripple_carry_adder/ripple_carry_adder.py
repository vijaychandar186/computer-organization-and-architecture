#!/usr/bin/env python3
"""Lab 8 – Ripple Carry Adder (RCA) simulation.

Chains N full adders in series. Carry ripples from LSB to MSB.

Run:
  python3 ripple_carry_adder.py              # demo: 4-bit and 8-bit examples
  python3 ripple_carry_adder.py <A> <B> [bits]  # custom addition
  Example: python3 ripple_carry_adder.py 13 11 4
"""

import sys


# ---------------------------------------------------------------------------
# Gate / Full Adder primitives (same as Lab 7)
# ---------------------------------------------------------------------------

def full_adder(a: int, b: int, cin: int) -> tuple[int, int]:
    s    = a ^ b ^ cin
    cout = (a & b) | (b & cin) | (a & cin)
    return s, cout


# ---------------------------------------------------------------------------
# Ripple Carry Adder
# ---------------------------------------------------------------------------

def ripple_carry_adder(a: int, b: int, n: int, cin: int = 0):
    """Add n-bit numbers a and b with initial carry cin.

    Returns (sum_bits, carry_chain, final_carry).
    sum_bits   – list of n sum bits, index 0 = LSB
    carry_chain – list of n carry-outs, one per stage
    """
    sum_bits: list[int] = []
    carry_chain: list[int] = []
    carry = cin

    for i in range(n):
        ai = (a >> i) & 1
        bi = (b >> i) & 1
        s, carry = full_adder(ai, bi, carry)
        sum_bits.append(s)
        carry_chain.append(carry)

    return sum_bits, carry_chain, carry


def bits_to_int(bits: list[int]) -> int:
    return sum(b << i for i, b in enumerate(bits))


def int_to_bits(val: int, n: int) -> list[int]:
    return [(val >> i) & 1 for i in range(n)]


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def format_bits(bits: list[int], sep: str = "") -> str:
    return sep.join(str(b) for b in reversed(bits))  # MSB first


def print_addition(a: int, b: int, n: int, cin: int = 0):
    sum_bits, carries, final_carry = ripple_carry_adder(a, b, n, cin)
    result = bits_to_int(sum_bits)
    overflow = final_carry

    a_bits = int_to_bits(a, n)
    b_bits = int_to_bits(b, n)

    print(f"\n{n}-bit Ripple Carry Addition")
    print(f"  A        = {format_bits(a_bits)}  ({a})")
    print(f"  B        = {format_bits(b_bits)}  ({b})")
    if cin:
        print(f"  Cin      = {cin}")
    print(f"  {'─' * (n + 12)}")

    carry_row = [cin] + carries[:-1]   # carries into each stage
    print(f"  Carries  = {format_bits(carry_row, ' ')}  (into each bit)")
    print(f"  Sum      = {format_bits(sum_bits)}  ({result})")
    print(f"  Cout     = {final_carry}  {'← overflow!' if overflow else ''}")

    print("\n  Stage-by-stage trace:")
    print(f"  {'Bit':>4}  {'A':>2}  {'B':>2}  {'Cin':>4}  {'Sum':>4}  {'Cout':>5}")
    print(f"  {'─'*30}")
    c = cin
    for i in range(n):
        ai = (a >> i) & 1
        bi = (b >> i) & 1
        s, c_out = full_adder(ai, bi, c)
        print(f"  {i:>4}  {ai:>2}  {bi:>2}  {c:>4}  {s:>4}  {c_out:>5}")
        c = c_out


def demo():
    print("=" * 45)
    print("Ripple Carry Adder Demo")
    print("=" * 45)

    # 4-bit examples
    print_addition(5, 3, 4)    # 0101 + 0011 = 1000
    print_addition(13, 11, 4)  # 1101 + 1011 = overflow
    print_addition(60, 20, 8)  # 8-bit
    print_addition(200, 100, 8) # overflow example


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) >= 3:
        a   = int(sys.argv[1])
        b   = int(sys.argv[2])
        n   = int(sys.argv[3]) if len(sys.argv) >= 4 else max(a, b).bit_length() + 1
        print_addition(a, b, n)
    else:
        demo()


if __name__ == "__main__":
    main()
