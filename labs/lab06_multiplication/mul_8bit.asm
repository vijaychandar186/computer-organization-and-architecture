; Lab 6 – 8-bit Multiplication using TASM / 8086
; Multiplies N1 by N2 using the MUL instruction.
; 8-bit MUL: AX = AL * operand8
; Result is in AX (AH holds overflow, AL holds lower byte).

data segment
    N1 db 04h
    N2 db 03h
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV al, N1      ; AL = first operand (implicit multiplicand for MUL)
    MOV bl, N2      ; BL = second operand
    MOV ah, 00h     ; clear AH before multiplication
    MUL bl          ; AX = AL * BL
    int 3           ; breakpoint – AX holds product (e.g. 04h * 03h = 0Ch)
code ends
end start
