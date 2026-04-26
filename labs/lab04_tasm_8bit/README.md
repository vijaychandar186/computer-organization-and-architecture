# Lab 4 – Study of TASM: Addition and Subtraction of 8-bit Numbers

## Objective
Write and simulate 8086 assembly programs to add and subtract two 8-bit numbers using TASM syntax.

## Theory

### 8086 Registers Used
| Register | Size | Role |
|----------|------|------|
| AL | 8-bit | Low byte of AX; primary 8-bit accumulator |
| BL | 8-bit | Low byte of BX; general-purpose |
| AX | 16-bit | Accumulator; used for MOV AX, data (segment load) |
| DS | 16-bit | Data Segment register |

### ADD Instruction
```
ADD dst, src   ; dst = dst + src
```
Affects: ZF, SF, CF, OF

### SUB Instruction
```
SUB dst, src   ; dst = dst - src
```
Affects: ZF, SF, CF, OF. CF=1 indicates a borrow (negative result in unsigned interpretation).

### Two's Complement Subtraction
The CPU performs `A - B` as `A + (~B + 1)` internally. The carry flag (CF) is set if the result wraps around.

### Data Segment Pattern (TASM)
```asm
data segment
    N1 db 04h   ; define byte
    N2 db 01h
data ends
```
`db` = define byte (8-bit). Variables are accessed by name after `MOV ds, ax`.

## Programs

**Software used:** EMU8086 (x86 emulator, runs via Wine)

### add_8bit.asm — Full TASM Listing
```asm
data segment
    a db 15h
    b db 12h
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov al, a        ; AL = 15h (first operand)
    mov bl, b        ; BL = 12h (second operand)
    add al, bl       ; AL = 27h (sum)
    int 3            ; breakpoint / halt
code ends
end start
```

**Algorithm (8-bit addition):**
1. Initialise DS from data segment base address
2. Load first operand into AL
3. Load second operand into BL
4. ADD AL, BL → result in AL; CF set if carry out of bit 7
5. Apply DAA if packed-BCD decimal adjustment is required
6. Store result (AX) to memory; halt via INT 3

### sub_8bit.asm — Full TASM Listing
```asm
data segment
    a db 15h
    b db 12h
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov al, a        ; AL = 15h (minuend)
    mov bl, b        ; BL = 12h (subtrahend)
    sub al, bl       ; AL = 03h (difference)
    int 3
code ends
end start
```

**Algorithm (8-bit subtraction):**
1. Initialise DS from data segment base address
2. Load minuend into AL
3. Load subtrahend into BL
4. SUB AL, BL → result in AL; CF=1 if borrow (unsigned underflow)
5. Apply DAS if packed-BCD decimal adjustment is required
6. Store result (AX) to memory; halt via INT 3

## Running with EMU8086

```bash
bash scripts/start-emu8086.sh
# open http://localhost:6080/vnc.html
```

In EMU8086:
1. Paste or open the TASM listing in the editor.
2. Click **Compile** then **Run** (or **Single Step** to watch registers update).
3. Inspect AL in the registers panel after INT 3 halts execution.

## Running with the Python Simulator

```bash
cd labs/
python3 asm_simulator.py lab04_tasm_8bit/add_8bit.asm
python3 asm_simulator.py lab04_tasm_8bit/sub_8bit.asm
```

Expected output for `add_8bit.asm` (15h + 12h):
```
AL=27h  (39)
```

Expected output for `sub_8bit.asm` (15h − 12h):
```
AL=03h  (3)
```

**Result:** Addition and subtraction of two 8-bit numbers completed successfully.

## Lab Tasks
1. Change N1 and N2 to test: `FFh + 01h` (overflow case).
2. Subtract a larger number from a smaller one and observe CF.
3. Verify results by hand using binary addition/subtraction.

## Questions
1. What is the maximum value that fits in an 8-bit register?
   - **255 (0xFF)** unsigned. In signed two's complement: +127 (0x7F). Setting all 8 bits high gives 1111 1111b = 255.
2. What does CF=1 mean after a subtraction?
   - A borrow occurred — the minuend was smaller than the subtrahend in unsigned interpretation. The result wrapped around (underflowed). For `05h − 08h`, CF=1 and AL = FDh (−3 in two's complement).
3. How does `INT 3` behave in a real TASM environment vs. this simulator?
   - In EMU8086/real TASM: INT 3 triggers a software breakpoint, halting execution and passing control to the debugger so registers can be inspected. In the Python simulator: it is treated as a HALT — execution stops and the final register state is printed.
