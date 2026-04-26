# Lab 6 – Multiplication of 8-bit Numbers; Factorial Program

## Objective
Use the 8086 `MUL` instruction to multiply numbers and implement an iterative factorial program using a loop.

## Theory

### MUL Instruction
The 8086 `MUL` instruction always uses the accumulator as one operand:

| Operand size | Syntax | Operation |
|-------------|--------|-----------|
| 8-bit  | `MUL reg8`  | `AX = AL × reg8` |
| 16-bit | `MUL reg16` | `DX:AX = AX × reg16` |

The result is automatically double-width to prevent overflow:
- 8-bit × 8-bit → 16-bit result in AX
- 16-bit × 16-bit → 32-bit result split across DX (high) and AX (low)

### Example: 8-bit Multiplication
```
N1 = 04h, N2 = 03h
MOV AL, N1   → AL = 04h
MOV BL, N2   → BL = 03h
MUL BL       → AX = 04h × 03h = 0Ch  (12 decimal)
```

### Factorial Algorithm
```
N! = N × (N-1) × (N-2) × … × 1
```
Iterative approach:
```
result = 1
for i = N downto 1:
    result = result × i
```

In 8086 assembly (using 16-bit MUL to handle results up to 8! = 40320):
```
AX = 1          ; running product
CX = N          ; countdown counter
loop:
  BX = CX       ; current multiplier
  MUL BX        ; AX = AX × BX  (DX:AX = AX × BX but N≤8 keeps DX=0)
  DEC CX
  JNZ loop
```

### Valid Range
| N | N! | Fits in AX (≤ 65535)? |
|---|----|-----------------------|
| 5 | 120 | Yes |
| 7 | 5040 | Yes |
| 8 | 40320 | Yes |
| 9 | 362880 | No (> 0xFFFF) |

## Programs

**Software used:** EMU8086 (x86 emulator, runs via Wine)

### mul_8bit.asm — Full TASM Listing
```asm
data segment
    A  db 09h
    B  db 02h
    Res1 dw ?
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov ax, 0000h
    mov al, A        ; AL = 09h (implicit operand for MUL)
    mul B            ; AX = AL × B = 09h × 02h = 12h (18)
    mov Res1, ax     ; store 16-bit result
    int 3
code ends
end start
```

**Algorithm (8-bit multiplication):**
1. Load first operand into AL (MUL always uses AL as one source)
2. Load second operand into BL (or a memory variable)
3. MUL BL → AX = AL × BL (result is always 16-bit)
4. Store AX to result memory location (Res1)
5. Halt (INT 3)

### factorial.asm — Full TASM Listing
```asm
data segment
    A db 5
data ends

code segment
assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    mov ah, 00h
    mov al, A        ; AL = N (e.g. 5)
L1: dec A            ; decrement memory variable
    mul A            ; AX = AX × A
    mov cl, A
    cmp cl, 01h      ; loop while A > 1
    jnz L1
    mov ah, 4ch
    int 21h          ; terminate program
code ends
end start
```

**Algorithm (factorial):**
1. Store N in CX register (LOOP counter condition)
2. Initialise AX = 0001h (running product), DX = 0000h
3. Each iteration: multiply AX by current counter value using MUL; decrement counter
4. Continue via JNZ until counter reaches 1
5. Copy AX (low word of result) to memory location 0600h
6. Copy DX (high word, overflow) to memory location 0601h
7. Halt (INT 21h / INT 3)

## Running with EMU8086

```bash
bash scripts/start-emu8086.sh
# open http://localhost:6080/vnc.html
```

In EMU8086: compile the program, run or single-step, inspect AX (and DX for large factorials) after the program terminates.

## Running with the Python Simulator

```bash
cd labs/
python3 asm_simulator.py lab06_multiplication/mul_8bit.asm
python3 asm_simulator.py lab06_multiplication/factorial.asm
```

Expected output for `mul_8bit.asm` (09h × 02h):
```
AX=0012h  (18)
```

Expected output for `factorial.asm` (5! = 120):
```
AX=0078h  (120)
```

**Result:** Multiplication of two 8-bit numbers and factorial of an 8-bit number completed successfully.

## Lab Tasks
1. Modify `mul_8bit.asm` to multiply `0Fh × 0Fh`; verify AX = 00E1h.
2. Change N in `factorial.asm` to 7 and confirm AX = 13B0h (5040).
3. Trace the factorial loop step by step, recording AX and CX at each iteration.

## Questions
1. Why does 8-bit MUL give a 16-bit result in AX rather than an 8-bit result in AL?
   - The maximum product of two 8-bit values is 255 × 255 = 65025, which exceeds 8 bits (max 255). Storing in AX (16-bit) ensures the result is never truncated for any valid input pair. Keeping AL only would silently discard the upper byte.
2. What happens to DX after a 16-bit `MUL BX` when the product exceeds 65535?
   - DX receives the high 16 bits of the 32-bit result. For example, 0x0100 × 0x0100 = 0x00010000; DX = 0x0001, AX = 0x0000. DX is the overflow register for 16-bit multiplication.
3. Implement the same factorial loop using the 8086 `LOOP` instruction instead of `DEC CX / JNZ`.
   ```asm
   mov cx, 5      ; N = 5
   mov ax, 1      ; running product
   loop_start:
       mul cx     ; AX = AX × CX  (16-bit MUL since CX is 16-bit)
       loop loop_start  ; LOOP = DEC CX ; JNZ loop_start
   ; AX = 120 (5!) after 5 iterations
   ```
