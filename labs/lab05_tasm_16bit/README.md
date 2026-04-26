# Lab 5 – Addition and Subtraction of 16-bit Numbers

## Objective
Extend the 8-bit programs from Lab 4 to operate on 16-bit operands using `dw` (define word) data declarations and 16-bit registers.

## Theory

### 16-bit vs 8-bit Operations
| Aspect | 8-bit | 16-bit |
|--------|-------|--------|
| Registers | AL, BL | AX, BX |
| Max value | 255 (0xFF) | 65535 (0xFFFF) |
| Data directive | `db` | `dw` |
| Carry on overflow | CF=1 at 256 | CF=1 at 65536 |

### Data Segment (16-bit)
```asm
data segment
    N1 dw 4004h   ; define word (16-bit)
    N2 dw 1001h
data ends
```

### Registers
```
AX = AH:AL   (16-bit = high byte : low byte)
BX = BH:BL
```
When you load `MOV AX, N1` for a `dw` variable, the full 16-bit value enters AX.

### Example: 16-bit Addition
```
  4004h
+ 1001h
-------
  5005h
```

### Example: 16-bit Subtraction
```
  4004h
- 1001h
-------
  3003h
```

## Programs

**Software used:** EMU8086 (x86 emulator, runs via Wine)

### add_16bit.asm — Full TASM Listing
```asm
data segment
    N1 dw 4004h
    N2 dw 1001h
    Res dw ?
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov ax, N1       ; AX = 4004h
    mov bx, N2       ; BX = 1001h
    add ax, bx       ; AX = 5005h
    mov Res, ax      ; store result
    int 3
code ends
end start
```

**Algorithm (16-bit addition):**
1. Load 0000H into CX register (carry tracker)
2. Load N1 into AX (accumulator) from data segment
3. Load N2 into BX from data segment
4. ADD AX, BX → result in AX; CF=1 if sum > 0xFFFF
5. JNC past carry step (jump if no carry)
6. INC CX (record the carry-out)
7. Store AX to result memory location
8. Store CX (carry) to secondary memory location
9. Halt (INT 3)

### sub_16bit.asm — Full TASM Listing
```asm
data segment
    N1 dw 4004h
    N2 dw 1001h
    Res dw ?
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov ax, N1       ; AX = 4004h
    mov bx, N2       ; BX = 1001h
    sub ax, bx       ; AX = 3003h
    mov Res, ax
    int 3
code ends
end start
```

**Algorithm (16-bit subtraction):**
1. Load 0000H into CX register (borrow tracker)
2. Load N1 into AX from data segment
3. Load N2 into BX from data segment
4. SUB AX, BX → result in AX; CF=1 if borrow occurred
5. JNC past borrow step
6. INC CX (record the borrow)
7. Store AX to result memory; store CX to borrow memory
8. Halt (INT 3)

## Running with EMU8086

```bash
bash scripts/start-emu8086.sh
# open http://localhost:6080/vnc.html
```

In EMU8086: compile, run (or single-step), inspect AX and the Flags register after INT 3.

## Running with the Python Simulator

```bash
cd labs/
python3 asm_simulator.py lab05_tasm_16bit/add_16bit.asm
python3 asm_simulator.py lab05_tasm_16bit/sub_16bit.asm
```

Expected output for `add_16bit.asm`:
```
AX=5005h  (20485)
```

Expected output for `sub_16bit.asm`:
```
AX=3003h  (12291)
```

**Result:** Addition and subtraction of two 16-bit numbers completed successfully.

## Lab Tasks
1. Add `FFFFh + 0001h` and observe CF and AX.
2. Compare the number of clock cycles for 8-bit vs 16-bit ADD (look up 8086 timing sheets).
3. Modify the programs to store the result back into a `dw` memory variable named `result`.

## Questions
1. If `AX = 0003h` and `BX = 0005h`, what is `AX` after `SUB AX, BX`? What does CF indicate?
   - **AX = FFFEh** (−2 in two's complement, or 65534 unsigned). **CF=1** — a borrow occurred because 3 < 5 in unsigned arithmetic; the result wrapped around the 16-bit boundary.
2. What is the difference between `db` and `dw` in the data segment?
   - `db` (define byte) allocates 1 byte (8-bit, 0–255); `dw` (define word) allocates 2 bytes (16-bit, 0–65535). Using `dw` with `MOV AX, N1` loads the full 16-bit value into AX; with `db` you would only load an 8-bit value into AL.
3. How would you add two 32-bit numbers on an 8086 (which has no 32-bit registers)?
   - Split each 32-bit number into a low word and a high word. ADD the low words (result in AX, CF captures the carry). Then use **ADC** (Add with Carry) for the high words — ADC includes CF from the first addition, correctly propagating the carry: `ADD ax, lo2 / ADC dx, hi2`.
