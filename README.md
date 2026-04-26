# Computer Organization and Architecture

## Contents

### PC Building Simulator (Labs 1–3)
An interactive Windows application for identifying, assembling, and disassembling PC components. Runs via Wine + noVNC inside this devcontainer.

```bash
bash scripts/start-pcbuilder.sh
# open http://localhost:6080/vnc.html
```

### EMU8086 (Labs 4–6)
8086 microprocessor emulator for running TASM assembly programs.

```bash
bash scripts/start-emu8086.sh
# open http://localhost:6080/vnc.html
```

### Logisim Evolution (Labs 7–13)
Java-based logic gate simulator for designing and testing combinational circuits (adders, multipliers, parallel adder/subtractor, carry-save multiplier, ALU, MUX). Runs natively — no Wine required.

```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html
```

### COA Labs (Labs 1–15)
PC hardware identification and assembly/disassembly (Labs 1–3); 8086 TASM assembly with full programs and algorithms (Labs 4–6); gate-level circuit design — half/full adders, RCA, CLA, array multiplier, binary parallel adder/subtractor, carry-save multiplier, MUX, ALU (Labs 7–13); primitive CPU with fetch-decode-execute cycle (Lab 14); 5-stage pipeline with hazard analysis (Lab 15). All labs include answered questions.

```bash
bash labs/tests/run_tests.sh   # run all automated tests
```

See [labs/README.md](labs/README.md) for the full lab index and per-lab run instructions.

## Lab Sessions

| Session | Labs |
|---------|------|
| S4–5 | Lab 1 (PC components), Lab 4 (TASM 8-bit), Lab 7 (Adders), Lab 10 (Array Multiplier), Lab 13 (Carry Save) |
| S9–10 | Lab 2 (PC assembly), Lab 5 (TASM 16-bit), Lab 8 (Ripple Carry), Lab 11 (Booth study), Lab 14 (Processing Unit) |
| S14–15 | Lab 3 (PC disassembly), Lab 6 (Multiplication), Lab 9 (CLA), Lab 12 (Booth program), Lab 15 (Pipeline) |
