// Lab 13 – Carry Save Adder + CSA-based Multiplication
// CSA mode input:  A B C n
// Multiply mode:   run binary with --multiply flag (uses built-in demo)

#include <iostream>
#include <vector>
#include <string>
#include <cstring>
using namespace std;

pair<int,int> fullAdder(int a, int b, int cin) {
    return { a ^ b ^ cin, (a & b) | (b & cin) | (a & cin) };
}

// CSA: reduce A+B+C to (sum_vec, carry_vec)
// A+B+C == sum_vec + (carry_vec << 1)
pair<int,int> csaAdd(int A, int B, int C, int n) {
    int S = 0, K = 0;
    for (int i = 0; i < n; i++) {
        auto [s, k] = fullAdder((A>>i)&1, (B>>i)&1, (C>>i)&1);
        S |= s << i;
        K |= k << i;
    }
    return { S, K };
}

string toBinary(long long v, int n) {
    string s(n, '0');
    for (int i = 0; i < n; i++) s[n-1-i] = '0' + ((v>>i)&1);
    return s;
}

void printCSA(int A, int B, int C, int n) {
    auto [S, K] = csaAdd(A, B, C, n);
    int result  = S + (K << 1);

    cout << "\nCarry Save Addition (" << n << "-bit)\n";
    cout << "  A = " << toBinary(A,n) << "  (" << A << ")\n";
    cout << "  B = " << toBinary(B,n) << "  (" << B << ")\n";
    cout << "  C = " << toBinary(C,n) << "  (" << C << ")\n\n";
    cout << "  CSA Stage:\n";
    cout << "  Sum vector   S = " << toBinary(S,n) << "  (" << S << ")\n";
    cout << "  Carry vector K = " << toBinary(K,n) << "  (" << K << ")\n";
    cout << "  K shifted (K<<1) = " << toBinary((long long)K<<1, n+1)
         << "  (" << (K<<1) << ")\n\n";
    cout << "  Final add S + (K<<1) = " << result << "\n";
    cout << "  Expected A+B+C      = " << A+B+C << "\n";
    cout << "  Match: " << (result == A+B+C ? "OK" : "FAIL") << "\n";
}

long long csaMultiply(int M, int Q, int n) {
    vector<int> Mbits(n), Qbits(n);
    for (int i = 0; i < n; i++) { Mbits[i]=(M>>i)&1; Qbits[i]=(Q>>i)&1; }

    // generate n partial products (each shifted left by i)
    vector<long long> pp(n, 0);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            pp[i] |= (long long)(Mbits[j] & Qbits[i]) << (i+j);

    // CSA tree: reduce while >2 operands
    while (pp.size() > 2) {
        vector<long long> next;
        size_t i = 0;
        while (i + 2 < pp.size()) {
            auto [S, K] = csaAdd((int)pp[i], (int)pp[i+1], (int)pp[i+2], 2*n);
            next.push_back(S);
            next.push_back((long long)K << 1);
            i += 3;
        }
        while (i < pp.size()) next.push_back(pp[i++]);
        pp = next;
    }

    long long product = 0;
    for (auto v : pp) product += v;
    return product;
}

void printMultiply(int M, int Q, int n) {
    long long product  = csaMultiply(M, Q, n);
    long long expected = (long long)M * Q;
    cout << "\nCSA Multiplication (" << n << "-bit)\n";
    cout << "  M = " << toBinary(M,n) << "  (" << M << ")\n";
    cout << "  Q = " << toBinary(Q,n) << "  (" << Q << ")\n";
    cout << "  Product  = " << product << "\n";
    cout << "  Expected = " << expected << "\n";
    cout << "  Match: " << (product == expected ? "OK" : "FAIL") << "\n";
}

int main(int argc, char* argv[]) {
    bool multiplyMode = (argc >= 2 && strcmp(argv[1], "--multiply") == 0);

    if (multiplyMode && argc >= 4) {
        int M = atoi(argv[2]);
        int Q = atoi(argv[3]);
        int n = argc >= 5 ? atoi(argv[4]) : 4;
        printMultiply(M, Q, n);
        return 0;
    }

    int A, B, C, n;
    cout << "Enter A B C n (e.g. 13 11 7 5): ";
    cin >> A >> B >> C >> n;
    printCSA(A, B, C, n);
    return 0;
}
