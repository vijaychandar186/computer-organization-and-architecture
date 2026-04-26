; Lab 4 – 8-bit Subtraction using TASM / 8086
; Subtracts N2 from N1; result stored in AL.

data segment
    N1 db 09h
    N2 db 03h
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV al, N1      ; load minuend into AL
    MOV bl, N2      ; load subtrahend into BL
    SUB al, bl      ; AL = AL - BL
    int 3           ; breakpoint – inspect AL for result
code ends
end start
