; Lab 4 – 8-bit Addition using TASM / 8086
; Adds two 8-bit numbers N1 and N2; result stored in AL.

data segment
    N1 db 04h
    N2 db 01h
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV al, N1      ; load first operand into AL
    MOV bl, N2      ; load second operand into BL
    ADD al, bl      ; AL = AL + BL
    int 3           ; breakpoint – inspect AL for result
code ends
end start
