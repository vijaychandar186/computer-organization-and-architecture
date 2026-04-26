# Lab 13 – Study of Carry Save Multiplication and Program Implementation

## Objective
Understand the Carry Save Adder (CSA) and apply it to accelerate the partial-product accumulation in a multiplier.

## Theory

### Carry Save Adder (CSA)
A CSA accepts **three** N-bit inputs (A, B, C) and produces two N-bit outputs in O(1) time:
```
Sum[i]   = A[i] ⊕ B[i] ⊕ C[i]       (from Full Adder sum bit)
Carry[i] = majority(A[i], B[i], C[i]) (from Full Adder carry bit)
```
The relationship:
```
A + B + C  =  Sum  +  (Carry << 1)
```
The carry vector is **not propagated**; it is deferred. A single ripple-carry (or CLA) adder at the end performs the final 2-operand addition.

### Why CSA is Faster
| Adder | Adding K operands | Delay |
|-------|------------------|-------|
| Sequential RCA | K−1 additions | O(K·N) |
| CSA tree (Wallace) | ceil(log₃/₂ K) stages | O(log K) |

For K=8 operands: RCA needs 7 additions (7N delay); a Wallace CSA tree needs 4 stages (4·const delay), plus 1 final add.

### CSA in Array Multipliers
An N×N multiplier generates N partial products. Rather than adding them sequentially, a CSA tree reduces them to 2 operands efficiently:

```
Stage 1: reduce 8 partial products → 6  (using 2 CSAs)
Stage 2: reduce 6 → 4
Stage 3: reduce 4 → 3
Stage 4: reduce 3 → 2  (one CSA)
Final  : 2 operands → RCA/CLA adds them → product
```

### Gate-Level View
```
 A[i] ──┬──[XOR]──────────────── Sum[i]
 B[i] ──┤             ┌─ [OR] ─── Carry[i]
 C[i] ──┤──[XOR]──┐   │
                  └──[AND]──┘
 A[i]─B[i] ──────────[AND]──┘
```
(Exactly a Full Adder, but outputs are not combined into a single carry chain.)

## Binary Parallel Adder and Subtractor

A binary parallel adder/subtractor builds on the Full Adder chain and extends it with a mode-select input.

### Parallel Adder
Full adders FA1…FAn chain carry bits, each adding one column of the operands:
```
FA1: (S1, C2) = FA(A1, B1, C1)   ← C1 = initial carry-in (0 for addition)
FA2: (S2, C3) = FA(A2, B2, C2)
...
FAn: (Sn, Cout) = FA(An, Bn, Cn)
```
All full adders operate simultaneously; carries propagate left to right. The result S[n:1] is available after carry propagation settles.

### Parallel Subtractor (via 2's Complement)
Subtraction A − B = A + (−B). The 2's complement of B is computed as:
1. **1's complement**: invert all bits of B using NOT gates.
2. **+1**: set the initial carry-in C1 = 1 (instead of 0).

The same FA chain then computes A + (~B) + 1 = A − B. A single mode bit M controls the XOR gates on B inputs and the carry-in:
- M=0 → B passes unchanged, C1=0 → **addition**
- M=1 → B is inverted, C1=1 → **subtraction**

### Truth Table (1-bit adder/subtractor cell, M=mode)
| M | A | B | Cin | S | Cout |
|---|---|---|-----|---|------|
| 0 | 0 | 0 |  0  | 0 |  0   |
| 0 | 1 | 1 |  0  | 0 |  1   |
| 1 | 1 | 1 |  0  | 0 |  1   |
| 1 | 0 | 1 |  0  | 1 |  0   |

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim:
1. Build the 4-bit parallel adder/subtractor: chain 4 Full Adders; add XOR gates on each B input controlled by mode bit M; wire M to C1 (carry-in of FA1).
2. Test addition (M=0): A=0101, B=0011 → result=1000.
3. Test subtraction (M=1): A=0101, B=0011 → result=0010 (5−3=2).
4. Then build the CSA circuit for the carry-save multiplier.

## Running with the Python Simulator

```bash
cd labs/
python3 lab13_carry_save/carry_save.py                      # demo
python3 lab13_carry_save/carry_save.py 13 11 7              # CSA: 13+11+7
python3 lab13_carry_save/carry_save.py --multiply 6 5       # CSA multiplication
python3 lab13_carry_save/carry_save.py --multiply 13 11 4   # 4-bit CSA multiply
```

**Result:** Binary parallel adder/subtractor and carry-save multiplier constructed and their characteristics studied.

## Lab Tasks
1. Add 5-bit numbers 13, 11, and 7 using a CSA; verify the sum manually.
2. Multiply 6 × 5 using `--multiply` and trace through the partial product reduction.
3. Count the number of Full Adders used in a 4×4 CSA multiplier vs. a 4×4 array multiplier.
4. Explain why CSA cannot replace the final ripple-carry adder.

## Questions
1. What is the difference between a carry-save adder and a carry-propagate adder?
   - A **carry-save adder** accepts 3 inputs and produces 2 outputs (a sum vector and a carry vector) without propagating the carry — the carry is deferred to the next stage. A **carry-propagate adder** (RCA/CLA) takes 2 inputs and resolves all carries to produce a single fully-computed output.
2. How many CSA stages does a Wallace tree need to reduce 8 operands to 2?
   - **4 stages**: 8→6 (2 CSAs reduce 3 to 2 each) → 4 → 3 → 2. Each CSA reduces 3 inputs to 2 sum+carry outputs, so the number decreases by factor 2/3 each stage: ceil(log_{3/2}(8)) = 4.
3. Why is CSA particularly important in multipliers rather than simple 2-operand adders?
   - Multipliers produce N partial products that all need summing. CSA reduces K>2 operands in O(log K) stages rather than K−1 sequential additions (O(K·N)). For a 2-operand adder there is no stack of partial products, so CSA offers no advantage.
4. If the CSA produces Sum = `01011` and Carry = `00110`, what is the total sum?
   - Total = Sum + (Carry << 1) = 01011 + 01100 = **10111** = **23** decimal. ✓ (Verify: 01011=11, 00110=6 shifted left=12; 11+12=23.)
