# Lab 14 – Understanding Processing Unit; Design of Primitive Processing Unit

## Objective
Understand the internal structure of a CPU and simulate a primitive processing unit with fetch-decode-execute cycle, registers, ALU, and memory.

## Theory

### CPU Components
```
         ┌───────────────────────────────────────┐
         │              CPU                       │
         │  ┌──────┐   ┌──────────────────────┐  │
         │  │  PC  │   │     Control Unit      │  │
         │  ├──────┤   │  (Fetch / Decode /    │  │
         │  │  IR  │   │   Execute FSM)        │  │
         │  ├──────┤   └──────────────────────┘  │
         │  │  MAR │         │                    │
         │  ├──────┤    ┌────▼────┐               │
         │  │  MDR │    │  ALU   │               │
         │  ├──────┤    │ADD SUB │               │
         │  │  ACC │    │AND OR  │               │
         │  ├──────┤    │NOT CMP │               │
         │  │ R0–R3│    └────────┘               │
         └──┴──────┴────────────────────────────┘
               │
        System Bus (Address + Data + Control)
               │
         ┌─────▼─────┐
         │   Memory  │
         │  256 words│
         └───────────┘
```

### Fetch-Decode-Execute Cycle
Each instruction takes 3–5 micro-operations:

**Fetch:**
1. MAR ← PC
2. MDR ← MEM[MAR]
3. IR  ← MDR
4. PC  ← PC + 1

**Decode:** Examine IR fields (opcode, operands)

**Execute:** Carry out the operation (ALU, memory access, branch)

### Instruction Encoding (16-bit)
```
 15..12   11..8   7..4    3..0
 opcode    dst    src/f2   imm
```

### Instruction Set
| Mnemonic | Opcode | Operation |
|----------|--------|-----------|
| LOAD Rd, addr | 0x1 | Rd ← MEM[addr] |
| STORE Rd, addr | 0x2 | MEM[addr] ← Rd |
| MOV Rd, Rs | 0x3 | Rd ← Rs |
| ADD Rd, Rs | 0x4 | Rd ← Rd + Rs |
| SUB Rd, Rs | 0x5 | Rd ← Rd − Rs |
| AND Rd, Rs | 0x6 | Rd ← Rd AND Rs |
| OR Rd, Rs | 0x7 | Rd ← Rd OR Rs |
| NOT Rd | 0x8 | Rd ← NOT Rd |
| JMP addr | 0x9 | PC ← addr |
| JZ addr | 0xA | if ZF: PC ← addr |
| JNZ addr | 0xB | if ¬ZF: PC ← addr |
| MOVI Rd, imm | 0xC | Rd ← imm |
| HLT | 0xF | halt |

## Multiplexer (MUX) — Theory

A Multiplexer selects one of N inputs and routes it to the output based on select line(s). It is a fundamental building block in CPU datapaths (register file read ports, ALU input selection, bus arbitration).

**Formula:** 2^n inputs require n select lines.

| Type | Inputs | Select Lines | Output | Application |
|------|--------|--------------|--------|-------------|
| 2×1  | A0, A1 | S0 | Y = A[S0] | Simple data routing |
| 4×1  | A0–A3  | S1, S0 | Y = A[S1S0] | ALU source select |
| 8×1  | A0–A7  | S2–S0 | Y = A[S2S1S0] | Register file mux |
| 16×1 | A0–A15 | S3–S0 | Y = A[S3S2S1S0] | Wide bus select |

**Boolean expression (4×1 MUX):**
```
Y = (A0 · S1' · S0') + (A1 · S1' · S0) + (A2 · S1 · S0') + (A3 · S1 · S0)
```

In Logisim: use the Plexers → Multiplexer component; set data bits and select bits in properties.

## ALU — Theory

The ALU performs all arithmetic and logic operations in the CPU. Every computation in a program ultimately executes here.

**Operations:**

| Category | Examples |
|----------|----------|
| Arithmetic | ADD, SUB, MUL, DIV, increment, decrement |
| Logic | AND, OR, NOT, XOR |
| Comparison | CMP (subtract and set flags, discard result) |
| Shift | SHL, SHR, SAR (arithmetic shift right) |

**Gate-level implementation:**
All data in a computer is represented as binary (0 and 1). Transistors implement binary states: an open transistor (no current) = 0; a closed transistor (current flowing) = 1. Logic gates are built by connecting multiple transistors — one transistor controls the state of another, acting as a gate that allows or blocks current. An ALU is a collection of such gate networks selected by control signals from the Control Unit.

**ALU control signals (3-bit example):**
| ALUOp | Operation |
|-------|-----------|
| 000 | AND |
| 001 | OR |
| 010 | ADD |
| 110 | SUB |
| 111 | SLT (set less than) |

## Running with Logisim Evolution

**Software used:** Logisim Evolution (logic gate simulator, Java)

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

In Logisim, build a simple 1-bit ALU cell:
1. Place AND, OR, ADD (half-adder) subcircuits.
2. Add a 3×1 MUX to select the operation output based on ALUOp bits.
3. Chain 4 1-bit ALU cells for a 4-bit ALU; wire carry-out to carry-in.
4. Test all operations by toggling A, B, and ALUOp inputs.

## Running with the Python Simulator

```bash
cd labs/
python3 lab14_processing_unit/primitive_cpu.py           # run demo programs
python3 lab14_processing_unit/primitive_cpu.py --trace   # micro-operation trace
```

**Program 1** loads two memory values (15 and 27), adds them, and stores the result.  
**Program 2** counts down from 5 to 0 using a JNZ loop.

With `--trace`, every micro-operation is printed: register transfers, ALU operations, and memory reads/writes.

**Result:** Arithmetic Logic Unit and primitive processing unit designed and studied.

## Lab Tasks
1. Run Program 1 with `--trace` and list each micro-operation in the fetch and execute phases.
2. Add a Program 3 that computes the sum of values in addresses 0x30, 0x31, 0x32.
3. Extend the instruction set with a `MUL` instruction.
4. Draw the datapath diagram showing how registers, ALU, MAR, MDR, and memory connect.

## Questions
1. Why are MAR and MDR needed as intermediate registers?
   - The memory bus is shared between the CPU and memory and operates on its own timing cycle. **MAR** (Memory Address Register) holds the target address stable on the address bus for the duration of a memory access. **MDR** (Memory Data Register) buffers data traveling between memory and internal registers, decoupling the slower memory timing from the faster register-to-register transfers inside the CPU.
2. What is the role of the ACC (accumulator) register?
   - The accumulator is the primary source of one ALU operand and the implicit destination for the result of most arithmetic/logic operations. On early CPUs (and the 8086 for MUL/DIV/IO), it is the dedicated working register — operations like ADD, SUB, and AND read from and write back to ACC without needing to explicitly name it as a destination.
3. How many clock cycles does Program 2's loop body take per iteration?
   - Each iteration executes MOVI/LOAD (~4–5 cycles), SUB (~4), and JNZ (~4), totalling approximately **12–14 micro-operation cycles** per loop iteration depending on the specific instruction timings of the primitive CPU implementation.
4. What is the difference between a RISC and CISC instruction set in terms of fetch-decode-execute?
   - **RISC** (Reduced Instruction Set Computer): fixed-length instructions, simple uniform decode, all operations complete in one pipeline stage, load/store architecture (only LOAD/STORE touch memory). Pipeline-friendly; CPI approaches 1. **CISC** (Complex Instruction Set Computer): variable-length instructions, multi-cycle decode (complex microcode), single instruction may perform memory read + ALU + write. Harder to pipeline; decoder must handle many formats. The 8086 used in Labs 4–6 is CISC.
