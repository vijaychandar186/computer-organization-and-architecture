; Lab 5 – 16-bit Addition using TASM / 8086
; Adds two 16-bit numbers N1 and N2; result stored in AX.

data segment
    N1 dw 4004h
    N2 dw 1001h
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV ax, N1      ; load first 16-bit operand into AX
    MOV bx, N2      ; load second 16-bit operand into BX
    ADD ax, bx      ; AX = AX + BX
    int 3           ; breakpoint – inspect AX for result
code ends
end start
