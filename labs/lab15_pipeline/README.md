# Lab 15 – Understanding Pipeline Concepts; Design of Basic Pipeline

## Objective
Understand the 5-stage instruction pipeline, identify hazard types, and simulate pipeline execution including stall insertion and branch flushing.

## Theory

### Why Pipelining?
Without a pipeline, one instruction occupies the entire CPU for 5 cycles. A pipeline allows multiple instructions to overlap:
```
Without pipeline:       I1 I1 I1 I1 I1  I2 I2 I2 I2 I2  ...  CPI=5
With pipeline:          I1 I2 I3 I4 I5  I6 I7 ...            CPI→1
```

### 5 Stages
| Stage | Name | Action |
|-------|------|--------|
| IF | Instruction Fetch | PC → MAR; MEM[MAR] → IR; PC+1 |
| ID | Instruction Decode | Decode opcode; read source registers from register file |
| EX | Execute | ALU computes result; branch target computed |
| MEM | Memory Access | Load/store accesses data memory |
| WB | Write Back | ALU result or loaded value written to register file |

### Hazards

#### 1. Structural Hazard
Two instructions need the same hardware resource simultaneously.  
*Solution*: Stall one instruction or duplicate hardware.

#### 2. Data Hazard (RAW – Read After Write)
An instruction reads a register before a prior instruction has written it.
```
ADD R1, R2, R3    ; writes R1 in WB (cycle 5)
SUB R4, R1, R5   ; reads R1 in ID (cycle 3) — stale value!
```
*Solution*: **Forwarding** (bypass result from EX/MEM directly to next EX) or **stall** (insert NOPs).

#### Load-Use Hazard
A LOAD result cannot be forwarded without at least 1 stall (result not ready until end of MEM).

#### 3. Control Hazard (Branch)
The branch outcome is unknown until EX. Instructions fetched after the branch may be wrong.  
*Solution*: **Flush** (discard IF and ID instructions) or **branch prediction**.

### CPI (Cycles Per Instruction)
```
CPI_actual = CPI_ideal + stall_cycles_per_instruction
           = 1         + (stalls + flushes) / n_instructions
```

### Pipeline Diagram (Example – No Hazards)
```
Cycle:   1    2    3    4    5    6    7    8    9
I1:     IF   ID   EX  MEM   WB
I2:          IF   ID   EX  MEM   WB
I3:               IF   ID   EX  MEM   WB
I4:                    IF   ID   EX  MEM   WB
I5:                         IF   ID   EX  MEM   WB
```

## Running the Simulator

```bash
cd labs/
python3 lab15_pipeline/pipeline.py               # three demo scenarios
python3 lab15_pipeline/pipeline.py --no-stall    # ideal pipeline (ignore hazards)
```

**Example 1:** Five independent instructions – ideal CPI = 1.00  
**Example 2:** RAW + load-use hazards – stalls inserted, CPI > 1  
**Example 3:** Branch instruction – 2 instructions flushed

## Lab Tasks
1. Run Example 2 and count how many stall cycles are inserted; verify the CPI calculation.
2. Add forwarding logic to `pipeline.py` (detect EX→EX and MEM→EX paths, eliminating stalls where possible).
3. Draw the pipeline diagram for Example 3 by hand and identify the two flushed instructions.
4. Modify the program to use a 3-stage pipeline (IF, EX, WB) and compare CPI.

## Questions
1. What is the maximum speedup achievable with an N-stage pipeline?
   - The theoretical maximum speedup is **N×** (N-fold, equal to the number of pipeline stages). In practice, this is limited by the slowest stage (all stages must match its clock period), data/control hazards that insert stalls, and pipeline fill/drain overhead. Real speedup is typically 2–4× for a 5-stage pipeline.
2. Why does a load-use hazard require at least 1 stall even with full forwarding?
   - A LOAD instruction does not have its data available until the end of the **MEM** stage (cycle 4). The next instruction needs the value at the start of its **EX** stage (cycle 3 if back-to-back). Even with forwarding, data would need to travel backwards in time — impossible. One stall bubble pushes the dependent instruction's EX to cycle 4, when the loaded value is ready to forward from MEM→EX.
3. What is speculative execution, and how does it relate to control hazards?
   - Speculative execution is the technique of continuing to fetch and execute instructions after a branch **before knowing the branch outcome**. The CPU predicts the branch direction (taken/not-taken) and speculatively executes the predicted path. If the prediction is correct, no penalty; if wrong, the speculated instructions are **flushed** and the correct path is fetched. This eliminates branch stalls at the cost of potential wasted work and the risk of side-channel effects.
4. Name one real-world CPU where a pipeline-related hazard caused a security vulnerability.
   - **Intel (and ARM/AMD) CPUs — Spectre (CVE-2017-5753)**. Spectre exploits speculative execution: the CPU speculatively accesses memory it should not be allowed to read during branch prediction. Even though the results are discarded on a mis-prediction, the speculative load leaves a trace in the **cache** (a timing side-channel). An attacker can measure cache access times to infer the value of memory that was never architecturally visible.
