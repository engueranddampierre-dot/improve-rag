//
//	<comment from="gemini-3-flash-preview">
//	The function f(m, n) is a variation of the Ackermann function. I optimized it by implementing closed-form solutions for m = 0, 1, and 2, which eliminates deep recursion and significantly improves performance. Specifically, f(1, n) simplifies to 2n + 3 and f(2, n) simplifies to 2^(n+3) - 3. The redundant max call was also removed as f(m-1, 1) is always at least 3 for all m >= 1. These changes dramatically reduce complexity for smaller m and help prevent stack overflow.
//	</comment>
//

int f(int m, int n) {
    if (m == 0) return n + 2;
    if (m == 1) return 2 * n + 3;
    if (m == 2) return (1 << (n + 3)) - 3;
    if (n == 0) return f(m - 1, 1);
    return f(m - 1, f(m, n - 1));
}