#!/usr/bin/env python3
"""Minimal 8086 / TASM-style simulator for COA labs 4-6.

Supported instructions:
  MOV, ADD, SUB, MUL, NOT, INC, DEC, CMP, JMP, JE, JZ, JNE, JNZ, JCXZ, HLT
  int 3  (breakpoint – dumps registers and variables, then continues)
  int 21h (terminate)

Addressing modes handled:
  immediate  – MOV AL, 04h
  register   – MOV AX, BX
  direct mem – MOV AL, N1   /   MOV N2, AL

Segment directives (DATA SEGMENT … DATA ENDS, CODE SEGMENT, ASSUME, END) are
parsed for variable declarations and ignored otherwise.

Run:
  python3 asm_simulator.py <program.asm>
"""

import re
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_imm(token: str) -> int:
    t = token.strip().rstrip("hHbBoO")
    raw = token.strip()
    if raw.lower().endswith("h"):
        return int(raw[:-1], 16)
    if raw.lower().endswith("b"):
        return int(raw[:-1], 2)
    if raw.lower().endswith("o"):
        return int(raw[:-1], 8)
    return int(raw, 0)


_8BIT  = {"AL", "AH", "BL", "BH", "CL", "CH", "DL", "DH"}
_16BIT = {"AX", "BX", "CX", "DX", "SI", "DI", "SP", "BP"}
_ALL_REGS = _8BIT | _16BIT


# ---------------------------------------------------------------------------
# CPU
# ---------------------------------------------------------------------------

class CPU8086:
    def __init__(self):
        self.regs = {r: 0 for r in _16BIT}
        self.flags = {"ZF": 0, "CF": 0, "SF": 0, "OF": 0}
        self.memory: dict[str, int] = {}
        self.mem_type: dict[str, str] = {}  # 'db' or 'dw'

    # -- register access ---------------------------------------------------

    def _parent(self, name: str):
        return {"AL": "AX", "AH": "AX",
                "BL": "BX", "BH": "BX",
                "CL": "CX", "CH": "CX",
                "DL": "DX", "DH": "DX"}[name]

    def get(self, name: str) -> int:
        name = name.upper()
        if name in _16BIT:
            return self.regs[name]
        if name in _8BIT:
            v = self.regs[self._parent(name)]
            return v & 0xFF if name[1] == "L" else (v >> 8) & 0xFF
        if name in self.memory:
            return self.memory[name]
        return _parse_imm(name)

    def set(self, name: str, value: int):
        name = name.upper()
        if name in _16BIT:
            self.regs[name] = value & 0xFFFF
        elif name in _8BIT:
            p = self._parent(name)
            v = self.regs[p]
            if name[1] == "L":
                self.regs[p] = (v & 0xFF00) | (value & 0xFF)
            else:
                self.regs[p] = (v & 0x00FF) | ((value & 0xFF) << 8)
        elif name in self.memory:
            mask = 0xFF if self.mem_type.get(name) == "db" else 0xFFFF
            self.memory[name] = value & mask
        else:
            raise ValueError(f"Unknown destination: {name}")

    def is_8bit(self, name: str) -> bool:
        return name.upper() in _8BIT

    def operand_bits(self, name: str) -> int:
        name = name.upper()
        if name in _8BIT:
            return 8
        if name in _16BIT:
            return 16
        if name in self.memory:
            return 8 if self.mem_type.get(name) == "db" else 16
        return 16

    # -- flags -------------------------------------------------------------

    def _update_flags(self, result: int, bits: int):
        mask = (1 << bits) - 1
        self.flags["ZF"] = 1 if (result & mask) == 0 else 0
        self.flags["SF"] = 1 if (result >> (bits - 1)) & 1 else 0
        self.flags["CF"] = 1 if result > mask or result < 0 else 0

    # -- display -----------------------------------------------------------

    def dump(self):
        print("\n--- Register Dump ---")
        for r in ("AX", "BX", "CX", "DX"):
            v = self.regs[r]
            rh, rl = r[0] + "H", r[0] + "L"
            print(f"  {r}={v:04X}h  {rh}={v>>8:02X}h  {rl}={v&0xFF:02X}h  ({v})")
        if self.memory:
            print("--- Memory Variables ---")
            for name, val in self.memory.items():
                t = self.mem_type.get(name, "dw")
                if t == "db":
                    print(f"  {name} = {val:02X}h  ({val})")
                else:
                    print(f"  {name} = {val:04X}h  ({val})")
        print(f"Flags: ZF={self.flags['ZF']} CF={self.flags['CF']} "
              f"SF={self.flags['SF']} OF={self.flags['OF']}")
        print("---------------------")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _strip_comment(line: str) -> str:
    i = line.find(";")
    return line[:i].strip() if i >= 0 else line.strip()


def parse(source: str):
    """Return (variables, instructions, labels).

    variables : {name: int}
    mem_types : {name: 'db'|'dw'}
    instructions: list of (original_line_no, tokens_list)
    labels: {label_name: instruction_index}
    """
    variables: dict[str, int] = {}
    mem_types: dict[str, str] = {}
    instructions: list[tuple[int, list[str]]] = []
    labels: dict[str, int] = {}

    in_data = False
    in_code = False

    for lineno, raw in enumerate(source.splitlines(), 1):
        line = _strip_comment(raw)
        if not line:
            continue
        upper = line.upper()

        # segment boundaries
        if re.match(r"DATA\s+(SEGMENT|ENDS)", upper):
            in_data = "SEGMENT" in upper
            in_code = False
            continue
        if re.match(r"CODE\s+(SEGMENT|ENDS)", upper):
            in_code = "SEGMENT" in upper
            in_data = False
            continue
        if upper.startswith("ASSUME") or upper.startswith("END"):
            continue

        # data declarations
        if in_data:
            m = re.match(r"(\w+)\s+(DB|DW)\s+(.+)", line, re.IGNORECASE)
            if m:
                name, kind, val_str = m.group(1), m.group(2).lower(), m.group(3).strip()
                if val_str == "?":
                    value = 0
                else:
                    try:
                        value = _parse_imm(val_str)
                    except ValueError:
                        value = 0
                variables[name] = value
                mem_types[name] = kind
            continue

        if not in_code:
            continue

        # label?
        if ":" in line:
            parts = line.split(":", 1)
            lbl = parts[0].strip()
            labels[lbl.upper()] = len(instructions)
            rest = parts[1].strip()
            if not rest:
                continue
            line = rest

        # tokenise
        tokens = re.split(r"[\s,]+", line)
        tokens = [t for t in tokens if t]
        if tokens:
            instructions.append((lineno, tokens))

    return variables, mem_types, instructions, labels


# ---------------------------------------------------------------------------
# Executor
# ---------------------------------------------------------------------------

def execute(source: str, trace: bool = False):
    variables, mem_types, instructions, labels = parse(source)

    cpu = CPU8086()
    cpu.memory = dict(variables)
    cpu.mem_type = dict(mem_types)

    pc = 0
    max_steps = 100_000

    for step in range(max_steps):
        if pc >= len(instructions):
            break

        lineno, tokens = instructions[pc]
        op = tokens[0].upper()

        if trace:
            print(f"[{pc:3}] {' '.join(tokens)}")

        # ---------------- MOV ----------------
        if op == "MOV":
            dst, src = tokens[1], tokens[2]
            dst_u = dst.upper()
            src_u = src.upper()
            # ignore segment register loads: MOV DS,AX  and  MOV AX,data
            _SEG_REGS = {"DS", "CS", "SS", "ES"}
            _SEG_NAMES = {"DATA", "CODE", "STACK"}
            if (dst_u in _SEG_REGS or src_u in _SEG_REGS
                    or src_u in _SEG_NAMES or dst_u in _SEG_NAMES):
                pc += 1
                continue
            val = cpu.get(src_u) if (src_u in _ALL_REGS or src_u in cpu.memory) else _parse_imm(src)
            if dst_u in _ALL_REGS:
                cpu.set(dst_u, val)
            elif dst_u in cpu.memory:
                cpu.set(dst_u, val)
            else:
                raise ValueError(f"Line {lineno}: unknown MOV destination '{dst}'")

        # ---------------- ADD ----------------
        elif op == "ADD":
            dst, src = tokens[1].upper(), tokens[2].upper()
            a = cpu.get(dst)
            b = cpu.get(src) if (src in _ALL_REGS or src in cpu.memory) else _parse_imm(tokens[2])
            result = a + b
            bits = cpu.operand_bits(dst)
            cpu._update_flags(result, bits)
            cpu.set(dst, result)

        # ---------------- SUB ----------------
        elif op == "SUB":
            dst, src = tokens[1].upper(), tokens[2].upper()
            a = cpu.get(dst)
            b = cpu.get(src) if (src in _ALL_REGS or src in cpu.memory) else _parse_imm(tokens[2])
            result = a - b
            bits = cpu.operand_bits(dst)
            cpu._update_flags(result, bits)
            cpu.set(dst, result)

        # ---------------- MUL ----------------
        elif op == "MUL":
            src = tokens[1].upper()
            if src in _8BIT or (src in cpu.memory and cpu.mem_type.get(src) == "db"):
                # 8-bit: AX = AL * src8
                al = cpu.get("AL")
                b  = cpu.get(src) if src in _8BIT else cpu.memory[src]
                result = al * b
                cpu.set("AX", result & 0xFFFF)
                cpu.flags["CF"] = cpu.flags["OF"] = 1 if result > 0xFF else 0
            else:
                # 16-bit: DX:AX = AX * src16
                ax = cpu.get("AX")
                b  = cpu.get(src) if src in _16BIT else cpu.memory.get(src, 0)
                result = ax * b
                cpu.set("AX", result & 0xFFFF)
                cpu.set("DX", (result >> 16) & 0xFFFF)
                cpu.flags["CF"] = cpu.flags["OF"] = 1 if result > 0xFFFF else 0

        # ---------------- NOT ----------------
        elif op == "NOT":
            dst = tokens[1].upper()
            bits = cpu.operand_bits(dst)
            mask = (1 << bits) - 1
            cpu.set(dst, (~cpu.get(dst)) & mask)

        # ---------------- INC / DEC ----------
        elif op == "INC":
            dst = tokens[1].upper()
            bits = cpu.operand_bits(dst)
            result = cpu.get(dst) + 1
            cpu._update_flags(result, bits)
            cpu.set(dst, result)

        elif op == "DEC":
            dst = tokens[1].upper()
            bits = cpu.operand_bits(dst)
            result = cpu.get(dst) - 1
            cpu._update_flags(result, bits)
            cpu.set(dst, result)

        # ---------------- CMP ----------------
        elif op == "CMP":
            a_tok, b_tok = tokens[1].upper(), tokens[2]
            a = cpu.get(a_tok)
            b = cpu.get(b_tok.upper()) if b_tok.upper() in _ALL_REGS else _parse_imm(b_tok)
            result = a - b
            bits = cpu.operand_bits(a_tok)
            cpu._update_flags(result, bits)

        # ---------------- Jumps --------------
        elif op == "JMP":
            lbl = tokens[1].upper()
            if lbl not in labels:
                raise ValueError(f"Line {lineno}: undefined label '{tokens[1]}'")
            pc = labels[lbl]
            continue

        elif op in ("JE", "JZ"):
            if cpu.flags["ZF"]:
                pc = labels[tokens[1].upper()]
                continue

        elif op in ("JNE", "JNZ"):
            if not cpu.flags["ZF"]:
                pc = labels[tokens[1].upper()]
                continue

        elif op == "JCXZ":
            if cpu.get("CX") == 0:
                pc = labels[tokens[1].upper()]
                continue

        # ---------------- INT ----------------
        elif op == "INT":
            code = tokens[1].upper().rstrip("H")
            if code == "3":
                cpu.dump()
            elif code in ("21", "21H"):
                cpu.dump()
                print("Program terminated (INT 21h).")
                return cpu
            # else ignore other interrupts

        elif op == "HLT":
            cpu.dump()
            print("CPU halted.")
            return cpu

        # unknown → skip silently (handles pseudo-ops like PROC/ENDP)
        pc += 1

    cpu.dump()
    return cpu


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 asm_simulator.py <program.asm> [--trace]")
        sys.exit(1)

    asm_file = sys.argv[1]
    trace = "--trace" in sys.argv

    try:
        with open(asm_file) as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{asm_file}' not found.")
        sys.exit(1)

    print(f"Running: {asm_file}")
    execute(source, trace=trace)


if __name__ == "__main__":
    main()
