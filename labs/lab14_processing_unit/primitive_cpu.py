#!/usr/bin/env python3
"""Lab 14 – Primitive Processing Unit simulator.

Models a simple single-bus CPU with:
  Registers : PC (Program Counter), IR (Instruction Register),
              MAR (Memory Address Register), MDR (Memory Data Register),
              ACC (Accumulator), R0..R3 (general purpose)
  Memory    : 256-word flat address space
  ALU       : ADD, SUB, AND, OR, NOT, CMP
  Control   : Fetch → Decode → Execute cycle with micro-operation trace

Instruction Set (each instruction is one word = 16 bits):
  Encoding: [opcode:4][dst:4][src:4][imm/addr:4]  (simplified)

  Mnemonic  Opcode  Operation
  --------  ------  ---------
  LOAD  Rn, addr   0x1   Rn = MEM[addr]
  STORE Rn, addr   0x2   MEM[addr] = Rn
  MOV   Rd, Rs     0x3   Rd = Rs
  ADD   Rd, Rs     0x4   Rd = ACC = Rd + Rs
  SUB   Rd, Rs     0x5   Rd = ACC = Rd - Rs
  AND   Rd, Rs     0x6   Rd = ACC = Rd AND Rs
  OR    Rd, Rs     0x7   Rd = ACC = Rd OR Rs
  NOT   Rd         0x8   Rd = NOT Rd
  JMP   addr       0x9   PC = addr
  JZ    addr       0xA   if ACC==0: PC = addr
  JNZ   addr       0xB   if ACC!=0: PC = addr
  MOVI  Rd, imm    0xC   Rd = imm  (4-bit immediate)
  HLT              0xF   stop

Run:
  python3 primitive_cpu.py             # run built-in demo programs
  python3 primitive_cpu.py --trace     # verbose micro-operation trace
"""

import sys


# ---------------------------------------------------------------------------
# Instruction encoding helpers
# ---------------------------------------------------------------------------

def encode(opcode: int, f1: int = 0, f2: int = 0, imm: int = 0) -> int:
    return ((opcode & 0xF) << 12) | ((f1 & 0xF) << 8) | ((f2 & 0xF) << 4) | (imm & 0xF)


OPCODES = {
    "LOAD": 0x1, "STORE": 0x2, "MOV": 0x3,
    "ADD": 0x4, "SUB": 0x5, "AND": 0x6, "OR": 0x7,
    "NOT": 0x8, "JMP": 0x9, "JZ": 0xA, "JNZ": 0xB,
    "MOVI": 0xC, "HLT": 0xF,
}
OP_NAMES = {v: k for k, v in OPCODES.items()}

REG_NAMES = {0: "R0", 1: "R1", 2: "R2", 3: "R3",
             4: "ACC", 5: "PC", 6: "IR", 7: "MAR", 8: "MDR"}


# ---------------------------------------------------------------------------
# CPU
# ---------------------------------------------------------------------------

class PrimitiveCPU:
    def __init__(self, trace: bool = False):
        self.PC  = 0
        self.IR  = 0
        self.MAR = 0
        self.MDR = 0
        self.ACC = 0
        self.R   = [0, 0, 0, 0]   # R0..R3
        self.MEM = [0] * 256
        self.ZF  = 0
        self.trace = trace
        self.halted = False
        self.cycles = 0

    # -- memory helpers ---------------------------------------------------

    def load_program(self, instructions: list[int], data: dict[int, int] | None = None,
                     start: int = 0):
        for i, instr in enumerate(instructions):
            self.MEM[start + i] = instr
        if data:
            for addr, val in data.items():
                self.MEM[addr] = val
        self.PC = start

    def mem_read(self, addr: int) -> int:
        return self.MEM[addr & 0xFF]

    def mem_write(self, addr: int, val: int):
        self.MEM[addr & 0xFF] = val & 0xFFFF

    # -- register helpers -------------------------------------------------

    def get_reg(self, idx: int) -> int:
        return self.R[idx & 3]

    def set_reg(self, idx: int, val: int):
        self.R[idx & 3] = val & 0xFFFF

    # -- micro-operation trace -------------------------------------------

    def _t(self, msg: str):
        if self.trace:
            print(f"    μ  {msg}")

    # -- ALU --------------------------------------------------------------

    def _alu(self, op: int, a: int, b: int) -> int:
        if op == OPCODES["ADD"]: return (a + b) & 0xFFFF
        if op == OPCODES["SUB"]: return (a - b) & 0xFFFF
        if op == OPCODES["AND"]: return a & b
        if op == OPCODES["OR" ]: return a | b
        if op == OPCODES["NOT"]: return (~a) & 0xFFFF
        return 0

    # -- fetch-decode-execute cycle --------------------------------------

    def step(self):
        if self.halted:
            return

        self.cycles += 1

        # --- FETCH ---
        self._t(f"MAR ← PC  ({self.PC})")
        self.MAR = self.PC
        self._t(f"MDR ← MEM[MAR]  ({self.MEM[self.MAR]:#06x})")
        self.MDR = self.mem_read(self.MAR)
        self._t(f"IR  ← MDR")
        self.IR  = self.MDR
        self._t(f"PC  ← PC + 1  ({self.PC + 1})")
        self.PC += 1

        # --- DECODE ---
        opcode = (self.IR >> 12) & 0xF
        f1     = (self.IR >>  8) & 0xF
        f2     = (self.IR >>  4) & 0xF
        imm    =  self.IR        & 0xF
        op_name = OP_NAMES.get(opcode, f"?{opcode:X}")

        self._t(f"Decode: {op_name}  f1={f1}  f2={f2}  imm={imm}")

        # --- EXECUTE ---
        if opcode == OPCODES["HLT"]:
            self._t("HLT: CPU halted")
            self.halted = True

        elif opcode == OPCODES["LOAD"]:
            addr = (f2 << 4) | imm
            self._t(f"MAR ← {addr}")
            self.MAR = addr
            self._t(f"MDR ← MEM[{addr}]  ({self.mem_read(addr)})")
            self.MDR = self.mem_read(addr)
            self._t(f"R{f1} ← MDR")
            self.set_reg(f1, self.MDR)

        elif opcode == OPCODES["STORE"]:
            addr = (f2 << 4) | imm
            self._t(f"MAR ← {addr},  MDR ← R{f1}")
            self.MAR = addr
            self.MDR = self.get_reg(f1)
            self._t(f"MEM[{addr}] ← {self.MDR}")
            self.mem_write(addr, self.MDR)

        elif opcode == OPCODES["MOV"]:
            val = self.get_reg(f2)
            self._t(f"R{f1} ← R{f2}  ({val})")
            self.set_reg(f1, val)

        elif opcode in (OPCODES["ADD"], OPCODES["SUB"],
                        OPCODES["AND"], OPCODES["OR"]):
            a, b = self.get_reg(f1), self.get_reg(f2)
            result = self._alu(opcode, a, b)
            self._t(f"ACC ← R{f1} {op_name} R{f2} = {a} {op_name} {b} = {result}")
            self.ACC = result
            self.ZF  = 1 if result == 0 else 0
            self.set_reg(f1, result)

        elif opcode == OPCODES["NOT"]:
            a      = self.get_reg(f1)
            result = (~a) & 0xFFFF
            self._t(f"R{f1} ← NOT {a} = {result}")
            self.set_reg(f1, result)
            self.ACC = result
            self.ZF  = 1 if result == 0 else 0

        elif opcode == OPCODES["JMP"]:
            addr = (f1 << 8) | (f2 << 4) | imm
            self._t(f"PC ← {addr}")
            self.PC = addr

        elif opcode == OPCODES["JZ"]:
            addr = (f1 << 8) | (f2 << 4) | imm
            self._t(f"ZF={self.ZF}: {'branch taken' if self.ZF else 'not taken'}")
            if self.ZF:
                self.PC = addr

        elif opcode == OPCODES["JNZ"]:
            addr = (f1 << 8) | (f2 << 4) | imm
            self._t(f"ZF={self.ZF}: {'branch taken' if not self.ZF else 'not taken'}")
            if not self.ZF:
                self.PC = addr

        elif opcode == OPCODES["MOVI"]:
            self._t(f"R{f1} ← {imm}")
            self.set_reg(f1, imm)

    def run(self, max_cycles: int = 1000):
        while not self.halted and self.cycles < max_cycles:
            if self.trace:
                print(f"\n[Cycle {self.cycles+1:3}] PC={self.PC:3}  "
                      f"R0={self.R[0]}  R1={self.R[1]}  "
                      f"R2={self.R[2]}  R3={self.R[3]}  "
                      f"ACC={self.ACC}  ZF={self.ZF}")
            self.step()

    def dump(self):
        print("\n  CPU State:")
        print(f"  PC={self.PC}  ACC={self.ACC}  ZF={self.ZF}  "
              f"Halted={self.halted}  Cycles={self.cycles}")
        print(f"  R0={self.R[0]}  R1={self.R[1]}  R2={self.R[2]}  R3={self.R[3]}")


# ---------------------------------------------------------------------------
# Demo programs
# ---------------------------------------------------------------------------

LOAD  = lambda r, addr: encode(0x1, r, (addr>>4)&0xF, addr&0xF)
STORE = lambda r, addr: encode(0x2, r, (addr>>4)&0xF, addr&0xF)
MOV   = lambda rd, rs:  encode(0x3, rd, rs)
ADD   = lambda rd, rs:  encode(0x4, rd, rs)
SUB   = lambda rd, rs:  encode(0x5, rd, rs)
AND_  = lambda rd, rs:  encode(0x6, rd, rs)
OR_   = lambda rd, rs:  encode(0x7, rd, rs)
NOT_  = lambda rd:      encode(0x8, rd)
JMP   = lambda addr:    encode(0x9, (addr>>8)&0xF, (addr>>4)&0xF, addr&0xF)
JZ    = lambda addr:    encode(0xA, (addr>>8)&0xF, (addr>>4)&0xF, addr&0xF)
JNZ   = lambda addr:    encode(0xB, (addr>>8)&0xF, (addr>>4)&0xF, addr&0xF)
MOVI  = lambda rd, imm: encode(0xC, rd, 0, imm)
HLT   = lambda:         encode(0xF)


def demo_add():
    """Program: R0 = MEM[0x20] + MEM[0x21]; store result in MEM[0x22]."""
    prog = [
        LOAD(0, 0x20),    # R0 = MEM[0x20]
        LOAD(1, 0x21),    # R1 = MEM[0x21]
        ADD(0, 1),        # R0 = R0 + R1
        STORE(0, 0x22),   # MEM[0x22] = R0
        HLT(),
    ]
    data = {0x20: 15, 0x21: 27}
    cpu = PrimitiveCPU(trace=("--trace" in sys.argv))
    cpu.load_program(prog, data, start=0)

    print("Program 1: Add two memory values (15 + 27)")
    cpu.run()
    cpu.dump()
    print(f"  MEM[0x22] = {cpu.MEM[0x22]}  (expected 42)")


def demo_countdown():
    """Program: count down from 5 to 0, then halt."""
    prog = [
        MOVI(0, 5),       # addr 0: R0 = 5
        SUB(0, 0),        # addr 1: R0 = R0 - R0 (set zero flag if R0==0) -- wait, need CMP
        # Instead: use MOVI R1,1 then loop: R0=R0-R1 until R0==0
        MOVI(0, 5),       # addr 0: R0 = 5   (restart)
        MOVI(1, 1),       # addr 1: R1 = 1
        # loop at addr 2:
        SUB(0, 1),        # addr 2: R0 = R0 - 1;  sets ACC=R0; ZF if R0 became 0
        JNZ(2),           # addr 3: if ACC!=0 goto addr 2
        HLT(),            # addr 4
    ]
    # trim the redundant first two instructions – rewrite cleanly
    prog = [
        MOVI(0, 5),       # 0: R0 = 5
        MOVI(1, 1),       # 1: R1 = 1
        SUB(0, 1),        # 2: R0 = R0 - 1
        JNZ(2),           # 3: if R0 != 0 goto 2
        HLT(),            # 4: done
    ]
    cpu = PrimitiveCPU(trace=("--trace" in sys.argv))
    cpu.load_program(prog, start=0)

    print("\nProgram 2: Count down from 5 to 0")
    cpu.run()
    cpu.dump()
    print(f"  R0 = {cpu.R[0]}  (expected 0)  Cycles = {cpu.cycles}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    demo_add()
    demo_countdown()


if __name__ == "__main__":
    main()
