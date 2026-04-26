// Lab 11 – Booth's Algorithm: step-by-step trace
// Input: M Q n   (signed multiplicand, multiplier, bit-width)
// Output: register state at each iteration

#include <iostream>
#include <string>
#include <cmath>
using namespace std;

// n-bit 2's complement: value -> unsigned representation
int toTC(int val, int n) {
    int mask = (1 << n) - 1;
    return val < 0 ? (val + (1 << n)) & mask : val & mask;
}

// unsigned n-bit value -> signed
int fromTC(int bits, int n) {
    return (bits >= (1 << (n-1))) ? bits - (1 << n) : bits;
}

string fmtBits(int val, int n) {
    val &= (1 << n) - 1;
    string s(n, '0');
    for (int i = 0; i < n; i++) s[n-1-i] = '0' + ((val >> i) & 1);
    return s;
}

// arithmetic right shift of n-bit value
int ars(int val, int n) {
    val &= (1 << n) - 1;
    int sign = (val >> (n-1)) & 1;
    val >>= 1;
    if (sign) val |= (1 << (n-1));
    return val & ((1 << n) - 1);
}

void boothTrace(int M, int Q, int n) {
    int mask  = (1 << n) - 1;
    int A     = 0;
    int Qreg  = toTC(Q, n);
    int Qm1   = 0;
    int Mpos  = toTC(M, n);
    int Mneg  = toTC(-M, n);

    cout << "\nBooth's Algorithm  M=" << M << "  Q=" << Q
         << "  (" << n << "-bit)\n";
    cout << "  M  = " << fmtBits(Mpos, n) << "\n";
    cout << "  -M = " << fmtBits(Mneg, n) << "\n\n";

    string hdr = "  Step  A         Q         Q-1  Q[0]  Action";
    cout << hdr << "\n";
    cout << "  " << string(hdr.size()-2, '-') << "\n";

    auto printRow = [&](const string& step, const string& action) {
        cout << "  " << step;
        // pad step to 5 chars
        for (int i = step.size(); i < 5; i++) cout << ' ';
        cout << "  " << fmtBits(A, n)
             << "  " << fmtBits(Qreg, n)
             << "    " << Qm1
             << "     " << (Qreg & 1)
             << "   " << action << "\n";
    };

    printRow("Init", "");

    for (int step = 1; step <= n; step++) {
        int q0  = Qreg & 1;
        string action;

        if      (q0 == 1 && Qm1 == 0) { A = (A + Mneg) & mask; action = "A = A - M"; }
        else if (q0 == 0 && Qm1 == 1) { A = (A + Mpos) & mask; action = "A = A + M"; }
        else                           { action = "no-op"; }

        int newQm1  = Qreg & 1;
        int newQreg = ((Qreg >> 1) | ((A & 1) << (n-1))) & mask;
        int newA    = ars(A, n);
        Qm1  = newQm1;
        Qreg = newQreg;
        A    = newA;

        printRow(to_string(step), action);
    }

    int resultBits = (A << n) | Qreg;
    int result     = fromTC(resultBits, 2*n);
    cout << "\n  Result A:Q = " << fmtBits(A, n) << " " << fmtBits(Qreg, n)
         << "  (" << result << ")\n";
    cout << "  Expected: " << M << " x " << Q << " = " << M*Q << "\n";
    cout << "  " << (result == M*Q ? "PASS" : "FAIL") << "\n";
}

int main() {
    int M, Q, n;
    cout << "Enter M Q n (e.g. -3 7 4): ";
    cin >> M >> Q >> n;
    boothTrace(M, Q, n);
    return 0;
}
