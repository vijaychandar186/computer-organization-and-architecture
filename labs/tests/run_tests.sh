#!/usr/bin/env bash
# run_tests.sh – Compile and smoke-test all COA lab programs.
# Usage: bash labs/tests/run_tests.sh
# Requirements: g++ (C++17), python3

set -euo pipefail
CXX=${CXX:-g++}
CXXFLAGS="-std=c++17 -O2 -Wall"
PYTHON=${PYTHON:-python3}
LABS="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0

# ── helpers ────────────────────────────────────────────────────────────────

run_cpp() {
    local label="$1" src="$2" input="$3" expected="$4"
    local bin; bin=$(mktemp /tmp/coa_XXXXXX)
    if ! $CXX $CXXFLAGS "$LABS/$src" -o "$bin" 2>/dev/null; then
        echo "[FAIL] $label  (compile error)"; FAIL=$((FAIL+1)); return
    fi
    local out; out=$(echo "$input" | timeout 5 "$bin" 2>/dev/null || true)
    rm -f "$bin"
    if echo "$out" | grep -qF -- "$expected"; then
        echo "[PASS] $label"; PASS=$((PASS+1))
    else
        echo "[FAIL] $label"; echo "       expected: $expected"; echo "       got: $(echo "$out"|head -3)"; FAIL=$((FAIL+1))
    fi
}

run_cpp_noargs() {
    local label="$1" src="$2" expected="$3"; shift 3
    local bin; bin=$(mktemp /tmp/coa_XXXXXX)
    if ! $CXX $CXXFLAGS "$LABS/$src" -o "$bin" 2>/dev/null; then
        echo "[FAIL] $label  (compile error)"; FAIL=$((FAIL+1)); return
    fi
    local out; out=$(timeout 5 "$bin" "$@" 2>/dev/null || true)
    rm -f "$bin"
    if echo "$out" | grep -qF -- "$expected"; then
        echo "[PASS] $label"; PASS=$((PASS+1))
    else
        echo "[FAIL] $label"; echo "       expected: $expected"; echo "       got: $(echo "$out"|head -3)"; FAIL=$((FAIL+1))
    fi
}

run_py() {
    local label="$1" script="$2" input="$3" expected="$4"; shift 4
    local out; out=$(echo "$input" | timeout 10 $PYTHON "$LABS/$script" "$@" 2>/dev/null || true)
    if echo "$out" | grep -qF -- "$expected"; then
        echo "[PASS] $label"; PASS=$((PASS+1))
    else
        echo "[FAIL] $label"; echo "       expected: $expected"; echo "       got: $(echo "$out"|head -3)"; FAIL=$((FAIL+1))
    fi
}

run_asm() {
    local label="$1" asm="$2" expected="$3"
    local out; out=$(timeout 10 $PYTHON "$LABS/asm_simulator.py" "$LABS/$asm" 2>/dev/null || true)
    if echo "$out" | grep -qF -- "$expected"; then
        echo "[PASS] $label"; PASS=$((PASS+1))
    else
        echo "[FAIL] $label"; echo "       expected: $expected"; echo "       got: $(echo "$out"|head -5)"; FAIL=$((FAIL+1))
    fi
}

# ══════════════════════════════════════════════════════════════════════════
echo "=== COA Labs – Test Suite ==="
echo ""

# ── Lab 4: 8-bit ASM ──────────────────────────────────────────────────────
run_asm "Lab04 add_8bit  (04h+01h=05h)" \
    "lab04_tasm_8bit/add_8bit.asm"  "AL=05"

run_asm "Lab04 sub_8bit  (09h-03h=06h)" \
    "lab04_tasm_8bit/sub_8bit.asm"  "AL=06"

# ── Lab 5: 16-bit ASM ─────────────────────────────────────────────────────
run_asm "Lab05 add_16bit (4004h+1001h=5005h)" \
    "lab05_tasm_16bit/add_16bit.asm"  "AX=5005"

run_asm "Lab05 sub_16bit (4004h-1001h=3003h)" \
    "lab05_tasm_16bit/sub_16bit.asm"  "AX=3003"

# ── Lab 6: Multiplication + Factorial ────────────────────────────────────
run_asm "Lab06 mul_8bit  (04h*03h=0Ch)" \
    "lab06_multiplication/mul_8bit.asm"  "AX=000C"

run_asm "Lab06 factorial (5!=78h)" \
    "lab06_multiplication/factorial.asm"  "AX=0078"

# ── Lab 7: Adders (C++) ───────────────────────────────────────────────────
run_cpp_noargs "Lab07 C++ half adder table" \
    "lab07_adders/adders.cpp"  "Half Adder Truth Table"

run_cpp_noargs "Lab07 C++ full adder table" \
    "lab07_adders/adders.cpp"  "Full Adder Truth Table"

# ── Lab 7: Adders (Python) ────────────────────────────────────────────────
run_py "Lab07 Python half adder" \
    "lab07_adders/adders.py"  ""  "Half Adder Truth Table"

run_py "Lab07 Python full adder" \
    "lab07_adders/adders.py"  ""  "Full Adder Truth Table"

# ── Lab 8: Ripple Carry Adder (C++) ──────────────────────────────────────
run_cpp "Lab08 C++ RCA 5+3=8" \
    "lab08_ripple_carry_adder/ripple_carry_adder.cpp"  "5 3 4"  "Sum: 1000  (8)"

run_cpp "Lab08 C++ RCA 60+20" \
    "lab08_ripple_carry_adder/ripple_carry_adder.cpp"  "60 20 8"  "(80)"

# ── Lab 8: RCA (Python) ───────────────────────────────────────────────────
run_py "Lab08 Python RCA 5+3=8" \
    "lab08_ripple_carry_adder/ripple_carry_adder.py"  ""  "Sum      = 1000  (8)"  5 3 4

# ── Lab 9: CLA (C++) ──────────────────────────────────────────────────────
run_cpp "Lab09 C++ CLA 5+3=8" \
    "lab09_carry_lookahead/carry_lookahead_adder.cpp"  "5 3 4"  "Sum  = 1000  (8)"

run_cpp "Lab09 C++ CLA equations" \
    "lab09_carry_lookahead/carry_lookahead_adder.cpp"  "13 11 4"  "Look-Ahead"

# ── Lab 9: CLA (Python) ───────────────────────────────────────────────────
run_py "Lab09 Python CLA 5+3=8" \
    "lab09_carry_lookahead/carry_lookahead_adder.py"  ""  "Sum  = 1000  (8)"  5 3 4

# ── Lab 10: Array Multiplier (C++) ────────────────────────────────────────
run_cpp "Lab10 C++ array mult 6x5=30" \
    "lab10_array_multiplier/array_multiplier.cpp"  "6 5 4"  "6 x 5 = 30"

run_cpp "Lab10 C++ array mult 13x11=143" \
    "lab10_array_multiplier/array_multiplier.cpp"  "13 11 4"  "13 x 11 = 143"

# ── Lab 10: Array Multiplier (Python) ────────────────────────────────────
run_py "Lab10 Python array mult 6x5=30" \
    "lab10_array_multiplier/array_multiplier.py"  ""  "6 × 5 = 30"  6 5 4

# ── Lab 11: Booth Trace (C++) ─────────────────────────────────────────────
run_cpp "Lab11 C++ booth trace -3x7=-21" \
    "lab11_booth_study/booth_trace.cpp"  "-3 7 4"  "PASS"

run_cpp "Lab11 C++ booth trace 3x5=15" \
    "lab11_booth_study/booth_trace.cpp"  "3 5 4"  "PASS"

# ── Lab 11: Booth Trace (Python) ──────────────────────────────────────────
run_py "Lab11 Python booth trace" \
    "lab11_booth_study/booth_trace.py"  ""  "-3 × 7 = -21"  -3 7 4

# ── Lab 12: Booth Program (C++) ──────────────────────────────────────────
run_cpp_noargs "Lab12 C++ booth test suite" \
    "lab12_booth_program/booth.cpp"  "All tests passed."

run_cpp_noargs "Lab12 C++ booth -3x7" \
    "lab12_booth_program/booth.cpp"  "-21"  "-3" "7"

# ── Lab 12: Booth Program (Python) ────────────────────────────────────────
run_py "Lab12 Python booth test suite" \
    "lab12_booth_program/booth.py"  ""  "All tests passed."

# ── Lab 13: Carry Save (C++) ─────────────────────────────────────────────
run_cpp "Lab13 C++ CSA 13+11+7" \
    "lab13_carry_save/carry_save.cpp"  "13 11 7 5"  "Match: OK"

run_cpp_noargs "Lab13 C++ CSA multiply 6x5=30" \
    "lab13_carry_save/carry_save.cpp"  "Product  = 30"  "--multiply" "6" "5" "4"

# ── Lab 13: Carry Save (Python) ───────────────────────────────────────────
run_py "Lab13 Python CSA 13+11+7" \
    "lab13_carry_save/carry_save.py"  ""  "Match    : ✓"  13 11 7

# ── Lab 14: Primitive CPU (C++) ──────────────────────────────────────────
run_cpp_noargs "Lab14 C++ CPU add (42)" \
    "lab14_processing_unit/primitive_cpu.cpp"  "(expected 42)"

run_cpp_noargs "Lab14 C++ CPU countdown" \
    "lab14_processing_unit/primitive_cpu.cpp"  "(expected 0)"

# ── Lab 14: Primitive CPU (Python) ────────────────────────────────────────
run_py "Lab14 Python CPU add (42)" \
    "lab14_processing_unit/primitive_cpu.py"  ""  "(expected 42)"

# ── Lab 15: Pipeline (C++) ────────────────────────────────────────────────
run_cpp_noargs "Lab15 C++ pipeline CPI" \
    "lab15_pipeline/pipeline.cpp"  "CPI:"

run_cpp_noargs "Lab15 C++ pipeline stalls" \
    "lab15_pipeline/pipeline.cpp"  "Stalls:"

# ── Lab 15: Pipeline (Python) ─────────────────────────────────────────────
run_py "Lab15 Python pipeline" \
    "lab15_pipeline/pipeline.py"  ""  "CPI"

# ══════════════════════════════════════════════════════════════════════════
echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ]
