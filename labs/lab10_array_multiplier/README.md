# Lab 10 – Study and Design of Array Multiplier

## Objective
Design an N×N Array Multiplier using an AND gate array for partial product generation and a Full Adder triangle for accumulation.

## Theory

### Binary Multiplication (Long Multiplication)
Multiplying A × B is analogous to decimal long multiplication:
- Form partial products: PP[i] = A × B[i]  (each is A shifted left by i)
- Sum all partial products

### Hardware Structure

**Step 1 – AND Gate Array (Partial Product Generation)**
```
PP[i][j] = A[j] AND B[i]
```
For N-bit operands, N² AND gates produce N partial product rows.

**Step 2 – Full Adder Triangle (Accumulation)**
The partial products are added column-by-column using a triangle of Full Adders:

For a 4×4 multiplier:
```
          p00  p01  p02  p03
     p10  p11  p12  p13
p20  p21  p22  p23
p30  p31  p32  p33
```
`PP[i][j]` contributes to bit position `i+j` of the result.

Each column feeds a chain of Full Adders that accumulate the bits and propagate carries to adjacent columns.

### Complexity
| Property | Value |
|----------|-------|
| AND gates | N² |
| Full Adders | N(N−2) + (N−1) ≈ N² |
| Result width | 2N bits |
| Delay | O(N) — FA rows stack vertically |

For N=4: 16 AND gates, 8 Full Adders, 8-bit result.

### Example: 4-bit × 4-bit (6 × 5)
```
A = 0110 (6)
B = 0101 (5)

Partial products (PP[i] = A × B[i]):
PP[0] = 0110 × 1 = 00000110   (shifted 0)
PP[1] = 0110 × 0 = 00000000   (shifted 1)
PP[2] = 0110 × 1 = 00011000   (shifted 2)
PP[3] = 0110 × 0 = 00000000   (shifted 3)
                 ──────────
Sum              = 00011110   (30)  ✓ 6×5=30
```

### 2-Bit Multiplier (Minimum Case)
A 2×2 multiplier illustrates the core hardware pattern before scaling to N×N:

| A1 | A0 | B1 | B0 | P3 | P2 | P1 | P0 |
|----|----|----|----|----|----|----|-----|
| 0  | 0  | 0  | 0  |  0 |  0 |  0 |  0  |
| 0  | 1  | 1  | 0  |  0 |  0 |  1 |  0  |
| 1  | 1  | 1  | 1  |  1 |  0 |  0 |  1  |

**Hardware requirements for N×M multiplier:**
- **N×M AND gates** to generate all partial products
- Result width: **N+M bits**
- Number of adders required: **N+M−2**
- Speed-limiting factor: accumulating all partial products (O(N) FA rows)

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim:
1. Place a 4×4 AND gate array: PP[i][j] = A[j] AND B[i] for all i,j.
2. Arrange partial product bits by column (column k sums all bits where i+j=k).
3. Chain Full Adders column-by-column to accumulate; wire carries to adjacent columns.
4. Verify the 8-bit product output against expected values.

## Running with the Python Simulator

```bash
cd labs/
python3 lab10_array_multiplier/array_multiplier.py            # demo
python3 lab10_array_multiplier/array_multiplier.py 6 5 4      # 4-bit: 6×5
python3 lab10_array_multiplier/array_multiplier.py 13 11 4    # 4-bit: 13×11
```

The simulator shows the AND gate array, all partial products, and the final accumulated result.

**Result:** 2-bit binary multiplier constructed and studied; extended to N-bit array multiplier.

## Lab Tasks
1. Trace a 4×4 multiply for `A=1101 (13)` and `B=1011 (11)` by hand; verify product = 143.
2. Count how many AND gates and Full Adders a 4×4 array multiplier uses.
3. Compare the delay of an array multiplier vs. a sequential shift-and-add multiplier.
4. Extend `array_multiplier.py` to handle signed numbers using 2's complement.

## Questions
1. Why does multiplying two N-bit numbers produce at most a 2N-bit result?
   - The maximum product of two N-bit values is (2^N−1)² ≈ 2^(2N), requiring up to 2N bits to represent. For example, 4-bit max is 15×15=225, which needs 8 bits (11100001b). N bits would only hold up to 15 — clearly insufficient.
2. What is the critical path in an array multiplier?
   - The bottom row of Full Adders. The last FA row must wait for all carries produced by the rows above it; these stack vertically giving O(N) delay through N−2 FA rows plus the final ripple-carry adder across N bits.
3. How does a Wallace Tree multiplier improve on the basic array multiplier?
   - Instead of adding partial product rows sequentially top-to-bottom (O(N) depth), a Wallace Tree uses Carry Save Adders to reduce all N partial products in O(log N) CSA stages in parallel, followed by a single final carry-propagate adder. This cuts delay dramatically for wide multipliers.
4. For `A=1111` and `B=1111`, what is the maximum product, and does it fit in 8 bits?
   - 15 × 15 = **225**. 225 < 256 = 2^8, so **yes**, it fits in 8 bits (11100001b). A 2×4 = 8-bit result register is sufficient for all 4-bit × 4-bit products.
