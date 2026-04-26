#!/usr/bin/env python3
"""Lab 7 – Half Adder and Full Adder simulation.

Implements gate-level logic and prints truth tables.

Run:
  python3 adders.py
  python3 adders.py --interactive
"""

import sys


# ---------------------------------------------------------------------------
# Gate primitives
# ---------------------------------------------------------------------------

def AND(a: int, b: int) -> int: return a & b
def OR(a: int, b: int)  -> int: return a | b
def XOR(a: int, b: int) -> int: return a ^ b
def NOT(a: int)         -> int: return 1 - a


# ---------------------------------------------------------------------------
# Half Adder
# ---------------------------------------------------------------------------

def half_adder(a: int, b: int) -> tuple[int, int]:
    """Returns (sum, carry_out).

    Gate structure:
      Sum   = A XOR B
      Carry = A AND B
    """
    s    = XOR(a, b)
    cout = AND(a, b)
    return s, cout


# ---------------------------------------------------------------------------
# Full Adder
# ---------------------------------------------------------------------------

def full_adder(a: int, b: int, cin: int) -> tuple[int, int]:
    """Returns (sum, carry_out).

    Built from two Half Adders and one OR gate:
      HA1: (s1, c1) = half_adder(A, B)
      HA2: (sum, c2) = half_adder(s1, Cin)
      Cout = c1 OR c2
    """
    s1, c1 = half_adder(a, b)
    s,  c2 = half_adder(s1, cin)
    cout   = OR(c1, c2)
    return s, cout


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_half_adder_table():
    print("Half Adder Truth Table")
    print("┌───┬───┬─────┬───────┐")
    print("│ A │ B │ Sum │ Carry │")
    print("├───┼───┼─────┼───────┤")
    for a in (0, 1):
        for b in (0, 1):
            s, c = half_adder(a, b)
            print(f"│ {a} │ {b} │  {s}  │   {c}   │")
    print("└───┴───┴─────┴───────┘")


def print_full_adder_table():
    print("\nFull Adder Truth Table")
    print("┌───┬───┬─────┬─────┬───────┐")
    print("│ A │ B │ Cin │ Sum │ Cout  │")
    print("├───┼───┼─────┼─────┼───────┤")
    for a in (0, 1):
        for b in (0, 1):
            for cin in (0, 1):
                s, c = full_adder(a, b, cin)
                print(f"│ {a} │ {b} │  {cin}  │  {s}  │   {c}   │")
    print("└───┴───┴─────┴─────┴───────┘")


def print_gate_diagram():
    print("""
Half Adder (gate diagram):
  A ──┬──[ XOR ]──── Sum
  B ──┘
  A ──┬──[ AND ]──── Carry
  B ──┘

Full Adder (gate diagram):
  A ──┬──[HA1]──S1──┬──[HA2]──── Sum
  B ──┘      └──C1──┤
  Cin─────────────[HA2]──C2─┐
                              └──[OR]──── Cout
                    C1 ───────────┘
""")


# ---------------------------------------------------------------------------
# Interactive mode
# ---------------------------------------------------------------------------

def interactive():
    print("Full Adder – Interactive")
    print("Enter A, B, Cin (0 or 1). Press Ctrl+C to quit.\n")
    while True:
        try:
            line = input("A B Cin: ").strip()
            parts = line.split()
            if len(parts) != 3:
                print("  Enter exactly three values: A B Cin"); continue
            a, b, cin = (int(x) for x in parts)
            if any(v not in (0, 1) for v in (a, b, cin)):
                print("  Values must be 0 or 1"); continue
            s, c = full_adder(a, b, cin)
            print(f"  Sum={s}  Cout={c}")
        except (ValueError, KeyboardInterrupt):
            print(); break


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print_gate_diagram()
    print_half_adder_table()
    print_full_adder_table()

    if "--interactive" in sys.argv:
        print()
        interactive()


if __name__ == "__main__":
    main()
