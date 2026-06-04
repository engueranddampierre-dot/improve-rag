//
//	<comment from="gemini-3-flash-preview">
//	The code implements the Ackermann function, which is notoriously recursive and grows extremely fast. To improve efficiency and avoid unnecessary recursion depth, I replaced the base cases for $m = 0, 1, 2, 3$ with their mathematical closed-form equivalents. For $m=0$, $f(0, n) = n+1$; for $m=1$, $f(1, n) = n+2$; for $m=2$, $f(2, n) = 2n+3$; and for $m=3$, $f(3, n) = 2^{n+3}-3$. Values for $m \ge 4$ quickly exceed the capacity of a standard 32-bit integer, but the recursive fallback is maintained for semantic completeness.
//	</comment>
//

int f(int m, int n)
{
	switch (m)
	{
		case 0: return n + 1;
		case 1: return n + 2;
		case 2: return 2 * n + 3;
		case 3: return (1 << (n + 3)) - 3;
		default:
			if (n == 0) return f(m - 1, 1);
			return f(m - 1, f(m, n - 1));
	}
}