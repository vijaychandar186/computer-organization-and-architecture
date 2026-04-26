#!/usr/bin/env python3
"""Lab 9 – Carry Look-Ahead Adder (CLA) simulation.

Computes all carries in parallel using Generate and Propagate signals,
then produces all sum bits simultaneously—eliminating the ripple delay.

Run:
  python3 carry_lookahead_adder.py              # demo
  python3 carry_lookahead_adder.py <A> <B> [bits]
  Example: python3 carry_lookahead_adder.py 13 11 4
"""

import sys


# ---------------------------------------------------------------------------
# CLA core
# ---------------------------------------------------------------------------

def carry_lookahead_adder(a: int, b: int, n: int, cin: int = 0):
    """Add n-bit numbers using carry look-ahead.

    Returns (sum_int, carries, generate_bits, propagate_bits, overflow).
    """
    # Step 1 – compute per-bit Generate (G) and Propagate (P)
    G = [(( a >> i) & 1) & ((b >> i) & 1) for i in range(n)]   # G_i = A_i AND B_i
    P = [(( a >> i) & 1) ^ ((b >> i) & 1) for i in range(n)]   # P_i = A_i XOR B_i

    # Step 2 – look-ahead carry computation
    # C_0 = cin
    # C_{i+1} = G_i OR (P_i AND C_i)
    C = [0] * (n + 1)
    C[0] = cin
    for i in range(n):
        C[i + 1] = G[i] | (P[i] & C[i])

    # Step 3 – sum bits
    # S_i = P_i XOR C_i  (same as A_i XOR B_i XOR C_i)
    S = [P[i] ^ C[i] for i in range(n)]

    result   = sum(S[i] << i for i in range(n))
    overflow = C[n]

    return result, C, G, P, overflow


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def int_to_bits(val: int, n: int) -> list[int]:
    return [(val >> i) & 1 for i in range(n)]


def fmt(bits: list[int]) -> str:
    return "".join(str(b) for b in reversed(bits))


def print_cla(a: int, b: int, n: int, cin: int = 0):
    result, C, G, P, overflow = carry_lookahead_adder(a, b, n, cin)

    a_bits = int_to_bits(a, n)
    b_bits = int_to_bits(b, n)
    s_bits = int_to_bits(result, n)

    print(f"\n{n}-bit Carry Look-Ahead Addition")
    print(f"  A = {fmt(a_bits)}  ({a})")
    print(f"  B = {fmt(b_bits)}  ({b})")
    if cin:
        print(f"  Cin = {cin}")
    print()

    print(f"  {'Bit':>4}  {'A':>2}  {'B':>2}  {'G':>2}  {'P':>2}  {'Cin':>4}  {'Sum':>4}  {'Cout':>5}")
    print(f"  {'─'*38}")
    for i in range(n):
        ai = (a >> i) & 1
        bi = (b >> i) & 1
        print(f"  {i:>4}  {ai:>2}  {bi:>2}  {G[i]:>2}  {P[i]:>2}  {C[i]:>4}  {s_bits[i]:>4}  {C[i+1]:>5}")

    print(f"\n  Sum  = {fmt(s_bits)}  ({result})")
    print(f"  Cout = {overflow}  {'← overflow!' if overflow else ''}")

    # Show the look-ahead carry equations
    print("\n  Look-Ahead Carry Equations (parallel, no ripple):")
    for i in range(1, n + 1):
        terms = [f"G{i-1}"]
        prop  = f"P{i-1}"
        for j in range(i - 1, 0, -1):
            prop_chain = "".join(f"P{k}" for k in range(j, i))
            terms.append(f"{prop_chain}·G{j-1}")
        prop_all = "".join(f"P{k}" for k in range(i))
        terms.append(f"{prop_all}·C0")
        print(f"  C{i} = " + " + ".join(terms))


def demo():
    print("=" * 50)
    print("Carry Look-Ahead Adder Demo")
    print("=" * 50)
    print_cla(5, 3, 4)
    print_cla(13, 11, 4)
    print_cla(170, 85, 8)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) >= 3:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else max(a, b).bit_length() + 1
        print_cla(a, b, n)
    else:
        demo()


if __name__ == "__main__":
    main()
