// Lab 12 – Booth's Algorithm: clean implementation + test suite
// Input (single run): M Q n
// No args: runs built-in test suite

#include <iostream>
#include <vector>
#include <tuple>
#include <string>
using namespace std;

int toTC(int val, int n) {
    return val < 0 ? (val + (1 << n)) & ((1 << n)-1) : val & ((1 << n)-1);
}

int fromTC(long long bits, int n) {
    long long half = 1LL << (n-1);
    return bits >= half ? (int)(bits - (1LL << n)) : (int)bits;
}

int ars(int val, int n) {
    val &= (1 << n) - 1;
    int sign = (val >> (n-1)) & 1;
    val >>= 1;
    if (sign) val |= 1 << (n-1);
    return val & ((1 << n) - 1);
}

int boothMultiply(int M, int Q, int n) {
    int mask = (1 << n) - 1;
    int A    = 0;
    int Qreg = toTC(Q, n);
    int Qm1  = 0;
    int Mpos = toTC(M, n);
    int Mneg = toTC(-M, n);

    for (int i = 0; i < n; i++) {
        int q0 = Qreg & 1;
        if      (q0 == 1 && Qm1 == 0) A = (A + Mneg) & mask;
        else if (q0 == 0 && Qm1 == 1) A = (A + Mpos) & mask;

        int newQm1  = Qreg & 1;
        int newQreg = ((Qreg >> 1) | ((A & 1) << (n-1))) & mask;
        A    = ars(A, n);
        Qm1  = newQm1;
        Qreg = newQreg;
    }

    long long resultBits = ((long long)A << n) | Qreg;
    return fromTC(resultBits, 2*n);
}

void runTests() {
    // { M, Q, n }
    vector<tuple<int,int,int>> cases = {
        {-3,  7, 4}, { 7, -3, 4}, { 3,  5, 4},
        {-4, -3, 4}, { 6,  7, 4}, { 0,  5, 4},
        { 5,  0, 4}, {-1, -1, 4}, { 7,  7, 4},
        {-8,  7, 5}, {-8, -7, 5}, {15, 15, 5},
    };

    cout << "Booth's Algorithm – Test Suite\n";
    cout << "  M       Q    bits   Result   Expected   OK\n";
    cout << "  " << string(48, '-') << "\n";

    bool allPass = true;
    for (auto [M, Q, n] : cases) {
        int result   = boothMultiply(M, Q, n);
        int expected = M * Q;
        bool ok      = (result == expected);
        allPass      = allPass && ok;
        printf("  %-6d  %-6d  %3d    %-8d  %-9d  %s\n",
               M, Q, n, result, expected, ok ? "OK" : "FAIL");
    }
    cout << "\n  " << (allPass ? "All tests passed." : "SOME TESTS FAILED.") << "\n";
}

int main(int argc, char* argv[]) {
    if (argc >= 3) {
        int M = atoi(argv[1]);
        int Q = atoi(argv[2]);
        int n = argc >= 4 ? atoi(argv[3]) : 4;
        cout << M << " x " << Q << " = " << boothMultiply(M, Q, n)
             << "  (using " << n << "-bit Booth)\n";
    } else {
        runTests();
    }
    return 0;
}
