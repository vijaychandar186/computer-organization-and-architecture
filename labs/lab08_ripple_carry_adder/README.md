# Lab 8 – Study and Design of Ripple Carry Adder

## Objective
Design an N-bit Ripple Carry Adder (RCA) by chaining N Full Adders in series, and analyse its propagation delay.

## Theory

### Structure
An N-bit RCA connects N Full Adders (FA) in sequence. The carry-out of stage `i` becomes the carry-in of stage `i+1`.

```
       A[0] B[0]    A[1] B[1]    A[2] B[2]    A[3] B[3]
         │    │       │    │       │    │       │    │
Cin=0 ──[FA0]──C1──[FA1]──C2──[FA2]──C3──[FA3]──── Cout
         │             │             │             │
        S[0]          S[1]          S[2]          S[3]
```

### Propagation Delay
Each FA introduces a delay of `t_FA`. Because carry must ripple from bit 0 to bit N−1, the **worst-case delay** of an N-bit RCA is:

```
T_RCA = N × t_FA
```

This linear scaling is the primary limitation of the RCA design. A 64-bit adder would require 64 FA delays just for the carry chain.

### Sum and Carry Equations (per stage)
```
S[i]    = A[i] ⊕ B[i] ⊕ C[i]
C[i+1]  = (A[i] · B[i]) + (B[i] · C[i]) + (A[i] · C[i])
```

### Example: 4-bit Addition
```
  A = 1101  (13)
  B = 1011  (11)
  Cin = 0

  Bit 0: 1+1+0 → S=0 C1=1
  Bit 1: 0+1+1 → S=0 C2=1
  Bit 2: 1+0+1 → S=0 C3=1
  Bit 3: 1+1+1 → S=1 C4=1  ← overflow!
  Result: 1000 with Cout=1  → 11000b = 24
```

## How the RCA Works (Procedure)
Each Full Adder stage activates only after receiving carry-in from the previous stage:
1. FA[0] receives Cin=0; computes S[0] and C[1].
2. C[1] becomes available → FA[1] activates; computes S[1] and C[2].
3. The carry continues rippling through each stage in sequence.
4. The final carry-out (Cout) indicates unsigned overflow.

The speed bottleneck is this sequential carry ripple — each stage must wait for the previous carry before it can produce its correct output.

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim:
1. Build a Full Adder subcircuit first (see Lab 7).
2. Place 4 instances of the Full Adder in series; wire Cout of FA[i] to Cin of FA[i+1].
3. Connect input buses A[3:0] and B[3:0]; add output pins for S[3:0] and final Cout.
4. Toggle inputs and observe how carry propagates stage by stage.

## Running with the Python Simulator

```bash
cd labs/
python3 lab08_ripple_carry_adder/ripple_carry_adder.py         # demo
python3 lab08_ripple_carry_adder/ripple_carry_adder.py 13 11 4  # custom
```

The output shows per-stage A, B, Cin, Sum, Cout and the carry chain.

**Result:** Ripple Carry Adder constructed in simulator and its characteristics studied.

## Lab Tasks
1. Add 4-bit numbers `0111` (7) and `0001` (1); trace each FA stage manually.
2. Add `1111` + `0001` and explain the overflow condition.
3. Count how many gate delays a 4-bit RCA needs for the worst-case carry path.
4. Compare the gate count and delay of a 4-bit RCA vs. a 4-bit CLA (Lab 9).

## Questions
1. What is the worst-case input for an N-bit RCA in terms of carry propagation?
   - Any input pair where carry must ripple through all N stages, e.g., **A = 0111...1, B = 0000...1** (or equivalently A=B=0111...1). A carry generated at bit 0 then propagates through every intermediate stage to produce the final carry-out.
2. How many Full Adders are needed for a 16-bit RCA?
   - **16 Full Adders** — one per bit position.
3. What is the total gate delay if each Full Adder takes 3 gate delays?
   - 16 × 3 = **48 gate delays** for the worst-case carry path through all 16 stages.
4. How can the RCA be modified to detect overflow in signed arithmetic?
   - XOR the carry into the MSB (C[N−1]) with the carry out of the MSB (Cout = C[N]). If `C[N] ⊕ C[N−1] = 1`, signed overflow occurred (the result sign is wrong). A single XOR gate on the two top carries implements this.
