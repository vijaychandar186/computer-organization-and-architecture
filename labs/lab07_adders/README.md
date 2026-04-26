# Lab 7 – Design of Half Adder and Full Adder

## Objective
Understand and simulate the gate-level design of a Half Adder and a Full Adder.

## Theory

### Half Adder
Adds two single bits. Produces a **Sum** and a **Carry** output.

| A | B | Sum | Carry |
|---|---|-----|-------|
| 0 | 0 |  0  |   0   |
| 0 | 1 |  1  |   0   |
| 1 | 0 |  1  |   0   |
| 1 | 1 |  0  |   1   |

**Boolean expressions:**
```
Sum   = A ⊕ B   (XOR)
Carry = A · B   (AND)
```

**Gate diagram:**
```
A ──┬──[XOR]──── Sum
B ──┘
A ──┬──[AND]──── Carry
B ──┘
```

### Full Adder
Adds two bits **plus a carry-in**. Required for multi-bit addition where carries propagate between stages.

| A | B | Cin | Sum | Cout |
|---|---|-----|-----|------|
| 0 | 0 |  0  |  0  |  0   |
| 0 | 0 |  1  |  1  |  0   |
| 0 | 1 |  0  |  1  |  0   |
| 0 | 1 |  1  |  0  |  1   |
| 1 | 0 |  0  |  1  |  0   |
| 1 | 0 |  1  |  0  |  1   |
| 1 | 1 |  0  |  0  |  1   |
| 1 | 1 |  1  |  1  |  1   |

**Boolean expressions:**
```
Sum  = A ⊕ B ⊕ Cin
Cout = (A · B) + (B · Cin) + (A · Cin)
```

**Implementation using two Half Adders:**
```
HA1: (s1, c1) = HA(A, B)
HA2: (Sum, c2) = HA(s1, Cin)
Cout = c1 OR c2
```

### Why Full Adder Uses Two Half Adders
A Half Adder cannot handle a carry input. The Full Adder chains two Half Adders so that three bits can be summed, propagating the carry correctly.

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim, build both circuits:
1. **Half Adder** — place one XOR gate (Sum output) and one AND gate (Carry output); connect inputs A and B to both gates.
2. **Full Adder** — chain two Half Adder subcircuits: HA1(A,B)→(s1,c1), HA2(s1,Cin)→(Sum,c2), then OR(c1,c2)→Cout. Gate count: 2×XOR + 2×AND + 1×OR = 5 gates.
3. Use the Poke tool to toggle A, B, Cin and verify each row of the truth table above.

## Running with the Python Simulator

```bash
cd labs/
python3 lab07_adders/adders.py
python3 lab07_adders/adders.py --interactive
```

The program prints the gate diagram and both truth tables, then optionally enters interactive mode where you type A, B, Cin and get Sum/Cout.

**Result:** Half Adder and Full Adder circuits designed, simulated, and truth tables verified.

## Lab Tasks
1. Verify the Half Adder truth table by tracing through each row by hand.
2. Derive the Full Adder truth table from its Boolean expression.
3. Count the total gate count for a Full Adder built from two Half Adders (AND, OR, XOR gates).
4. Modify `adders.py` to print `NAND`-only implementations of both adders.

## Questions
1. Why can a Half Adder not be used on its own to add multi-bit numbers?
   - A Half Adder has no carry-in input. When adding bit positions beyond bit 0, the carry from the previous stage must be included. Without a Cin port, that carry is simply discarded, giving wrong results for multi-bit operands.
2. What is the minimum number of NAND gates needed to implement a Full Adder?
   - **9 NAND gates** (the standard minimum). XOR requires 4 NANDs; two XORs + the carry majority function can be combined to reach 9 with gate sharing. (Some optimised forms achieve 9; textbook implementations use 9–14 depending on whether sharing is exploited.)
3. If `A=1, B=1, Cin=1`, what are Sum and Cout? Verify using the truth table.
   - **Sum = 1**, **Cout = 1**. From Boolean: Sum = 1⊕1⊕1 = 0⊕1 = 1; Cout = (1·1)+(1·1)+(1·1) = 1+1+1 = 1. Reading truth table row (A=1, B=1, Cin=1): Sum=1, Cout=1. ✓ (Three 1s sum to 3 = binary 11, i.e., Sum bit=1, Carry=1.)
