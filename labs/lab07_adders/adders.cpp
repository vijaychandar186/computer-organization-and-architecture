// Lab 07 – Half Adder and Full Adder
// Gate-level simulation with truth tables.
// No input required; run: ./adders

#include <iostream>
#include <string>
using namespace std;

// Gate primitives
int AND(int a, int b) { return a & b; }
int OR (int a, int b) { return a | b; }
int XOR(int a, int b) { return a ^ b; }
int NOT(int a)        { return 1 - a; }

// Half Adder: sum = A XOR B,  carry = A AND B
pair<int,int> halfAdder(int a, int b) {
    return { XOR(a, b), AND(a, b) };
}

// Full Adder: built from two half adders + one OR gate
pair<int,int> fullAdder(int a, int b, int cin) {
    auto [s1, c1] = halfAdder(a, b);
    auto [s,  c2] = halfAdder(s1, cin);
    return { s, OR(c1, c2) };
}

void printHalfAdderTable() {
    cout << "Half Adder Truth Table\n";
    cout << "+---+---+-----+-------+\n";
    cout << "| A | B | Sum | Carry |\n";
    cout << "+---+---+-----+-------+\n";
    for (int a : {0, 1})
        for (int b : {0, 1}) {
            auto [s, c] = halfAdder(a, b);
            cout << "| " << a << " | " << b
                 << " |  "  << s << "  |   " << c << "   |\n";
        }
    cout << "+---+---+-----+-------+\n";
}

void printFullAdderTable() {
    cout << "\nFull Adder Truth Table\n";
    cout << "+---+---+-----+-----+-------+\n";
    cout << "| A | B | Cin | Sum | Cout  |\n";
    cout << "+---+---+-----+-----+-------+\n";
    for (int a : {0, 1})
        for (int b : {0, 1})
            for (int cin : {0, 1}) {
                auto [s, c] = fullAdder(a, b, cin);
                cout << "| " << a << " | " << b
                     << " |  "  << cin
                     << "  |  "  << s
                     << "  |   "  << c << "   |\n";
            }
    cout << "+---+---+-----+-----+-------+\n";
}

void printDiagram() {
    cout << "Half Adder (gate diagram):\n"
         << "  A --+--[XOR]---- Sum\n"
         << "  B --+\n"
         << "  A --+--[AND]---- Carry\n"
         << "  B --+\n\n"
         << "Full Adder = two Half Adders + one OR:\n"
         << "  A --+--[HA1]--S1--+--[HA2]---- Sum\n"
         << "  B --+      +--C1--+\n"
         << "  Cin--------------[HA2]--C2--+\n"
         << "                    C1 -------+--[OR]---- Cout\n\n";
}

int main() {
    printDiagram();
    printHalfAdderTable();
    printFullAdderTable();
    return 0;
}
