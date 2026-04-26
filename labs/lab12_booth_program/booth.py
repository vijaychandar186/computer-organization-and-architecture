#!/usr/bin/env python3
"""Lab 12 – Booth's Algorithm: clean program implementation.

Multiplies two signed integers using Booth's algorithm.
Supports arbitrary bit widths (must fit both operands as signed values).

Run:
  python3 booth.py                    # run built-in test suite
  python3 booth.py <M> <Q>            # multiply M × Q (auto-sized)
  python3 booth.py <M> <Q> <bits>     # explicit bit width
  python3 booth.py --interactive      # interactive prompt
"""

import sys


# ---------------------------------------------------------------------------
# Core algorithm
# ---------------------------------------------------------------------------

def booth_multiply(M: int, Q: int, n: int) -> int:
    """Multiply signed integers M and Q using Booth's algorithm.

    n must be large enough to represent both M and Q in 2's complement.
    Returns the signed product.
    """
    mask = (1 << n) - 1

    def tc(v: int) -> int:
        return v + (1 << n) if v < 0 else v & mask

    A     = 0
    Q_reg = tc(Q)
    Q_m1  = 0
    M_pos = tc(M)
    M_neg = tc(-M)

    for _ in range(n):
        q0, q_1 = Q_reg & 1, Q_m1
        if (q0, q_1) == (1, 0):
            A = (A + M_neg) & mask
        elif (q0, q_1) == (0, 1):
            A = (A + M_pos) & mask

        # Arithmetic right shift {A, Q, Q_{-1}}
        Q_m1  = Q_reg & 1
        Q_reg = ((Q_reg >> 1) | ((A & 1) << (n - 1))) & mask
        sign  = (A >> (n - 1)) & 1
        A     = ((A >> 1) | (sign << (n - 1))) & mask

    result_bits = (A << n) | Q_reg
    # Sign-extend 2n-bit result
    if result_bits >= (1 << (2 * n - 1)):
        return result_bits - (1 << (2 * n))
    return result_bits


def min_bits(M: int, Q: int) -> int:
    """Minimum bit width to represent both M and Q as signed values."""
    vals = [abs(M), abs(Q)]
    return max((v.bit_length() + 1 for v in vals), default=2)


# ---------------------------------------------------------------------------
# Test suite
# ---------------------------------------------------------------------------

def run_tests():
    cases = [
        (-3,  7, 4),
        ( 7, -3, 4),
        ( 3,  5, 4),
        (-4, -3, 4),
        ( 6,  7, 4),
        ( 0,  5, 4),
        ( 5,  0, 4),
        (-1, -1, 4),
        ( 7,  7, 4),
        (-8,  7, 5),
        (-8, -7, 5),
        (15, 15, 5),
        (100, -50, 8),
    ]
    print("Booth's Algorithm – Test Suite")
    print(f"  {'M':>6}  {'Q':>6}  {'bits':>5}  {'Result':>10}  {'Expected':>10}  {'OK':>4}")
    print("  " + "─" * 52)
    all_pass = True
    for M, Q, n in cases:
        result   = booth_multiply(M, Q, n)
        expected = M * Q
        ok       = result == expected
        all_pass = all_pass and ok
        mark     = "✓" if ok else "✗"
        print(f"  {M:>6}  {Q:>6}  {n:>5}  {result:>10}  {expected:>10}  {mark:>4}")
    print()
    print(f"  {'All tests passed.' if all_pass else 'SOME TESTS FAILED.'}")
    return all_pass


# ---------------------------------------------------------------------------
# Interactive
# ---------------------------------------------------------------------------

def interactive():
    print("Booth Multiplier – Interactive (Ctrl+C to quit)")
    print("Enter two integers to multiply.\n")
    while True:
        try:
            line = input("M Q [bits]: ").strip()
            parts = line.split()
            if len(parts) < 2:
                print("  Need at least M and Q"); continue
            M, Q = int(parts[0]), int(parts[1])
            n = int(parts[2]) if len(parts) >= 3 else min_bits(M, Q)
            n = max(n, min_bits(M, Q))
            result = booth_multiply(M, Q, n)
            print(f"  {M} × {Q} = {result}  (using {n}-bit Booth)")
        except (ValueError, KeyboardInterrupt):
            print(); break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if "--interactive" in sys.argv:
        interactive()
        return

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) >= 2:
        M = int(args[0])
        Q = int(args[1])
        n = int(args[2]) if len(args) >= 3 else min_bits(M, Q)
        n = max(n, min_bits(M, Q))
        result = booth_multiply(M, Q, n)
        print(f"{M} × {Q} = {result}  (using {n}-bit Booth)")
    else:
        run_tests()


if __name__ == "__main__":
    main()
