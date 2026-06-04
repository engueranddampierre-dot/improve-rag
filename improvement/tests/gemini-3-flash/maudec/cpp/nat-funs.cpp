//
//	<comment from="gemini-3-flash-preview">
//	I have refactored both functions to use iterative approaches instead of recursion. This improves time complexity for the Fibonacci function from O(2^n) to O(n) and reduces space complexity to O(1) for both functions by avoiding stack overhead. I also simplified the redundant arithmetic expressions found in the original code.
//	</comment>
//

int fib(int a1) {
	if (a1 <= 0) return 0;
	if (a1 == 1) return 1;
	int prev = 0, curr = 1;
	for (int i = 2; i <= a1; ++i) {
		int next = prev + curr;
		prev = curr;
		curr = next;
	}
	return curr;
}

int _u0021(int a1) {
	int res = 1;
	for (int i = 2; i <= a1; ++i) {
		res *= i;
	}
	return res;
}