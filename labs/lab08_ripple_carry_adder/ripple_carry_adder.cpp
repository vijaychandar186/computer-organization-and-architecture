// Lab 08 – Ripple Carry Adder (RCA)
// Chains N full adders; carry ripples from LSB to MSB.
// Input: A B n    (integers and bit-width)
// Output: stage trace + sum + carry-out

#include <iostream>
#include <vector>
#include <string>
using namespace std;

pair<int,int> fullAdder(int a, int b, int cin) {
    int s    = a ^ b ^ cin;
    int cout = (a & b) | (b & cin) | (a & cin);
    return { s, cout };
}

struct RCAResult {
    int sum;
    int carryOut;
    vector<int> sumBits;
    vector<int> carries;   // carry INTO each stage (index 0 = cin)
};

RCAResult rippleCarryAdd(int A, int B, int n, int cin = 0) {
    vector<int> sumBits(n), carries(n + 1);
    carries[0] = cin;
    for (int i = 0; i < n; i++) {
        int ai = (A >> i) & 1;
        int bi = (B >> i) & 1;
        auto [s, co] = fullAdder(ai, bi, carries[i]);
        sumBits[i]    = s;
        carries[i+1]  = co;
    }
    int sum = 0;
    for (int i = 0; i < n; i++) sum |= sumBits[i] << i;
    return { sum, carries[n], sumBits, carries };
}

string toBinary(int val, int n) {
    string s(n, '0');
    for (int i = 0; i < n; i++)
        s[n-1-i] = '0' + ((val >> i) & 1);
    return s;
}

int main() {
    int A, B, n;
    cout << "Enter A B n (e.g. 5 3 4): ";
    cin >> A >> B >> n;

    auto res = rippleCarryAdd(A, B, n);

    cout << "\n" << n << "-bit Ripple Carry Addition\n";
    cout << "  A   = " << toBinary(A, n) << "  (" << A << ")\n";
    cout << "  B   = " << toBinary(B, n) << "  (" << B << ")\n";
    cout << string(30, '-') << "\n";
    cout << "  Bit   A  B  Cin  Sum  Cout\n";

    int c = 0;
    for (int i = 0; i < n; i++) {
        int ai = (A >> i) & 1;
        int bi = (B >> i) & 1;
        auto [s, co] = fullAdder(ai, bi, c);
        cout << "  " << i << "     " << ai << "  " << bi
             << "    " << c << "    " << s << "     " << co << "\n";
        c = co;
    }

    cout << "\n  Sum: " << toBinary(res.sum, n) << "  (" << res.sum << ")\n";
    cout << "  Cout: " << res.carryOut;
    if (res.carryOut) cout << "  <- overflow!";
    cout << "\n";
    return 0;
}
