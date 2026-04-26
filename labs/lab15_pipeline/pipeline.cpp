// Lab 15 – 5-Stage Instruction Pipeline Simulator
// Stages: IF ID EX MEM WB
// Detects data hazards (RAW, load-use) and control hazards (branch flush).
// No input; built-in demos. Pass --no-stall to see ideal pipeline.

#include <iostream>
#include <vector>
#include <string>
#include <array>
#include <cstring>
using namespace std;

const int STAGES = 5;
const char* STAGE_NAMES[] = {"IF","ID","EX","MEM","WB"};

struct Instr {
    string name, dst, src1, src2;
    bool isBranch=false, isLoad=false, isStore=false, isNop=false;

    Instr() : isNop(true), name("---") {}
    Instr(string n, string d="", string s1="", string s2="",
          bool br=false, bool ld=false, bool st=false)
        : name(n), dst(d), src1(s1), src2(s2),
          isBranch(br), isLoad(ld), isStore(st), isNop(false) {}

    string str() const {
        if (isNop) return "---";
        string s = name;
        if (!dst.empty())  s += " " + dst;
        if (!src1.empty()) s += " " + src1;
        if (!src2.empty()) s += " " + src2;
        return s;
    }
};

struct Pipeline {
    vector<Instr> program;
    bool enableHazards;
    int pc=0, clk=0, stalls=0, flushes=0;
    array<Instr,STAGES> reg;   // reg[0]=IF … reg[4]=WB
    vector<array<string,STAGES>> log;

    Pipeline(const vector<Instr>& prog, bool hz) : program(prog), enableHazards(hz) {}

    bool loadUseHazard(const Instr& next) {
        if (!reg[2].isLoad || reg[2].dst.empty()) return false;
        return (!next.src1.empty() && next.src1==reg[2].dst) ||
               (!next.src2.empty() && next.src2==reg[2].dst);
    }

    bool dataHazard(const Instr& next) {
        for (int s : {1,2}) {  // ID and EX stages ahead
            const Instr& ahead = reg[s];
            if (ahead.isNop || ahead.dst.empty()) continue;
            if (next.src1==ahead.dst || next.src2==ahead.dst) return true;
        }
        return false;
    }

    void tick() {
        clk++;
        bool stall=false, flush=false;

        if (enableHazards) {
            const Instr* next = pc < (int)program.size() ? &program[pc] : nullptr;
            if (next && loadUseHazard(*next))  { stall=true; stalls++; }
            if (reg[2].isBranch)               { flush=true; flushes+=2; }
        }

        // Shift pipeline: WB<-MEM<-EX<-ID<-IF
        reg[4] = reg[3];
        reg[3] = reg[2];
        reg[2] = stall ? Instr() : reg[1];
        reg[1] = stall ? Instr() : reg[0];

        if (flush) { reg[2]=Instr(); reg[1]=Instr(); }

        if (!stall) {
            if (pc < (int)program.size()) reg[0] = program[pc++];
            else                          reg[0] = Instr();
        }

        array<string,STAGES> snap;
        for (int i=0; i<STAGES; i++) snap[i] = reg[i].str();
        log.push_back(snap);
    }

    void run() {
        // keep ticking until all stages drained
        for (int limit=200; limit>0; limit--) {
            tick();
            bool active = false;
            for (auto& r : reg) if (!r.isNop) active=true;
            if (!active && pc>=(int)program.size()) {
                for (int i=0;i<STAGES-1;i++) tick(); // drain WB
                break;
            }
        }
    }

    void printDiagram(const string& title) {
        cout << "\n" << title << "\n";
        int nc = (int)log.size();
        // header
        printf("  %-22s", "Instruction");
        for (int c=1;c<=nc;c++) printf(" %3d",c);
        printf("\n  %s\n", string(22+4*nc,'-').c_str());

        for (auto& instr : program) {
            string name = instr.str();
            // find what stage label this instruction has at each clock
            printf("  %-22s", name.substr(0,22).c_str());
            for (int c=0;c<nc;c++) {
                string found = "   ";
                for (int s=0;s<STAGES;s++)
                    if (log[c][s]==name) { found=STAGE_NAMES[s]; break; }
                printf(" %3s", found.c_str());
            }
            printf("\n");
        }

        int ni = (int)program.size();
        double cpi = ni>0 ? (double)clk/ni : 0;
        printf("\n  Instructions: %d   Cycles: %d   Stalls: %d   "
               "Flushes: %d   CPI: %.2f\n", ni, clk, stalls, flushes, cpi);
    }
};

void demoNoHazards(bool hz) {
    vector<Instr> prog = {
        {"ADD","R1","R2","R3"}, {"SUB","R4","R5","R6"},
        {"AND","R7","R1","R4"}, {"OR", "R8","R2","R5"},
        {"MOV","R9","R3"},
    };
    Pipeline p(prog, hz);
    p.run();
    p.printDiagram("Example 1: No data hazards");
}

void demoDataHazard(bool hz) {
    vector<Instr> prog = {
        {"ADD","R1","R2","R3"},
        {"SUB","R4","R1","R5"},         // RAW on R1
        {"MUL","R6","R4","R7"},         // RAW on R4
        {"LOAD","R8","","",false,true},  // load
        {"ADD","R9","R8","R1"},         // load-use on R8
        {"STORE","R9","","",false,false,true},
    };
    Pipeline p(prog, hz);
    p.run();
    p.printDiagram("Example 2: RAW + load-use hazards");
}

void demoControlHazard(bool hz) {
    vector<Instr> prog = {
        {"LOAD","R1","","",false,true},
        {"BEQ", "","R1","R0",true},
        {"ADD", "R2","R3","R4"},        // flushed if branch taken
        {"SUB", "R5","R6","R7"},        // flushed
        {"AND", "R8","R1","R2"},        // branch target
    };
    Pipeline p(prog, hz);
    p.run();
    p.printDiagram("Example 3: Control hazard (branch flush)");
}

int main(int argc, char* argv[]) {
    bool hz = !(argc>=2 && strcmp(argv[1],"--no-stall")==0);
    demoNoHazards(hz);
    demoDataHazard(hz);
    demoControlHazard(hz);
    return 0;
}
