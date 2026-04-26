# Computer Organization and Architecture – Labs

15 lab sessions covering PC hardware, 8086 assembly programming, digital arithmetic circuits, multiplication algorithms, and CPU/pipeline design.

## Lab Overview

| Lab | Session | Topic | Type |
|-----|---------|-------|------|
| 01 | S4–5 | Recognize PC components (I/O, Processing, Memory) | PC Simulator |
| 02 | S9–10 | PC component connections; Assembly | PC Simulator |
| 03 | S14–15 | PC disassembly | PC Simulator |
| 04 | S4–5 | TASM – 8-bit addition and subtraction | ASM + Python |
| 05 | S9–10 | 16-bit addition and subtraction | ASM + Python |
| 06 | S14–15 | 8-bit multiplication; Factorial program | ASM + Python |
| 07 | S4–5 | Half Adder and Full Adder | Python |
| 08 | S9–10 | Ripple Carry Adder | Python |
| 09 | S14–15 | Carry Look-Ahead Adder | Python |
| 10 | S4–5 | Array Multiplier | Python |
| 11 | S9–10 | Booth Algorithm study (step-by-step trace) | Python |
| 12 | S14–15 | Booth Algorithm program implementation | Python |
| 13 | S4–5 | Carry Save Multiplication | Python |
| 14 | S9–10 | Primitive Processing Unit | Python |
| 15 | S14–15 | Pipeline concepts; Basic pipeline design | Python |

## Directory Structure

```
.
├── scripts/
│   ├── start-pcbuilder.sh
│   ├── start-emu8086.sh
│   └── start-logicgate.sh
├── simulators/
│   ├── pc-building-simulator/
│   ├── emu8086/                   ← setup.exe (Wine)
│   ├── logic-gate-simulator/      ← GateSimSetup-1.4.msi (unused)
│   └── logisim-evolution.jar      ← active logic gate simulator (Java)
└── labs/
    ├── README.md
    ├── asm_simulator.py           ← shared 8086 simulator for labs 4–6
    ├── lab01_pc_components/
    ├── lab02_pc_assembly/
    ├── lab03_pc_disassembly/
    ├── lab04_tasm_8bit/
    ├── lab05_tasm_16bit/
    ├── lab06_multiplication/
    ├── lab07_adders/
    ├── lab08_ripple_carry_adder/
    ├── lab09_carry_lookahead/
    ├── lab10_array_multiplier/
    ├── lab11_booth_study/
    ├── lab12_booth_program/
    ├── lab13_carry_save/
    ├── lab14_processing_unit/
    ├── lab15_pipeline/
    └── tests/
        └── run_tests.sh
```

## Running Labs 1–3 (PC Building Simulator)
```bash
bash scripts/start-pcbuilder.sh
# open http://localhost:6080/vnc.html in your browser
```

## Running EMU8086 (Labs 4–6 — Windows emulator)
```bash
bash scripts/start-emu8086.sh
# open http://localhost:6080/vnc.html in your browser
```

## Running Logisim Evolution (Labs 7–13 — Logic Gate Simulator)
```bash
bash scripts/start-logicgate.sh
# open http://localhost:6080/vnc.html in your browser
```

## Running Labs 4–6 (8086 Assembly Simulator)
```bash
cd labs/
python3 asm_simulator.py lab04_tasm_8bit/add_8bit.asm
python3 asm_simulator.py lab04_tasm_8bit/sub_8bit.asm
python3 asm_simulator.py lab05_tasm_16bit/add_16bit.asm
python3 asm_simulator.py lab06_multiplication/factorial.asm
```

## Running Labs 7–15 (Python Simulators)
```bash
cd labs/
python3 lab07_adders/adders.py
python3 lab08_ripple_carry_adder/ripple_carry_adder.py
python3 lab09_carry_lookahead/carry_lookahead_adder.py
python3 lab10_array_multiplier/array_multiplier.py
python3 lab11_booth_study/booth_trace.py
python3 lab12_booth_program/booth.py
python3 lab13_carry_save/carry_save.py
python3 lab14_processing_unit/primitive_cpu.py
python3 lab15_pipeline/pipeline.py
```

## Running All Tests
```bash
bash labs/tests/run_tests.sh
```
