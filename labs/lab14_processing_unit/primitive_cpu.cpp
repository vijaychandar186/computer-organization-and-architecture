// Lab 14 – Primitive Processing Unit
// Simulates fetch-decode-execute with MAR/MDR/ACC/PC/IR and R0-R3.
// No input; built-in demo programs. Pass --trace for micro-op output.

#include <iostream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstring>
#include <cstdio>
using namespace std;

// ── Opcode constants ──────────────────────────────────────────────────────
enum Op { LOAD=1, STORE, MOV, ADD, SUB, BAND, BOR, BNOT, JMP, JZ, JNZ, MOVI, HLT=15 };

// Encode a 16-bit instruction word
uint16_t enc(int op, int f1=0, int f2=0, int imm=0) {
    return (uint16_t)( ((op&0xF)<<12) | ((f1&0xF)<<8) | ((f2&0xF)<<4) | (imm&0xF) );
}

// Instruction builder macros
#define ILOAD(r,a)   enc(LOAD,  r, (a>>4)&0xF, a&0xF)
#define ISTORE(r,a)  enc(STORE, r, (a>>4)&0xF, a&0xF)
#define IMOV(d,s)    enc(MOV,   d, s)
#define IADD(d,s)    enc(ADD,   d, s)
#define ISUB(d,s)    enc(SUB,   d, s)
#define IJMP(a)      enc(JMP,   (a>>8)&0xF, (a>>4)&0xF, a&0xF)
#define IJZ(a)       enc(JZ,    (a>>8)&0xF, (a>>4)&0xF, a&0xF)
#define IJNZ(a)      enc(JNZ,   (a>>8)&0xF, (a>>4)&0xF, a&0xF)
#define IMOVI(r,i)   enc(MOVI,  r, 0, i)
#define IHLT()       enc(HLT)

// ── CPU ────────────────────────────────────────────────────────────────────
struct CPU {
    uint16_t mem[256];
    uint16_t R[4];
    uint16_t PC, IR, MAR, MDR, ACC;
    int ZF;
    bool halted;
    int cycles;
    bool trace;

    CPU() {
        memset(mem, 0, sizeof(mem));
        memset(R, 0, sizeof(R));
        PC=IR=MAR=MDR=ACC=0; ZF=0; halted=false; cycles=0; trace=false;
    }

    void load(const vector<uint16_t>& prog, int start=0) {
        for (int i=0; i<(int)prog.size(); i++) mem[start+i] = prog[i];
        PC = (uint16_t)start;
    }

    void t(const char* msg) { if (trace) printf("    u  %s\n", msg); }

    void step() {
        if (halted) return;
        cycles++;
        if (trace)
            printf("\n[Cycle %3d] PC=%d  R0=%d R1=%d R2=%d R3=%d  ACC=%d  ZF=%d\n",
                   cycles, PC, R[0], R[1], R[2], R[3], ACC, ZF);

        // Fetch
        MAR = PC; t("MAR <- PC");
        MDR = mem[MAR & 0xFF]; t("MDR <- MEM[MAR]");
        IR  = MDR; t("IR  <- MDR");
        PC  = (uint16_t)(PC + 1); t("PC  <- PC+1");

        int op  = (IR >> 12) & 0xF;
        int f1  = (IR >>  8) & 0xF;
        int f2  = (IR >>  4) & 0xF;
        int imm =  IR        & 0xF;

        int addr;
        switch (op) {
        case HLT:
            halted = true; t("HLT"); break;
        case LOAD:
            addr = (f2 << 4) | imm;
            MAR  = (uint16_t)addr;
            MDR  = mem[addr & 0xFF];
            R[f1 & 3] = MDR;
            break;
        case STORE:
            addr = (f2 << 4) | imm;
            mem[addr & 0xFF] = R[f1 & 3];
            break;
        case MOV:
            R[f1 & 3] = R[f2 & 3]; break;
        case ADD:
            ACC = (uint16_t)(R[f1&3] + R[f2&3]);
            ZF  = (ACC == 0);
            R[f1 & 3] = ACC; break;
        case SUB:
            ACC = (uint16_t)(R[f1&3] - R[f2&3]);
            ZF  = (ACC == 0);
            R[f1 & 3] = ACC; break;
        case BAND:
            ACC = R[f1&3] & R[f2&3]; ZF = (ACC==0); R[f1&3] = ACC; break;
        case BOR:
            ACC = R[f1&3] | R[f2&3]; ZF = (ACC==0); R[f1&3] = ACC; break;
        case BNOT:
            ACC = ~R[f1&3]; ZF = (ACC==0); R[f1&3] = ACC; break;
        case JMP:
            PC = (uint16_t)(((f1 & 0xF) << 8) | ((f2 & 0xF) << 4) | (imm & 0xF));
            break;
        case JZ:
            if (ZF)
                PC = (uint16_t)(((f1 & 0xF) << 8) | ((f2 & 0xF) << 4) | (imm & 0xF));
            break;
        case JNZ:
            if (!ZF)
                PC = (uint16_t)(((f1 & 0xF) << 8) | ((f2 & 0xF) << 4) | (imm & 0xF));
            break;
        case MOVI:
            R[f1 & 3] = (uint16_t)imm; break;
        }
    }

    void run(int maxCycles=1000) {
        while (!halted && cycles < maxCycles) step();
    }

    void dump() {
        printf("\n  CPU State: PC=%d  ACC=%d  ZF=%d  halted=%s  cycles=%d\n",
               PC, ACC, ZF, halted ? "yes" : "no", cycles);
        printf("  R0=%d  R1=%d  R2=%d  R3=%d\n", R[0], R[1], R[2], R[3]);
    }
};

// ── Demo programs ──────────────────────────────────────────────────────────
void demoAdd(bool tr) {
    // R0 = MEM[0x20] + MEM[0x21];  MEM[0x22] = R0
    vector<uint16_t> prog = {
        ILOAD(0, 0x20), ILOAD(1, 0x21), IADD(0, 1), ISTORE(0, 0x22), IHLT()
    };
    CPU cpu; cpu.trace = tr;
    cpu.load(prog, 0);
    cpu.mem[0x20] = 15;
    cpu.mem[0x21] = 27;
    printf("Program 1: Add two memory values (15 + 27)\n");
    cpu.run();
    cpu.dump();
    printf("  MEM[0x22] = %d  (expected 42)\n", cpu.mem[0x22]);
}

void demoCountdown(bool tr) {
    // count down from 5 to 0 using R0=R0-R1
    vector<uint16_t> prog = {
        IMOVI(0, 5),   // 0: R0 = 5
        IMOVI(1, 1),   // 1: R1 = 1
        ISUB(0, 1),    // 2: R0 = R0 - 1  (sets ZF if zero)
        IJNZ(2),       // 3: if R0 != 0 goto 2
        IHLT(),        // 4
    };
    CPU cpu; cpu.trace = tr;
    cpu.load(prog, 0);
    printf("\nProgram 2: Count down from 5 to 0\n");
    cpu.run();
    cpu.dump();
    printf("  R0 = %d  (expected 0)  Cycles = %d\n", cpu.R[0], cpu.cycles);
}

int main(int argc, char* argv[]) {
    bool tr = (argc >= 2 && strcmp(argv[1], "--trace") == 0);
    demoAdd(tr);
    demoCountdown(tr);
    return 0;
}
