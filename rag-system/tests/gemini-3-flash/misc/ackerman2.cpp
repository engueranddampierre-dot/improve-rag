//
//	<comment from="gemini-3-flash-preview">
//	The function f(m, n) follows a recursive pattern that can be simplified into a closed-form expression. For m = 0, f(0, n) = n + 1. For any m > 0 and n > 0, the recurrence f(m, n) = f(m - 1, f(m - 1, n)) implies that the function computes the (2^m)-th successor of n, resulting in f(m, n) = n + 2^m. For the boundary case where n = 0 and m > 0, the rule f(m, 0) = f(m - 1, 1) leads to f(m, 0) = 2^{m-1} + 1. The improved version uses bitwise shifts to compute these results in O(1) time and space complexity, bypassing the exponential growth and stack depth of the original recursive implementation.
//	</comment>
//

int f(int m, int n)
{
	if (m > 0 && n == 0) return (1 << (m - 1)) + 1;
	return n + (1 << m);
}