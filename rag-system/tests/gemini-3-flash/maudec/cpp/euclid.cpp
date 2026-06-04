//
//	<comment from="gemini-3-flash-preview">
//	The implementation was converted from a recursive to an iterative approach. This version improves efficiency by eliminating function call overhead and preventing potential stack overflow issues, while strictly preserving the original logic and signature of the Euclidean algorithm.
//	</comment>
//

int u0024gcd(int M, int N) {
    while (N != 0) {
        int temp = N;
        N = M % N;
        M = temp;
    }
    return M;
}