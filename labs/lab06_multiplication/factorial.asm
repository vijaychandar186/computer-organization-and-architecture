; Lab 6 – Factorial of N using TASM / 8086
; Computes N! for small N (N <= 8 to stay within 16-bit range).
; Strategy: AX accumulates the product; CX counts down from N to 1.
; 16-bit MUL: DX:AX = AX * BX  (we keep N small so DX stays 0)

data segment
    N  dw 5         ; change this value to compute a different factorial
data ends

code segment
    assume cs:code, ds:data
    start:
    MOV ax, data
    MOV ds, ax
    MOV cx, N       ; CX = N  (loop counter)
    MOV ax, 1       ; AX = 1  (running product)
    CMP cx, 0
    JE  done        ; 0! = 1, already set

fact_loop:
    MOV bx, cx      ; BX = current multiplier
    MUL bx          ; DX:AX = AX * BX
    DEC cx          ; CX--
    JNZ fact_loop   ; repeat until CX == 0

done:
    int 3           ; AX contains N! (e.g. 5! = 78h = 120)
code ends
end start
