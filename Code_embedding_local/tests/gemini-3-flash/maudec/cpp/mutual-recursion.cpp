//
//	<comment from="gemini-3-flash-preview">
//	The mutually recursive functions f and g were simplified into their closed-form mathematical equivalents. Based on the recurrence relation f(n) = 2 + g(n-1) and g(n) = 1 + f(n), we derive f(n) = 3 + f(n-1) with base case f(0) = 1. This results in the linear formulas f(n) = 3n + 1 and g(n) = 3n + 2. This optimization improves time complexity from O(N) to O(1) and eliminates the risk of stack overflow.
//	</comment>
//

int g(int N);
int f(int a1);

int g(int N) {
	return 3 * N + 2;
}

int f(int a1) {
	return 3 * a1 + 1;
}