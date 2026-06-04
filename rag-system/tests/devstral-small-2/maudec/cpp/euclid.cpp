//
//	<comment from="devstral-small-2">
//	The original code is already quite efficient as it implements the Euclidean algorithm for computing the greatest common divisor (GCD). However, we can make a few minor improvements to enhance readability and efficiency slightly.
//	</comment>
//

int u0024gcd(int M, int N) {
    while (N != 0) {
        int temp = M % N;
        M = N;
        N = temp;
    }
    return M;
}