// Lab 09 – Carry Look-Ahead Adder (CLA)
// Computes all carries in parallel using Generate and Propagate signals.
// Input: A B n
// Output: G/P vectors, look-ahead carry equations, sum

#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct CLAResult {
    int sum;
    int carryOut;
    vector<int> G, P, C;   // C has n+1 elements: C[0]=cin, C[n]=carry-out
};

CLAResult cla(int A, int B, int n, int cin = 0) {
    vector<int> G(n), P(n), C(n+1);
    C[0] = cin;

    for (int i = 0; i < n; i++) {
        int ai = (A >> i) & 1;
        int bi = (B >> i) & 1;
        G[i] = ai & bi;           // Generate
        P[i] = ai ^ bi;           // Propagate
    }
    for (int i = 0; i < n; i++)
        C[i+1] = G[i] | (P[i] & C[i]);

    int sum = 0;
    for (int i = 0; i < n; i++)
        sum |= (P[i] ^ C[i]) << i;

    return { sum, C[n], G, P, C };
}

string toBinary(int val, int n) {
    string s(n, '0');
    for (int i = 0; i < n; i++)
        s[n-1-i] = '0' + ((val >> i) & 1);
    return s;
}

int main() {
    int A, B, n;
    cout << "Enter A B n (e.g. 13 11 4): ";
    cin >> A >> B >> n;

    auto res = cla(A, B, n);

    cout << "\n" << n << "-bit Carry Look-Ahead Addition\n";
    cout << "  A = " << toBinary(A, n) << "  (" << A << ")\n";
    cout << "  B = " << toBinary(B, n) << "  (" << B << ")\n\n";

    cout << "  Bit   A  B   G  P  Cin  Sum  Cout\n";
    cout << "  " << string(38, '-') << "\n";
    for (int i = 0; i < n; i++) {
        int ai = (A >> i) & 1, bi = (B >> i) & 1;
        int si = res.P[i] ^ res.C[i];
        cout << "   " << i << "    " << ai << "  " << bi
             << "   " << res.G[i] << "  " << res.P[i]
             << "    " << res.C[i] << "    " << si
             << "     " << res.C[i+1] << "\n";
    }

    cout << "\n  Sum  = " << toBinary(res.sum, n) << "  (" << res.sum << ")\n";
    cout << "  Cout = " << res.carryOut;
    if (res.carryOut) cout << "  <- overflow!";
    cout << "\n";

    cout << "\nLook-Ahead Carry Equations (no ripple):\n";
    for (int i = 1; i <= n; i++) {
        cout << "  C" << i << " = G" << (i-1);
        string prop = "";
        for (int j = i-1; j >= 1; j--) {
            prop += "P" + to_string(j-1);
            // build product of P[j-1..i-2] then G[j-1]
            // simplified: just note the structure
        }
        // Print full expansion
        for (int j = i-2; j >= 0; j--) {
            cout << " + (";
            for (int k = j+1; k < i; k++) cout << "P" << k-1;
            cout << "*G" << j << ")";
        }
        cout << " + (";
        for (int k = 0; k < i; k++) cout << "P" << k;
        cout << "*C0)\n";
    }
    return 0;
}
