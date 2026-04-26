// Lab 10 – Array Multiplier
// N×N unsigned multiplication via AND gate array + Full Adder triangle.
// Input: A B n
// Output: partial products + final product

#include <iostream>
#include <vector>
#include <string>
using namespace std;

pair<int,int> fullAdder(int a, int b, int cin) {
    return { a ^ b ^ cin, (a & b) | (b & cin) | (a & cin) };
}

string toBinary(long long val, int n) {
    string s(n, '0');
    for (int i = 0; i < n; i++)
        s[n-1-i] = '0' + ((val >> i) & 1);
    return s;
}

long long arrayMultiply(int A, int B, int n) {
    // AND gate array: PP[i][j] = A[j] AND B[i]
    vector<vector<int>> PP(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            PP[i][j] = ((A >> j) & 1) & ((B >> i) & 1);

    // accumulate partial products into a 2n-bit array
    vector<int> acc(2*n, 0);
    for (int j = 0; j < n; j++) acc[j] = PP[0][j];

    for (int i = 1; i < n; i++) {
        int carry = 0;
        for (int j = 0; j < n; j++) {
            auto [s, co] = fullAdder(acc[i+j], PP[i][j], carry);
            acc[i+j] = s;
            carry = co;
        }
        int pos = i + n;
        while (carry && pos < 2*n) {
            auto [s, co] = fullAdder(acc[pos], 0, carry);
            acc[pos] = s; carry = co; pos++;
        }
    }

    long long result = 0;
    for (int k = 0; k < 2*n; k++) result |= (long long)acc[k] << k;
    return result;
}

int main() {
    int A, B, n;
    cout << "Enter A B n (e.g. 6 5 4): ";
    cin >> A >> B >> n;

    cout << "\n" << n << "-bit Array Multiplier\n";
    cout << "  A = " << toBinary(A, n) << "  (" << A << ")\n";
    cout << "  B = " << toBinary(B, n) << "  (" << B << ")\n\n";

    cout << "  Partial Products (PP[i] = A * B[i], shifted by i):\n";
    for (int i = 0; i < n; i++) {
        int bi = (B >> i) & 1;
        long long pp = 0;
        for (int j = 0; j < n; j++)
            pp |= (long long)(((A >> j) & 1) & bi) << (i + j);
        cout << "  PP[" << i << "] (B[" << i << "]=" << bi << ") = "
             << toBinary(pp, 2*n) << "\n";
    }

    long long product = arrayMultiply(A, B, n);
    cout << "\n  Product = " << toBinary(product, 2*n)
         << "  (" << product << ")\n";
    cout << "  Check: " << A << " x " << B << " = " << A*B
         << (product == (long long)A*B ? "  OK" : "  MISMATCH") << "\n";
    return 0;
}
