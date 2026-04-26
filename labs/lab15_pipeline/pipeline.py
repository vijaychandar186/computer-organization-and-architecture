#!/usr/bin/env python3
"""Lab 15 – 5-Stage Instruction Pipeline Simulator.

Simulates a classic 5-stage RISC pipeline:
  IF  – Instruction Fetch
  ID  – Instruction Decode / Register Read
  EX  – Execute (ALU)
  MEM – Memory Access
  WB  – Write Back

Features:
  - Pipeline diagram (Gantt-chart style)
  - Data hazard detection with stall insertion
  - Control hazard detection (branch flush)
  - Throughput and CPI metrics

Run:
  python3 pipeline.py              # demo with two instruction sequences
  python3 pipeline.py --no-stall   # show ideal (no hazard) pipeline
"""

import sys
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Instruction model
# ---------------------------------------------------------------------------

@dataclass
class Instruction:
    name:   str
    dst:    str | None = None   # destination register
    src1:   str | None = None   # source register 1
    src2:   str | None = None   # source register 2
    is_branch: bool = False
    is_load:   bool = False
    is_store:  bool = False
    is_nop:    bool = False

    def __str__(self):
        parts = [self.name]
        if self.dst:  parts.append(self.dst)
        if self.src1: parts.append(self.src1)
        if self.src2: parts.append(self.src2)
        return " ".join(parts)


NOP = Instruction("NOP", is_nop=True)


# ---------------------------------------------------------------------------
# Pipeline stage names
# ---------------------------------------------------------------------------

STAGES = ["IF", "ID", "EX", "MEM", "WB"]
NSTAGES = len(STAGES)


# ---------------------------------------------------------------------------
# Hazard detection
# ---------------------------------------------------------------------------

def has_data_hazard(current: Instruction, pipeline: list[Instruction | None]) -> bool:
    """Return True if current needs a register that is not yet written back.

    pipeline[0]=EX  pipeline[1]=MEM  pipeline[2]=WB  (stages ahead)
    Hazard if: a register read by current is the destination written by
    an instruction still in EX or MEM (i.e., not yet in WB).
    """
    needs = {r for r in (current.src1, current.src2) if r}
    for instr in pipeline:
        if instr and not instr.is_nop and instr.dst and instr.dst in needs:
            return True
    return False


def load_use_hazard(current: Instruction, ex_stage: Instruction | None) -> bool:
    """Load-use hazard: instruction in EX is a LOAD that writes a register
    needed by the current instruction. Requires an extra stall."""
    if ex_stage and ex_stage.is_load and ex_stage.dst:
        needs = {current.src1, current.src2} - {None}
        if ex_stage.dst in needs:
            return True
    return False


# ---------------------------------------------------------------------------
# Pipeline simulator
# ---------------------------------------------------------------------------

class Pipeline:
    def __init__(self, instructions: list[Instruction], enable_hazards: bool = True):
        self.program       = list(instructions)
        self.enable_hazards = enable_hazards
        self.clock         = 0
        self.stalls        = 0
        self.flushes       = 0

        # pipeline register: each holds the instruction occupying that stage
        self.stage_reg: list[Instruction | None] = [None] * NSTAGES
        # IF, ID, EX, MEM, WB = indices 0..4

        self.pc            = 0
        self.halted        = False
        self.log: list[dict] = []   # {clock: int, stages: list[str]}

    def _snapshot(self):
        self.log.append({
            "clock":  self.clock,
            "stages": [str(s) if s and not s.is_nop else ("NOP" if s else "---")
                       for s in self.stage_reg],
        })

    def tick(self):
        self.clock += 1

        stall = False
        flush = False

        if self.enable_hazards:
            # Check load-use hazard (needs 2 stalls: one here + the NOP insertion)
            next_instr = self.program[self.pc] if self.pc < len(self.program) else None
            if next_instr and load_use_hazard(next_instr, self.stage_reg[2]):  # EX
                stall = True
                self.stalls += 1

            # Check branch in EX: flush IF and ID
            if self.stage_reg[2] and self.stage_reg[2].is_branch:
                flush = True
                self.flushes += 2

        # Advance pipeline (WB retires, shift down)
        # WB  ← MEM
        # MEM ← EX
        # EX  ← ID  (or NOP on stall)
        # ID  ← IF  (or NOP on stall)
        # IF  ← fetch next (or re-fetch on stall)

        self.stage_reg[4] = self.stage_reg[3]   # WB  ← MEM
        self.stage_reg[3] = self.stage_reg[2]   # MEM ← EX
        self.stage_reg[2] = self.stage_reg[1] if not stall else NOP   # EX ← ID
        self.stage_reg[1] = self.stage_reg[0] if not stall else NOP   # ID ← IF

        if flush:
            self.stage_reg[2] = NOP
            self.stage_reg[1] = NOP

        # Fetch next instruction
        if not stall:
            if self.pc < len(self.program):
                self.stage_reg[0] = self.program[self.pc]
                self.pc += 1
            else:
                self.stage_reg[0] = None

        self._snapshot()

    def run(self):
        # Drain: keep ticking until all stages are empty
        while True:
            self.tick()
            active = any(s and not s.is_nop for s in self.stage_reg)
            if not active and self.pc >= len(self.program):
                # a few more ticks to drain WB
                for _ in range(NSTAGES - 1):
                    self.tick()
                break

    def print_diagram(self):
        n_clocks = self.log[-1]["clock"] if self.log else 0
        print(f"\n  Pipeline Diagram (clock cycles)")
        print(f"  {'Cycle':>6}", end="")
        for c in range(1, n_clocks + 1):
            print(f"  {c:>3}", end="")
        print()
        print("  " + "─" * (8 + 5 * n_clocks))

        # Track where each instruction appears in each stage
        instr_timeline: dict[str, list[str]] = {}
        for entry in self.log:
            c = entry["clock"]
            for stage_i, label in enumerate(entry["stages"]):
                stage = STAGES[stage_i]
                if label and label not in ("---", "NOP"):
                    if label not in instr_timeline:
                        instr_timeline[label] = ["   "] * (n_clocks + 1)
                    instr_timeline[label][c] = stage[:2]

        for instr in self.program:
            name = str(instr)
            row = instr_timeline.get(name, ["   "] * (n_clocks + 1))
            print(f"  {name:>20}", end="")
            for c in range(1, n_clocks + 1):
                print(f"  {row[c]:>3}", end="")
            print()

        print()
        n_instr = len([i for i in self.program if not i.is_nop])
        cpi = (n_clocks / n_instr) if n_instr else 0
        print(f"  Instructions : {n_instr}")
        print(f"  Total cycles : {n_clocks}")
        print(f"  Stalls       : {self.stalls}")
        print(f"  Flushes      : {self.flushes}")
        print(f"  CPI          : {cpi:.2f}  (ideal = 1.00)")


# ---------------------------------------------------------------------------
# Demo programs
# ---------------------------------------------------------------------------

def demo_no_hazards():
    prog = [
        Instruction("ADD", "R1", "R2", "R3"),
        Instruction("SUB", "R4", "R5", "R6"),
        Instruction("AND", "R7", "R1", "R4"),
        Instruction("OR",  "R8", "R2", "R5"),
        Instruction("MOV", "R9", "R3"),
    ]
    print("=" * 55)
    print("Example 1: No data hazards")
    print("=" * 55)
    p = Pipeline(prog, enable_hazards=("--no-stall" not in sys.argv))
    p.run()
    p.print_diagram()


def demo_data_hazard():
    # RAW hazard: ADD writes R1; next SUB reads R1 before WB
    prog = [
        Instruction("ADD",  "R1", "R2", "R3"),   # R1 = R2 + R3
        Instruction("SUB",  "R4", "R1", "R5"),   # R4 = R1 - R5  ← RAW on R1
        Instruction("MUL",  "R6", "R4", "R7"),   # R6 = R4 * R7  ← RAW on R4
        Instruction("LOAD", "R8", None, None, is_load=True),  # R8 = MEM[...]
        Instruction("ADD",  "R9", "R8", "R1"),   # R9 = R8 + R1  ← load-use on R8
        Instruction("STORE","R9", None, None, is_store=True),
    ]
    prog[3].dst = "R8"
    print("=" * 55)
    print("Example 2: Data hazards (RAW + load-use)")
    print("=" * 55)
    p = Pipeline(prog, enable_hazards=("--no-stall" not in sys.argv))
    p.run()
    p.print_diagram()


def demo_control_hazard():
    prog = [
        Instruction("LOAD",   "R1", is_load=True),
        Instruction("BEQ",    None, "R1", "R0", is_branch=True),
        Instruction("ADD",    "R2", "R3", "R4"),   # flushed if branch taken
        Instruction("SUB",    "R5", "R6", "R7"),   # flushed if branch taken
        Instruction("AND",    "R8", "R1", "R2"),   # branch target
    ]
    prog[0].dst = "R1"
    print("=" * 55)
    print("Example 3: Control hazard (branch flush)")
    print("=" * 55)
    p = Pipeline(prog, enable_hazards=("--no-stall" not in sys.argv))
    p.run()
    p.print_diagram()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    demo_no_hazards()
    print()
    demo_data_hazard()
    print()
    demo_control_hazard()


if __name__ == "__main__":
    main()
