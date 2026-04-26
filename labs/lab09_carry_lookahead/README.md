# Lab 9 – Study and Design of Carry Look-Ahead Adder

## Objective
Design a Carry Look-Ahead Adder (CLA) that computes all carries simultaneously, eliminating the linear delay of the Ripple Carry Adder.

## Theory

### Motivation
In an RCA, carry must ripple through every stage. A CLA pre-computes all carries in parallel using only the original inputs A and B.

### Generate and Propagate Signals
For each bit position `i`:
```
G[i] = A[i] AND B[i]    (Generate: this stage always produces a carry)
P[i] = A[i] XOR B[i]    (Propagate: this stage passes on an incoming carry)
```

### Look-Ahead Carry Equations
```
C[0] = Cin
C[1] = G[0] + P[0]·C[0]
C[2] = G[1] + P[1]·G[0] + P[1]·P[0]·C[0]
C[3] = G[2] + P[2]·G[1] + P[2]·P[1]·G[0] + P[2]·P[1]·P[0]·C[0]
...
```

All C[i] are computed directly from G, P, and Cin — **no carry chain**.

### Sum Bits
```
S[i] = P[i] XOR C[i]     (same as A[i] XOR B[i] XOR C[i])
```

### Propagation Delay
All carries are available after just **2 gate delays** (regardless of N):
1. One AND/OR level to compute G and P
2. One level to compute all C[i] simultaneously

Total: `T_CLA = 4 gate delays` (fixed, vs. N × t_FA for RCA)

### Comparison: RCA vs CLA
| Property | RCA | CLA |
|----------|-----|-----|
| Carry delay | O(N) | O(1) |
| Gate count | Low | Higher (fan-in grows) |
| Practical limit | 4–8 bits | 4–16 bits before fan-in issues |

### Practical Note
For large word sizes, CLAs are grouped: a 16-bit adder uses four 4-bit CLA blocks, then a second-level CLA to combine their group generates/propagates.

## How the CLA Works (Procedure)
Rather than waiting for carries to ripple, the CLA performs two parallel steps:
1. **Compute G and P** for every bit position simultaneously (one gate level).
2. **Evaluate all carry equations** in parallel using G, P, and Cin (second gate level).
3. **Compute all sum bits** from P[i] XOR C[i] (third gate level).

Every bit position then produces its correct carry and sum at the same time, regardless of word width. This eliminates the carry chain entirely.

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim:
1. Build G[i] = A[i] AND B[i] and P[i] = A[i] XOR B[i] for each bit.
2. Wire the look-ahead carry equations using AND/OR gates (no chain between stages).
3. Compute S[i] = P[i] XOR C[i].
4. Compare gate levels with Lab 8's RCA for the same 4-bit inputs.

## Running with the Python Simulator

```bash
cd labs/
python3 lab09_carry_lookahead/carry_lookahead_adder.py          # demo
python3 lab09_carry_lookahead/carry_lookahead_adder.py 13 11 4  # custom
```

The output shows G, P, computed C[i], and the look-ahead carry equations.

**Result:** Carry Look-Ahead Adder constructed and its characteristics studied.

## Lab Tasks
1. Compute the CLA carry equations for `A=1010, B=0110` by hand; verify using the simulator.
2. Compare the number of gate levels needed vs. Lab 8's RCA for 4 bits.
3. Identify which input patterns achieve maximum (worst-case) fan-in in the carry equations.
4. Explain why a 16-bit CLA in a single block becomes impractical.

## Questions
1. What does `G[i]=1` mean in physical terms for that bit position?
   - Both A[i] and B[i] are 1. This bit stage **generates** a carry regardless of carry-in — even if Cin=0, Cout of this stage will be 1. No incoming carry is needed to produce a carry-out.
2. How many AND/OR gates does a 4-bit CLA need to compute C[4]?
   - C[4] = G[3] + P[3]·G[2] + P[3]·P[2]·G[1] + P[3]·P[2]·P[1]·G[0] + P[3]·P[2]·P[1]·P[0]·Cin. That requires **4 AND gates** (for the product terms of increasing width) and **1 wide 5-input OR gate**. Total: 5 gates for C[4] alone; fan-in on the OR gate is 5.
3. What is a "Group Generate" signal in a hierarchical CLA?
   - A single bit, GG, indicating that a **block** of bit positions (e.g., bits 0–3) will produce a carry-out regardless of the block's carry-in. Used as an input to a second-level CLA that combines block-level G/P signals, allowing 16-bit or 64-bit adders without fan-in explosion.
4. Is a CLA or an RCA better for a battery-powered device? Justify.
   - **RCA** is better for low-power devices. CLA requires significantly more gates (wide AND/OR trees for every carry term), increasing transistor count, die area, and dynamic power consumption per operation. RCA is simpler — fewer gates means less capacitance to switch and lower energy per addition.
