; Lab 5 – 16-bit Subtraction using TASM / 8086
; Subtracts N2 from N1; result stored in AX.

data segment
    N1 dw 4004h
    N2 dw 1001h
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV ax, N1      ; load minuend into AX
    MOV bx, N2      ; load subtrahend into BX
    SUB ax, bx      ; AX = AX - BX
    int 3           ; breakpoint – inspect AX for result
code ends
end start
